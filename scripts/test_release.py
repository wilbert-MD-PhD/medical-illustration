#!/usr/bin/env python3
"""Release boundary regression tests. MIT; see ../LICENSE-CODE."""
import importlib.util
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('release', Path(__file__).with_name('release.py'))
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def test_unicode_roundtrip_and_reproducible_build(self):
        root = self.base/'fixture-repo'
        for folder in ('plugins', '.agents'):
            shutil.copytree(release.ROOT/folder, root/folder)
        fixture = root/release.REL/'测试资料/中文说明.md'
        fixture.parent.mkdir()
        fixture.write_text('中文文件往返校验', encoding='utf-8')
        release.write_manifest(root/release.REL)
        a = release.build(root, self.base/'a', 'zip')
        b = release.build(root, self.base/'b', 'zip')
        self.assertEqual(a.read_bytes(), b.read_bytes())
        with zipfile.ZipFile(a) as z:
            name = 'medical-illustration/测试资料/中文说明.md'
            self.assertTrue(z.getinfo(name).flag_bits & 0x800)
            self.assertEqual('中文文件往返校验', z.read(name).decode('utf-8'))

    def test_retired_examples_cannot_be_published(self):
        root = self.base/'repository'
        for name in release.RETIRED_EXAMPLES:
            folder = root/release.REL/'examples'/name
            folder.mkdir(parents=True)
            for format in ('directory', 'zip'):
                with self.subTest(name=name, format=format):
                    output = self.base/'blocked-output'
                    with self.assertRaisesRegex(ValueError, 'Retired example'):
                        release.build(root, output, format)
                    self.assertFalse(output.exists())
            folder.rmdir()

    def test_default_build_is_directory_and_preserves_existing_delivery(self):
        directory = release.build(release.ROOT, self.base/'dist')
        self.assertTrue(directory.is_dir())
        self.assertFalse(list(self.base.rglob('*.zip')))
        self.assertEqual(release.hashes(directory), release.hashes(release.ROOT/release.REL))
        marker = directory/'user-notes.txt'
        marker.write_text('keep', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            release.build(release.ROOT, self.base/'dist')
        self.assertEqual(marker.read_text(encoding='utf-8'), 'keep')

    def test_nested_output_is_rejected_without_modifying_source(self):
        root = self.base/'repository'
        skill = root/release.REL
        shutil.copytree(release.ROOT/release.REL, skill)
        before = release.hashes(skill)
        for format in ('directory', 'zip'):
            with self.subTest(format=format):
                for output in (skill, skill/'build-output'):
                    with self.assertRaisesRegex(ValueError, 'outside the source'):
                        release.build(root, output, format)
                    self.assertEqual(release.hashes(skill), before)
                    self.assertFalse((skill/'build-output').exists())

    def test_output_alias_into_source_is_rejected(self):
        root = self.base/'repository'
        skill = root/release.REL
        shutil.copytree(release.ROOT/release.REL, skill)
        alias = self.base/'output-alias'
        try:
            alias.symlink_to(skill, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f'Symlinks unavailable: {error}')
        before = release.hashes(skill)
        for format in ('directory', 'zip'):
            with self.subTest(format=format):
                with self.assertRaisesRegex(ValueError, 'outside the source'):
                    release.build(root, alias/'new-output', format)
        self.assertEqual(release.hashes(skill), before)
        self.assertFalse((skill/'new-output').exists())

    def test_old_style_unmarked_unicode_is_rejected(self):
        archive = self.base/'old.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('medical-illustration/示例.md', 'example')
        # Simulate the rc.2 writer: UTF-8 bytes with the flag cleared in both headers.
        data = bytearray(archive.read_bytes())
        for sig, offset in [(b'PK\x03\x04', 6), (b'PK\x01\x02', 8)]:
            pos = data.index(sig) + offset
            flags = int.from_bytes(data[pos:pos+2], 'little') & ~0x800
            data[pos:pos+2] = flags.to_bytes(2, 'little')
        archive.write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'UTF-8'):
            release.verify_archive(archive)

    def test_nested_manifest_named_file_cannot_bypass_integrity(self):
        skill = self.base/'skill'
        shutil.copytree(release.ROOT/release.REL, skill)
        nested = skill/'scripts/SHA256SUMS'
        nested.write_text('undeclared extra file', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Manifest mismatch'):
            release.verify_manifest(skill)
        release.write_manifest(skill)
        self.assertIn('scripts/SHA256SUMS', release.hashes(skill))
        release.verify_manifest(skill)
        nested.write_text('modified after manifest', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Manifest mismatch'):
            release.verify_manifest(skill)

    def test_corrupted_content_is_rejected(self):
        skill = self.base/'skill'
        shutil.copytree(release.ROOT/release.REL, skill)
        (skill/'VERSION').write_text('0.0.0\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Manifest mismatch'):
            release.verify_manifest(skill)

    def test_archive_traversal_is_rejected(self):
        archive = self.base/'unsafe.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('medical-illustration/../../escaped', 'bad')
        with self.assertRaisesRegex(ValueError, 'Unsafe archive path'):
            release.verify_archive(archive)
        self.assertFalse((self.base/'escaped').exists())

    def test_broken_link_is_rejected(self):
        (self.base/'README.md').write_text('[missing](missing.svg)', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Broken'):
            release.check_links(self.base)


if __name__ == '__main__':
    unittest.main(verbosity=2)
