#!/usr/bin/env python3
"""Check, update and roll back an installed medical-illustration Skill (Python 3.9+)."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import uuid
import zipfile

NAME = 'medical-illustration'
REPO = 'wilbert-MD-PhD/medical-illustration'
API = f'https://api.github.com/repos/{REPO}'
MAX_ARCHIVE = 25_000_000
MAX_EXPANDED = 100_000_000


class UpdateError(Exception):
    pass


def version_key(value):
    match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)(?:-rc\.(\d+))?', value or '')
    if not match:
        raise UpdateError(f'Unsupported version: {value!r}')
    major, minor, patch, rc = match.groups()
    return (int(major), int(minor), int(patch), 1 if rc is None else 0, int(rc or 0))


def safe_path(value):
    path = Path(os.path.abspath(Path(value).expanduser()))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise UpdateError(f'Symlink path is not supported: {part}')
    return path


def fingerprint(root, payload_only=False):
    result = {}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise UpdateError(f'Symlink in Skill: {p}')
        if p.is_dir():
            continue
        if not p.is_file():
            raise UpdateError(f'Non-regular file: {p}')
        if payload_only and (p == root/'SHA256SUMS' or '__pycache__' in p.parts or
                             p.name == '.DS_Store' or p.suffix in ('.pyc', '.pyo')):
            continue
        result[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def validate_identity(root):
    text = (root/'SKILL.md').read_text(encoding='utf-8')
    if not text.startswith('---\n') or not re.search(
            r'^name: medical-illustration\s*$', text.split('---', 2)[1], re.M):
        raise UpdateError(f'Not a medical-illustration Skill: {root}')


def manifest(root):
    expected = {}
    for line in (root/'SHA256SUMS').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([a-f0-9]{64})  (.+)', line)
        if not match:
            raise UpdateError('Invalid SHA256SUMS line')
        digest, name = match.groups()
        parts = PurePosixPath(name)
        if (parts.is_absolute() or '..' in parts.parts or '\\' in name or
                parts.as_posix() != name or name in expected or name == 'SHA256SUMS'):
            raise UpdateError(f'Invalid manifest path: {name}')
        expected[name] = digest
    return expected


def differences(expected, actual):
    return {kind: sorted(names) for kind, names in (
        ('missing', expected.keys() - actual.keys()),
        ('extra', actual.keys() - expected.keys()),
        ('changed', {p for p in expected.keys() & actual.keys() if expected[p] != actual[p]}))}


def local_info(root):
    validate_identity(root)
    actual = fingerprint(root, True)
    version_file = root/'VERSION'
    version = version_file.read_text(encoding='utf-8').strip() if version_file.exists() else None
    if version:
        version_key(version)
    try:
        delta = differences(manifest(root), actual)
        integrity = 'modified' if any(delta.values()) else 'clean'
    except (OSError, ValueError, UpdateError):
        integrity, delta = 'unknown', {}
    return {'install_dir': str(root), 'version': version, 'integrity': integrity,
            'differences': delta, 'legacy_install': version is None}


def validate_package(root, expected_version=None):
    validate_identity(root)
    version = (root/'VERSION').read_text(encoding='utf-8').strip()
    version_key(version)
    if expected_version and version != expected_version:
        raise UpdateError('Release tag and package VERSION differ')
    for name in ('README.md', 'LICENSE-CODE', 'LICENSE-CONTENT.md', 'NOTICE.md',
                 'agents/openai.yaml', 'scripts/init_medical_project.py'):
        if not (root/name).is_file():
            raise UpdateError(f'Incomplete package: {name}')
    if not (root/'references').is_dir():
        raise UpdateError('Incomplete package: references')
    installed_files = fingerprint(root)
    installed_files.pop('SHA256SUMS', None)
    if any(differences(manifest(root), installed_files).values()):
        raise UpdateError('Package SHA256SUMS mismatch')
    return version


def candidates():
    home = Path.home()
    paths = [Path(os.environ.get('CODEX_HOME', home/'.codex'))/'skills'/NAME,
             home/'.agents/skills'/NAME]
    for parent in (Path.cwd(), *Path.cwd().parents):
        paths.extend((parent/'.agents/skills'/NAME, parent/'.codex/skills'/NAME))
    return sorted({str(p.absolute()) for p in paths if (p/'SKILL.md').is_file()})


def locate(explicit):
    found = candidates()
    if explicit:
        return safe_path(explicit), found
    own = Path(__file__).resolve().parents[1]
    if (own/'SKILL.md').is_file() and str(own) not in found:
        found.append(str(own))
    if len(found) != 1:
        raise UpdateError('Select the actually loaded copy with --install-dir. Candidates: ' +
                          json.dumps(found, ensure_ascii=False))
    return safe_path(found[0]), found


def check_mutable(root):
    if root.name != NAME or not (root/'SKILL.md').is_file():
        raise UpdateError('Target must be an existing medical-illustration directory')
    if any((p/'.codex-plugin/plugin.json').exists() for p in (root, *root.parents)):
        raise UpdateError('Plugin-managed/source copy: use the host plugin updater or a standalone installation')
    if '/plugins/cache/' in root.as_posix() or (root/'.git').exists():
        raise UpdateError('Managed cache or Git checkout cannot be replaced by this updater')
    validate_identity(root)
    fingerprint(root)


def fetch(url, limit):
    if not url.startswith('https://'):
        raise UpdateError('HTTPS is required')
    request = Request(url, headers={'User-Agent': 'medical-illustration-updater',
                                   'Accept': 'application/vnd.github+json'})
    with urlopen(request, timeout=30) as response:
        if not response.geturl().startswith('https://'):
            raise UpdateError('Non-HTTPS redirect rejected')
        data = response.read(limit + 1)
    if len(data) > limit:
        raise UpdateError('Download exceeds size limit')
    return data


def release_metadata(endpoint):
    try:
        return json.loads(fetch(API + endpoint, 2_000_000)), 'github-api'
    except HTTPError as error:
        if error.code not in (403, 429):
            raise
        code = error.code
    gh = shutil.which('gh')
    if gh is None:
        raise UpdateError(f'GitHub API returned HTTP {code}; optional gh CLI is unavailable. Retry later or use an offline release package.')
    # Let gh use its existing credential store; never extract or print a token,
    # start login, run a shell, or enable gh HTTP debugging.
    env = os.environ.copy()
    env.pop('GH_DEBUG', None)
    env.pop('GH_FORCE_TTY', None)
    env.update(GH_PROMPT_DISABLED='1', GIT_TERMINAL_PROMPT='0')
    try:
        result = subprocess.run(
            [gh, 'api', '--hostname', 'github.com', '--method', 'GET',
             f'repos/{REPO}' + endpoint],
            env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise UpdateError(f'GitHub API returned HTTP {code}; existing gh session could not complete the request. Retry later or use an offline package.') from None
    if result.returncode != 0 or len(result.stdout) > 2_000_000:
        raise UpdateError(f'GitHub API returned HTTP {code}; existing gh session is unavailable or also limited. Sign in with gh separately, retry later, or use an offline package.')
    try:
        return json.loads(result.stdout), 'gh-cli'
    except (ValueError, UnicodeError):
        raise UpdateError('gh returned invalid release metadata; no installation changed') from None


def release_info(version=None, allow_prerelease=False):
    if version:
        version_key(version)
    endpoint = '/releases/tags/v' + version if version else '/releases/latest'
    data, metadata_source = release_metadata(endpoint)
    if not isinstance(data, dict):
        raise UpdateError('Invalid release metadata object')
    tag = data.get('tag_name', '')
    if not tag.startswith('v'):
        raise UpdateError('Release has no supported tag')
    remote = tag[1:]
    version_key(remote)
    if version and version != remote:
        raise UpdateError('Requested version and release differ')
    if data.get('draft') or ((data.get('prerelease') or '-rc.' in remote) and not allow_prerelease):
        raise UpdateError('Draft/prerelease excluded; select an RC explicitly with --version and --allow-prerelease')
    archive_name = f'{NAME}-{remote}.zip'
    urls = {}
    for name in (archive_name, archive_name + '.sha256'):
        matches = [a for a in data.get('assets', []) if a.get('name') == name]
        if len(matches) != 1:
            raise UpdateError(f'Release asset missing or duplicated: {name}')
        url = matches[0].get('browser_download_url', '')
        if not url.startswith(f'https://github.com/{REPO}/releases/download/{tag}/'):
            raise UpdateError('Unexpected release asset origin')
        urls[name] = url
    return {'version': remote, 'url': data.get('html_url'), 'archive_name': archive_name, 'assets': urls, 'metadata_source': metadata_source}


def unpack(archive, checksum, dest):
    # No archive-supplied Python is executed during validation or replacement.
    match = re.fullmatch(r'([a-fA-F0-9]{64})(?:[ \t]+\*?([^\r\n]+))?\s*', checksum.strip())
    if not match or (match[2] and match[2] != archive.name):
        raise UpdateError('Invalid checksum or checksum filename mismatch')
    if hashlib.sha256(archive.read_bytes()).hexdigest() != match[1].lower():
        raise UpdateError('Archive SHA-256 mismatch')
    with zipfile.ZipFile(archive) as z:
        seen, total = set(), 0
        for item in z.infolist():
            name = item.filename.rstrip('/')
            path = PurePosixPath(name)
            mode = item.external_attr >> 16
            reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {f'{prefix}{n}' for prefix in ('COM', 'LPT') for n in range(1, 10)}
            if (not name or path.is_absolute() or '..' in path.parts or '\\' in name or
                    ':' in name or path.as_posix() != name or path.parts[0] != NAME or
                    any(p.endswith((' ', '.')) or p.split('.')[0].upper() in reserved for p in path.parts) or
                    name.casefold() in seen or stat.S_ISLNK(mode) or
                    (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR))):
                raise UpdateError(f'Unsafe archive member: {item.filename}')
            seen.add(name.casefold())
            total += item.file_size
            if total > MAX_EXPANDED or len(seen) > 5000:
                raise UpdateError('Expanded archive exceeds limits')
        z.extractall(dest)
    return dest/NAME


def state_dir(root):
    # Outside the skills discovery directory; backups are never active copies.
    identity = hashlib.sha256(str(root).encode('utf-8')).hexdigest()[:16]
    return safe_path(root.parent.parent/'.medical-illustration-updates'/identity)


def write_json(path, data):
    temp = path.with_suffix('.tmp')
    with temp.open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


@contextmanager
def lock(state):
    state.mkdir(parents=True, exist_ok=True)
    marker = state/'lock'
    try:
        marker.mkdir()
    except FileExistsError:
        raise UpdateError(f'Update lock exists: {marker}. Inspect the previous process and transaction; do not delete an uncertain lock.')
    try:
        yield
    finally:
        # Incomplete restoration keeps a visible lock and all recovery material.
        if not (state/'recovery-required').exists():
            marker.rmdir()


def replace_install(root, staged, state, before, operation, source=None):
    transaction = state/uuid.uuid4().hex
    transaction.mkdir()
    previous = transaction/'previous'
    record = {'operation': operation, 'target': str(root), 'source': source,
              'before': before, 'after': fingerprint(staged), 'status': 'prepared'}
    record_path = transaction/'transaction.json'
    write_json(record_path, record)
    if fingerprint(root) != before:
        raise UpdateError('Installation changed during preparation; no replacement performed')
    moved = False
    try:
        root.rename(previous)
        moved = True
        staged.rename(root)
        if fingerprint(root) != record['after']:
            raise UpdateError('Post-install verification failed')
        record['status'] = 'committed'
        write_json(record_path, record)
    except BaseException:
        if moved:
            try:
                if root.exists():
                    root.rename(transaction/'failed-new-copy')
                previous.rename(root)
                if fingerprint(root) != before:
                    raise UpdateError('Restored copy differs from original')
                record['status'] = 'restored-after-failure'
                write_json(record_path, record)
            except BaseException:
                (state/'recovery-required').write_text(str(transaction), encoding='utf-8')
                raise UpdateError(f'Recovery needs attention; copies and lock retained at {transaction}')
        raise
    return {'status': operation + '_complete', 'install_dir': str(root),
            'backup_id': transaction.name, 'backup_dir': str(previous),
            'host_reload': 'required; disk verification does not prove the host loaded this copy'}


def update(root, release=None, archive=None, checksum=None, replace_local=False):
    check_mutable(root)
    state = state_dir(root)
    with lock(state):
        before = fingerprint(root)
        info = local_info(root)
        if (info['integrity'] != 'clean' or info['legacy_install']) and not replace_local:
            raise UpdateError('Local edits or unknown legacy baseline; inspect check output. Use --replace-local only after explicitly choosing backup-and-replace; nothing is overwritten.')
        with tempfile.TemporaryDirectory(prefix='stage-', dir=state) as tmp:
            stage = Path(tmp)
            if archive is None:
                if release is None:
                    release = release_info()
                archive = stage/release['archive_name']
                checksum = fetch(release['assets'][archive.name + '.sha256'], 4096).decode('utf-8')
                archive.write_bytes(fetch(release['assets'][archive.name], MAX_ARCHIVE))
            else:
                archive = safe_path(archive)
                if archive.stat().st_size > MAX_ARCHIVE:
                    raise UpdateError('Archive exceeds size limit')
                checksum = safe_path(checksum).read_text(encoding='utf-8')
            staged = unpack(archive, checksum, stage/'unpacked')
            new_version = validate_package(staged, release['version'] if release else None)
            if info['version'] and version_key(new_version) < version_key(info['version']):
                raise UpdateError('Downgrade refused; use rollback to restore a recorded backup')
            if fingerprint(staged, True) == fingerprint(root, True):
                return {'status': 'already_current', 'install_dir': str(root), 'version': new_version}
            result = replace_install(root, staged, state, before, 'update',
                                     release['url'] if release else str(archive))
            result['version'] = new_version
            return result


def history(root):
    result = []
    state = state_dir(root)
    if not state.exists():
        return result
    for p in state.glob('*/transaction.json'):
        p = safe_path(p)
        data = json.loads(p.read_text(encoding='utf-8'))
        if data.get('target') == str(root) and data.get('status') == 'committed':
            result.append((p.stat().st_mtime_ns, p.parent.name, data))
    return sorted(result, reverse=True)


def rollback(root, backup_id=None, replace_local=False):
    check_mutable(root)
    state = state_dir(root)
    with lock(state):
        records = history(root)
        if backup_id:
            records = [r for r in records if r[1] == backup_id]
        if not records:
            raise UpdateError('No matching committed backup')
        _, selected, record = records[0]
        before = fingerprint(root)
        latest = history(root)[0][2]
        if before != latest['after'] and not replace_local:
            raise UpdateError('Installed files changed after the last operation; back up and review before --replace-local')
        previous = safe_path(state/selected/'previous')
        if fingerprint(previous) != record['before']:
            raise UpdateError('Backup missing or modified; rollback refused')
        with tempfile.TemporaryDirectory(prefix='rollback-', dir=state) as tmp:
            staged = Path(tmp)/NAME
            shutil.copytree(previous, staged)
            validate_identity(staged)  # A legitimate legacy backup may lack VERSION/SHA256SUMS.
            return replace_install(root, staged, state, before, 'rollback', selected)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(errors='backslashreplace')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'update', 'rollback'])
    parser.add_argument('--install-dir', type=Path, help='Actually loaded standalone Skill directory')
    parser.add_argument('--offline', action='store_true', help='Check local state without networking')
    parser.add_argument('--version', help='Explicit release version, e.g. 1.1.2')
    parser.add_argument('--allow-prerelease', action='store_true')
    parser.add_argument('--archive', type=Path, help='Offline update using a complete release ZIP')
    parser.add_argument('--sha256', type=Path, help='Matching local checksum file')
    parser.add_argument('--replace-local', action='store_true', help='Explicitly back up and replace local edits; no automatic merge')
    parser.add_argument('--backup', help='Rollback to a backup ID from check output (default: latest)')
    args = parser.parse_args(argv)
    try:
        if bool(args.archive) != bool(args.sha256):
            raise UpdateError('--archive and --sha256 must be supplied together')
        if args.allow_prerelease and not args.version:
            raise UpdateError('--allow-prerelease requires an explicit --version')
        if args.command != 'update' and (args.archive or args.sha256):
            raise UpdateError('Archive options are only supported for update')
        if args.offline and args.command == 'update' and not args.archive:
            raise UpdateError('Offline update requires --archive and --sha256')
        if args.archive and args.version:
            raise UpdateError('Use either a local archive or a remote version')
        root, found = locate(args.install_dir)
        if args.command == 'check':
            result = local_info(root)
            result['candidates'] = found
            result['backups'] = [{'id': r[1], 'operation': r[2]['operation']} for r in history(root)]
            result['host_loaded_version'] = 'unverified'
            if not args.offline:
                try:
                    release = release_info(args.version, args.allow_prerelease)
                except (UpdateError, OSError, ValueError, KeyError) as error:
                    result.update(remote_status='error', remote_error=str(error), update_available=None)
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                    return 1
                result['release'] = release
                result['remote_status'] = 'checked'
                result['update_available'] = (version_key(release['version']) > version_key(result['version'])
                                              if result['version'] else None)
            else:
                result['remote_status'] = 'not_checked'
        elif args.command == 'update':
            release = None if args.archive else release_info(args.version, args.allow_prerelease)
            result = update(root, release, args.archive, args.sha256, args.replace_local)
        else:
            result = rollback(root, args.backup, args.replace_local)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (UpdateError, OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        print(json.dumps({'status': 'error', 'message': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
