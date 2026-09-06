#!/usr/bin/env python3
"""Release boundary regression tests. MIT; see ../LICENSE-CODE."""
import importlib.util
import shutil
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET
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
        a = release.build(release.ROOT, self.base/'a')
        b = release.build(release.ROOT, self.base/'b')
        self.assertEqual(a.read_bytes(), b.read_bytes())
        with zipfile.ZipFile(a) as z:
            name = 'medical-illustration/examples/generic-visit-preparation/示例说明.md'
            self.assertTrue(z.getinfo(name).flag_bits & 0x800)
            self.assertIn('通用示例', z.read(name).decode('utf-8'))

    def test_lettering_preserves_protected_artwork_and_editable_text(self):
        folder = release.ROOT/release.REL/'examples/editable-lettering'
        base = ET.parse(folder/'base.svg').getroot()
        lettered = ET.parse(folder/'lettered.svg').getroot()
        for group in ('background', 'artwork', 'review'):
            self.assertEqual(ET.tostring(base.find(f".//*[@id='{group}']")), ET.tostring(lettered.find(f".//*[@id='{group}']")))
        ns = {'s': 'http://www.w3.org/2000/svg'}
        self.assertGreater(len(lettered.findall('.//s:text', ns)), len(base.findall('.//s:text', ns)))
        self.assertFalse(lettered.findall('.//s:image', ns))

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
