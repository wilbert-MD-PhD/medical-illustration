#!/usr/bin/env python3
"""Build and verify the distributable Skill. MIT; see ../LICENSE-CODE."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REL = Path('plugins/medical-illustration/skills/medical-illustration')
NAME = 'medical-illustration'


def payload(root):
    paths = []
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError(f'Symlink in package: {p}')
        if '__pycache__' in p.parts or p.name == '.DS_Store' or p.suffix in ('.pyc', '.pyo'):
            continue
        if p.is_file() and p.name != 'SHA256SUMS':
            paths.append(p)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())


def hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in payload(root)}


def write_manifest(root):
    (root/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p, h in hashes(root).items()), encoding='utf-8')


def verify_manifest(root):
    expected = {}
    for line in (root/'SHA256SUMS').read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        if name in expected or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError(f'Invalid manifest entry: {name}')
        expected[name] = digest
    actual = hashes(root)
    if actual != expected:
        missing = sorted(set(expected)-set(actual))
        extra = sorted(set(actual)-set(expected))
        changed = sorted(p for p in actual.keys() & expected.keys() if actual[p] != expected[p])
        raise ValueError(f'Manifest mismatch: missing={missing}, extra={extra}, changed={changed}')
    return len(actual)


def check_links(root):
    for p in root.rglob('*.md'):
        if '.git' in p.parts:
            continue
        text = re.sub(r'```.*?```', '', p.read_text(encoding='utf-8'), flags=re.S)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            url = urlsplit(target.strip('<>'))
            if url.scheme or url.netloc or not url.path:
                continue
            dest = (p.parent/unquote(url.path)).resolve()
            if not dest.is_relative_to(root.resolve()) or not dest.exists():
                raise ValueError(f'Broken or external local link: {p}: {target}')


def check_skill(root):
    text = (root/'SKILL.md').read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError('Missing SKILL frontmatter')
    front = text.split('---', 2)[1]
    if not re.search(r'^name: medical-illustration$', front, re.M) or not re.search(r'^description: .+', front, re.M):
        raise ValueError('Invalid Skill name or description')
    ui = (root/'agents/openai.yaml').read_text(encoding='utf-8')
    if '$medical-illustration' not in ui:
        raise ValueError('Missing explicit invocation in UI prompt')
    version = (root/'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-rc\.\d+)?', version):
        raise ValueError('Invalid VERSION')
    script = (root/'scripts/init_medical_project.py').read_text(encoding='utf-8')
    if f'SKILL_VERSION = "{version}"' not in script:
        raise ValueError('Initializer version mismatch')
    check_links(root)
    count = verify_manifest(root)
    print(f'Skill {version}: {count} checksums and local links passed')
    return version


def check_repo(root):
    version = check_skill(root/REL)
    plugin = json.loads((root/'plugins/medical-illustration/.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    market = json.loads((root/'.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
    if plugin['version'] != version or plugin['name'] != NAME or plugin['skills'] != './skills/':
        raise ValueError('Plugin version/name/skills mismatch')
    entry = next(p for p in market['plugins'] if p['name'] == NAME)
    if (root/entry['source']['path']).resolve() != (root/'plugins/medical-illustration').resolve():
        raise ValueError('Marketplace source mismatch')
    check_links(root)
    return version


def verify_archive(archive, source=None):
    with tempfile.TemporaryDirectory(prefix='medical-release-') as tmp:
        with zipfile.ZipFile(archive) as z:
            seen = set()
            for item in z.infolist():
                name = item.filename
                p = PurePosixPath(name)
                if p.is_absolute() or '..' in p.parts or '\\' in name or not p.parts or p.parts[0] != NAME:
                    raise ValueError(f'Unsafe archive path: {name}')
                if name in seen or stat.S_ISLNK(item.external_attr >> 16):
                    raise ValueError(f'Duplicate or linked archive path: {name}')
                seen.add(name)
                if any(ord(c) > 127 for c in name) and not item.flag_bits & 0x800:
                    raise ValueError(f'Missing UTF-8 filename flag: {name!r}')
            bad = z.testzip()
            if bad:
                raise ValueError(f'CRC failure: {bad}')
            z.extractall(tmp)
        extracted = Path(tmp)/NAME
        check_skill(extracted)
        if source and hashes(extracted) != hashes(source):
            raise ValueError('Archive differs from source Skill')
    print(f'Archive round trip passed: {Path(archive).name}')


def build(root, output):
    version = check_repo(root)
    skill = root/REL
    output.mkdir(parents=True, exist_ok=True)
    archive = output/f'{NAME}-{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(payload(skill) + [skill/'SHA256SUMS'], key=lambda p: p.relative_to(skill).as_posix()):
            info = zipfile.ZipInfo(f'{NAME}/{p.relative_to(skill).as_posix()}', date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())  # zipfile sets UTF-8 bit for Unicode filenames.
    verify_archive(archive, skill)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output/f'{archive.name}.sha256').write_text(f'{checksum}  {archive.name}\n', encoding='utf-8')
    print(f'SHA256 {checksum}')
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['manifest', 'check', 'build', 'verify'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT/'dist')
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    if args.command == 'manifest':
        write_manifest(args.root/REL)
    elif args.command == 'check':
        check_repo(args.root)
    elif args.command == 'build':
        build(args.root, args.output)
    elif args.archive:
        verify_archive(args.archive, args.root/REL)
    else:
        parser.error('--archive is required for verify')


if __name__ == '__main__':
    main()
