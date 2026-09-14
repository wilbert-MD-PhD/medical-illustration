#!/usr/bin/env python3
"""Offline updater regression tests; no live installation or remote writes."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from urllib.error import HTTPError
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/'plugins/medical-illustration/skills/medical-illustration'
spec = importlib.util.spec_from_file_location('updater', SKILL/'scripts/update_skill.py')
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.installed = self.base/'user/skills'/u.NAME
        self.source = self.base/'release'/u.NAME
        shutil.copytree(SKILL, self.installed, ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(SKILL, self.source, ignore=shutil.ignore_patterns('__pycache__'))
        (self.installed/'VERSION').write_text('1.0.0', encoding='utf-8')
        (self.installed/'retired.txt').write_text('old', encoding='utf-8')
        self.seal(self.installed)
        (self.source/'VERSION').write_text('1.1.1', encoding='utf-8')
        self.archive, self.checksum = self.pack(self.source)
        self.before = u.fingerprint(self.installed)

    def seal(self, root):
        (root/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p, h in
            u.fingerprint(root, True).items()), encoding='utf-8')

    def pack(self, source, name='package.zip'):
        self.seal(source)
        archive = self.base/name
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in source.rglob('*'):
                if p.is_file():
                    z.write(p, u.NAME + '/' + p.relative_to(source).as_posix())
        checksum = archive.with_suffix('.zip.sha256')
        checksum.write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n')
        return archive, checksum

    def update(self, **kwargs):
        return u.update(self.installed, archive=self.archive, checksum=self.checksum, **kwargs)

    def test_clean_update_removes_retired_files_and_rollback_restores_exact_bytes(self):
        project = self.base/'user/project/story.md'
        project.parent.mkdir()
        project.write_text('existing project', encoding='utf-8')
        result = self.update()
        self.assertEqual(result['version'], '1.1.1')
        self.assertFalse((self.installed/'retired.txt').exists())
        self.assertEqual(u.fingerprint(Path(result['backup_dir'])), self.before)
        after = u.fingerprint(self.installed)
        restored = u.rollback(self.installed)
        self.assertEqual(u.fingerprint(self.installed), self.before)
        self.assertEqual(u.fingerprint(Path(restored['backup_dir'])), after)
        self.assertEqual(project.read_text(), 'existing project')
        self.assertFalse(u.state_dir(self.installed).is_relative_to(self.installed.parent))

    def test_local_changes_block_by_default_and_are_preserved_when_explicitly_replaced(self):
        (self.installed/'notes.txt').write_text('my local edits', encoding='utf-8')
        before = u.fingerprint(self.installed)
        with self.assertRaisesRegex(u.UpdateError, 'Local edits'):
            self.update()
        self.assertEqual(u.fingerprint(self.installed), before)
        result = self.update(replace_local=True)
        self.assertEqual(u.fingerprint(Path(result['backup_dir'])), before)
        u.rollback(self.installed)
        self.assertEqual(u.fingerprint(self.installed), before)

    def test_legacy_without_version_and_manifest_remains_unknown_and_can_be_restored(self):
        (self.installed/'VERSION').unlink()
        (self.installed/'SHA256SUMS').unlink()
        before = u.fingerprint(self.installed)
        info = u.local_info(self.installed)
        self.assertIsNone(info['version'])
        self.assertEqual(info['integrity'], 'unknown')
        with self.assertRaises(u.UpdateError):
            self.update()
        self.update(replace_local=True)
        u.rollback(self.installed)
        self.assertEqual(u.fingerprint(self.installed), before)

    def test_corrupt_download_keeps_original(self):
        with self.archive.open('ab') as f:
            f.write(b'corrupt')
        with self.assertRaisesRegex(u.UpdateError, 'Archive SHA-256 mismatch'):
            self.update()
        self.assertEqual(u.fingerprint(self.installed), self.before)

    def test_inner_manifest_tampering_rejected_even_with_valid_outer_checksum(self):
        (self.source/'SKILL.md').write_text((self.source/'SKILL.md').read_text(encoding='utf-8') + '\ntampered', encoding='utf-8')
        with zipfile.ZipFile(self.archive, 'w') as z:
            for p in self.source.rglob('*'):
                if p.is_file():
                    z.write(p, u.NAME + '/' + p.relative_to(self.source).as_posix())
        self.checksum.write_text(hashlib.sha256(self.archive.read_bytes()).hexdigest())
        with self.assertRaisesRegex(u.UpdateError, 'Package SHA256SUMS mismatch'):
            self.update()
        self.assertEqual(u.fingerprint(self.installed), self.before)

    def test_archive_traversal_symlink_and_case_collision_rejected(self):
        for kind in ('traversal', 'symlink', 'case'):
            with self.subTest(kind=kind):
                with zipfile.ZipFile(self.archive, 'w') as z:
                    if kind == 'traversal':
                        z.writestr(u.NAME + '/../escape', 'bad')
                    elif kind == 'symlink':
                        item = zipfile.ZipInfo(u.NAME + '/link')
                        item.create_system = 3
                        item.external_attr = (stat.S_IFLNK | 0o777) << 16
                        z.writestr(item, '/tmp/elsewhere')
                    else:
                        z.writestr(u.NAME + '/SKILL.md', 'a')
                        z.writestr(u.NAME + '/skill.md', 'b')
                self.checksum.write_text(hashlib.sha256(self.archive.read_bytes()).hexdigest())
                with self.assertRaisesRegex(u.UpdateError, 'Unsafe archive member'):
                    self.update()
                self.assertEqual(u.fingerprint(self.installed), self.before)

    def test_replacement_failure_automatically_restores_original(self):
        real_rename = Path.rename
        def fail_install(path, target):
            if path.name == u.NAME and path.parent.name == 'unpacked':
                raise OSError('injected disk failure')
            return real_rename(path, target)
        with patch.object(Path, 'rename', fail_install):
            with self.assertRaisesRegex(OSError, 'injected disk failure'):
                self.update()
        self.assertEqual(u.fingerprint(self.installed), self.before)
        self.assertFalse((u.state_dir(self.installed)/'lock').exists())

    def test_failed_restore_keeps_recovery_copy_and_lock(self):
        real_rename = Path.rename
        def fail(path, target):
            if path.parent.name == 'unpacked' or path.name == 'previous':
                raise OSError('injected failure')
            return real_rename(path, target)
        with patch.object(Path, 'rename', fail):
            with self.assertRaisesRegex(u.UpdateError, 'Recovery needs attention'):
                self.update()
        state = u.state_dir(self.installed)
        self.assertTrue((state/'lock').exists())
        previous = next(state.glob('*/previous'))
        self.assertEqual(u.fingerprint(previous), self.before)
        self.assertTrue((state/'recovery-required').exists())

    def test_concurrent_change_during_staging_is_not_overwritten(self):
        real_unpack = u.unpack
        def change(*args):
            result = real_unpack(*args)
            (self.installed/'live.txt').write_text('concurrent edit')
            return result
        with patch.object(u, 'unpack', change):
            with self.assertRaisesRegex(u.UpdateError, 'changed during preparation'):
                self.update()
        self.assertEqual((self.installed/'live.txt').read_text(), 'concurrent edit')
        self.assertEqual((self.installed/'VERSION').read_text(), '1.0.0')

    def test_lock_prevents_second_update(self):
        state = u.state_dir(self.installed)
        with u.lock(state):
            with self.assertRaisesRegex(u.UpdateError, 'lock exists'):
                self.update()
        self.assertEqual(u.fingerprint(self.installed), self.before)

    def test_rollback_protects_edits_made_after_update(self):
        self.update()
        (self.installed/'later.txt').write_text('new work')
        with self.assertRaisesRegex(u.UpdateError, 'changed after'):
            u.rollback(self.installed)
        result = u.rollback(self.installed, replace_local=True)
        self.assertEqual((Path(result['backup_dir'])/'later.txt').read_text(), 'new work')

    def test_damaged_backup_cannot_be_restored(self):
        result = self.update()
        (Path(result['backup_dir'])/'retired.txt').write_text('changed')
        after = u.fingerprint(self.installed)
        with self.assertRaisesRegex(u.UpdateError, 'Backup missing or modified'):
            u.rollback(self.installed)
        self.assertEqual(u.fingerprint(self.installed), after)

    def test_old_release_cannot_downgrade_newer_install(self):
        (self.installed/'VERSION').write_text('2.0.0')
        self.seal(self.installed)
        with self.assertRaisesRegex(u.UpdateError, 'Downgrade refused'):
            self.update()
        self.assertEqual((self.installed/'VERSION').read_text(), '2.0.0')

    def test_second_identical_update_is_noop(self):
        self.update()
        count = len(u.history(self.installed))
        self.assertEqual(self.update()['status'], 'already_current')
        self.assertEqual(len(u.history(self.installed)), count)

    def test_offline_check_has_no_writes_or_network(self):
        before = u.fingerprint(self.base)
        with patch.object(u, 'fetch', side_effect=AssertionError('must not network')):
            with patch('sys.stdout', new_callable=io.StringIO) as output:
                self.assertEqual(u.main(['check', '--offline', '--install-dir', str(self.installed)]), 0)
        data = json.loads(output.getvalue())
        self.assertEqual(data['remote_status'], 'not_checked')
        self.assertEqual(u.fingerprint(self.base), before)

    def test_multiple_candidates_require_explicit_target(self):
        with patch.object(u, 'candidates', return_value=[str(self.installed), str(self.source)]):
            with self.assertRaisesRegex(u.UpdateError, 'actually loaded copy'):
                u.locate(None)
            self.assertEqual(u.locate(self.installed)[0], self.installed)

    def test_managed_plugin_copy_is_not_overwritten(self):
        plugin = self.installed.parent.parent/'.codex-plugin'
        plugin.mkdir()
        (plugin/'plugin.json').write_text('{}')
        with self.assertRaisesRegex(u.UpdateError, 'Plugin-managed'):
            self.update()

    def test_remote_release_selection_missing_assets_prerelease_and_offline_failure(self):
        release = {'tag_name': 'v1.1.1', 'draft': False, 'prerelease': False,
                   'html_url': f'https://github.com/{u.REPO}/releases/tag/v1.1.1', 'assets': []}
        for suffix in ('.zip', '.zip.sha256'):
            name = u.NAME + '-1.1.1' + suffix
            release['assets'].append({'name': name, 'browser_download_url':
                f'https://github.com/{u.REPO}/releases/download/v1.1.1/{name}'})
        with patch.object(u, 'fetch', return_value=json.dumps(release).encode()) as fetch:
            self.assertEqual(u.release_info()['version'], '1.1.1')
            self.assertTrue(fetch.call_args[0][0].endswith('/releases/latest'))
        release['prerelease'] = True
        with patch.object(u, 'fetch', return_value=json.dumps(release).encode()):
            with self.assertRaisesRegex(u.UpdateError, 'prerelease excluded'):
                u.release_info()
        release['prerelease'] = False
        release['assets'].pop()
        with patch.object(u, 'fetch', return_value=json.dumps(release).encode()):
            with self.assertRaisesRegex(u.UpdateError, 'asset missing'):
                u.release_info()
        with patch.object(u, 'fetch', side_effect=OSError('network unavailable')):
            with patch('sys.stderr', new_callable=io.StringIO):
                self.assertEqual(u.main(['update', '--install-dir', str(self.installed)]), 1)
        self.assertEqual(u.fingerprint(self.installed), self.before)

    def test_symlink_target_is_rejected(self):
        link = self.base/'linked'
        try:
            link.symlink_to(self.installed, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            self.skipTest(str(error))
        with self.assertRaisesRegex(u.UpdateError, 'Symlink path'):
            u.locate(link)

    def test_network_check_reports_local_version_and_unknown_remote(self):
        with patch.object(u, 'fetch', side_effect=OSError('HTTP 403: rate limit exceeded')):
            with patch('sys.stdout', new_callable=io.StringIO) as output:
                self.assertEqual(u.main(['check', '--install-dir', str(self.installed)]), 1)
        result = json.loads(output.getvalue())
        self.assertEqual(result['version'], '1.0.0')
        self.assertEqual(result['remote_status'], 'error')
        self.assertIsNone(result['update_available'])
        self.assertEqual(u.fingerprint(self.installed), self.before)

    def test_bootstrap_cli_then_run_installed_updater_to_rollback_itself(self):
        (self.installed/'scripts/update_skill.py').unlink()
        (self.installed/'VERSION').unlink()
        (self.installed/'SHA256SUMS').unlink()
        old = u.fingerprint(self.installed)
        runner = SKILL/'scripts/update_skill.py'
        result = subprocess.run([sys.executable, str(runner), 'update', '--install-dir',
            str(self.installed), '--archive', str(self.archive), '--sha256', str(self.checksum),
            '--replace-local'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['version'], '1.1.1')
        result = subprocess.run([sys.executable, str(self.installed/'scripts/update_skill.py'),
            'rollback', '--install-dir', str(self.installed)], capture_output=True,
            text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(u.fingerprint(self.installed), old)

    def test_rate_limit_uses_existing_gh_without_exposing_credentials(self):
        for code in (403, 429):
            with self.subTest(code=code), patch.object(u, 'fetch', side_effect=HTTPError(u.API, code, 'limited', {}, None)), patch.object(u.shutil, 'which', return_value='/test/gh'), patch.dict(u.os.environ, {'GH_DEBUG': 'api'}), patch.object(u.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, b'{"tag_name":"v1.1.1"}')) as run:
                data, transport = u.release_metadata('/releases/latest')
                self.assertEqual(transport, 'gh-cli')
                self.assertEqual(data['tag_name'], 'v1.1.1')
                args, options = run.call_args
                self.assertEqual(args[0], ['/test/gh', 'api', '--hostname', 'github.com', '--method', 'GET', f'repos/{u.REPO}/releases/latest'])
                self.assertNotIn('GH_DEBUG', options['env'])
                self.assertEqual(options['env']['GH_PROMPT_DISABLED'], '1')
                self.assertEqual(options['stderr'], subprocess.DEVNULL)
                self.assertEqual(options['stdin'], subprocess.DEVNULL)
                self.assertNotIn('shell', options)

    def test_successful_anonymous_request_never_invokes_gh(self):
        with patch.object(u, 'fetch', return_value=b'{}'), patch.object(u.subprocess, 'run') as run:
            self.assertEqual(u.release_metadata('/releases/latest'), ({}, 'github-api'))
            run.assert_not_called()

    def test_non_rate_limit_error_never_invokes_gh(self):
        with patch.object(u, 'fetch', side_effect=HTTPError(u.API, 404, 'missing', {}, None)), patch.object(u.subprocess, 'run') as run:
            with self.assertRaises(HTTPError):
                u.release_metadata('/releases/tags/v9.9.9')
            run.assert_not_called()

    def test_missing_gh_preserves_installation(self):
        with patch.object(u, 'fetch', side_effect=HTTPError(u.API, 403, 'limited', {}, None)), patch.object(u.shutil, 'which', return_value=None):
            with patch('sys.stderr', new_callable=io.StringIO) as output:
                self.assertEqual(u.main(['update', '--install-dir', str(self.installed)]), 1)
            self.assertIn('optional gh CLI is unavailable', output.getvalue())
        self.assertEqual(u.fingerprint(self.installed), self.before)

    def test_gh_failure_and_timeout_do_not_echo_sensitive_process_output(self):
        for effect in (subprocess.CompletedProcess([], 1, b'sensitive-debug-output'), subprocess.TimeoutExpired(['gh'], 30, output=b'sensitive-debug-output')):
            with self.subTest(effect=type(effect).__name__), patch.object(u, 'fetch', side_effect=HTTPError(u.API, 403, 'limited', {}, None)), patch.object(u.shutil, 'which', return_value='/test/gh'):
                config = {'side_effect': effect} if isinstance(effect, Exception) else {'return_value': effect}
                with patch.object(u.subprocess, 'run', **config):
                    with self.assertRaises(u.UpdateError) as caught:
                        u.release_metadata('/releases/latest')
                    self.assertNotIn('sensitive-debug-output', str(caught.exception))
        self.assertEqual(u.fingerprint(self.installed), self.before)

    def test_invalid_gh_json_does_not_echo_output(self):
        with patch.object(u, 'fetch', side_effect=HTTPError(u.API, 429, 'limited', {}, None)), patch.object(u.shutil, 'which', return_value='/test/gh'), patch.object(u.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, b'sensitive-debug-output')):
            with self.assertRaisesRegex(u.UpdateError, '^gh returned invalid release metadata'):
                u.release_metadata('/releases/latest')

    def test_online_update_validates_release_version_and_both_checksums(self):
        archive_bytes = self.archive.read_bytes()
        release = {'version': '1.1.1', 'url': 'https://github.com/example/release',
                   'archive_name': self.archive.name,
                   'assets': {self.archive.name: 'archive', self.archive.name + '.sha256': 'checksum'}}
        def fetch(url, limit):
            return archive_bytes if url == 'archive' else self.checksum.read_bytes()
        with patch.object(u, 'fetch', fetch):
            result = u.update(self.installed, release=release)
        self.assertEqual(result['version'], '1.1.1')
        self.assertEqual(u.fingerprint(Path(result['backup_dir'])), self.before)


if __name__ == '__main__':
    unittest.main()
