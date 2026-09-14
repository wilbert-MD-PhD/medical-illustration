#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for initialization behavior. MIT License; see ../LICENSE-CODE."""

from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("init_medical_project.py")


class InitializeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="medical-skill-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "中文 空格项目"

    def run_init(self, output_encoding="utf-8", arguments=None):
        arguments = [str(self.root)] if arguments is None else arguments
        command = [sys.executable, "-I", "-X", "utf8"]
        if output_encoding == "utf-8":
            command += [str(SCRIPT.resolve())] + arguments
        else:
            wrapper = (
                "import sys,runpy; "
                f"sys.stdout.reconfigure(encoding={output_encoding!r},errors='strict'); "
                f"sys.stderr.reconfigure(encoding={output_encoding!r},errors='strict'); "
                "sys.argv=sys.argv[1:]; "
                "runpy.run_path(sys.argv[0],run_name='__main__')"
            )
            command += ["-c", wrapper, str(SCRIPT.resolve())] + arguments
        return subprocess.run(
            command, cwd=self.base, capture_output=True, text=True,
            encoding=output_encoding,
        )

    def test_non_utf8_success_keeps_utf8_files(self):
        for encoding in ("cp1252", "ascii", "gbk"):
            with self.subTest(encoding=encoding):
                self.root = self.base / (encoding + " 中文项目")
                result = self.run_init(encoding)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout)
                self.assertFalse(result.stderr)
                content = (self.root / "00_项目规范/项目说明.md").read_text(encoding="utf-8")
                self.assertIn("项目名称", content)

    def test_non_utf8_repeat_preserves_user_content(self):
        for encoding in ("cp1252", "ascii", "gbk"):
            with self.subTest(encoding=encoding):
                self.root = self.base / (encoding + " 中文项目")
                self.assertEqual(self.run_init(encoding).returncode, 0)
                target = self.root / "00_项目规范/项目说明.md"
                target.write_text("人工内容：保持原样", encoding="utf-8")
                before = self.snapshot()
                result = self.run_init(encoding)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_non_utf8_error_reports_without_traceback(self):
        self.root.mkdir()
        (self.root / "07_审计记录").write_text("保留", encoding="utf-8")
        for encoding in ("cp1252", "ascii", "gbk"):
            with self.subTest(encoding=encoding):
                result = self.run_init(encoding)
                self.assertEqual(result.returncode, 1)
                self.assertTrue(result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn("SyntaxError", result.stderr)
                self.assertIn("初始化失败".encode(encoding, errors="backslashreplace").decode(encoding), result.stderr)
                self.assertEqual(list(self.root.iterdir()), [self.root / "07_审计记录"])

    def test_non_utf8_argparse_output(self):
        for encoding in ("cp1252", "ascii", "gbk"):
            with self.subTest(encoding=encoding):
                help_result = self.run_init(encoding, ["--help"])
                self.assertEqual(help_result.returncode, 0, help_result.stderr)
                self.assertIn("project_dir", help_result.stdout)
                error_result = self.run_init(encoding, [])
                self.assertEqual(error_result.returncode, 2)
                self.assertTrue(error_result.stderr)
                self.assertNotIn("Traceback", error_result.stderr)
                self.assertFalse(self.root.exists())

    def snapshot(self):
        return {
            str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.root.rglob("*") if path.is_file()
        }

    def assert_failed_without_writes(self, before):
        result = self.run_init()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("初始化失败", result.stderr)
        self.assertNotIn("SyntaxError", result.stderr)
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*")))

    def test_create_and_retain_user_edits(self):
        first = self.run_init()
        self.assertEqual(first.returncode, 0, first.stderr)
        edited = self.root / "00_项目规范/项目说明.md"
        edited.write_text(edited.read_text(encoding="utf-8") + "\n用户填写：保留\n", encoding="utf-8")
        extra = self.root / "用户额外记录.txt"
        extra.write_text("不要覆盖", encoding="utf-8")
        before = self.snapshot()
        repeated = self.run_init()
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(before, self.snapshot())

    def test_restore_one_missing_template(self):
        self.assertEqual(self.run_init().returncode, 0)
        before = self.snapshot()
        missing = self.root / "01_证据/医学事实与来源.md"
        missing.unlink()
        self.assertEqual(self.run_init().returncode, 0)
        self.assertEqual(before, self.snapshot())

    def test_new_templates_carry_license_and_version(self):
        self.assertEqual(self.run_init().returncode, 0)
        templates = list(self.root.rglob("*.md"))
        self.assertTrue(templates)
        for path in templates:
            content = path.read_text(encoding="utf-8")
            self.assertIn("wilbert", content)
            self.assertIn("https://creativecommons.org/licenses/by-nc-sa/4.0/", content)
        notice = self.root / "00_项目规范/模板来源与许可说明.md"
        version = SCRIPT.parent.parent.joinpath("VERSION").read_text().strip()
        self.assertIn(version, notice.read_text(encoding="utf-8"))

    def test_directory_at_template_path_is_error_before_writes(self):
        (self.root / "07_审计记录/问题与变更.md").mkdir(parents=True)
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        self.assert_failed_without_writes(before)

    def test_file_at_directory_path_is_error_before_writes(self):
        self.root.mkdir()
        (self.root / "07_审计记录").write_text("保留", encoding="utf-8")
        self.assert_failed_without_writes(["07_审计记录"])

    def make_link(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"当前环境不支持创建符号链接: {error}")

    def test_external_directory_link_is_rejected(self):
        self.root.mkdir()
        outside = self.base / "外部目录"
        outside.mkdir()
        self.make_link(self.root / "00_项目规范", outside, directory=True)
        self.assert_failed_without_writes(["00_项目规范"])
        self.assertEqual(list(outside.iterdir()), [])

    def test_dangling_template_link_is_rejected(self):
        parent = self.root / "00_项目规范"
        parent.mkdir(parents=True)
        outside = self.base / "不得创建.txt"
        self.make_link(parent / "项目说明.md", outside)
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        self.assert_failed_without_writes(before)
        self.assertFalse(outside.exists())

    def test_root_file_is_preserved(self):
        self.root.write_text("根路径已有文件", encoding="utf-8")
        result = self.run_init()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("初始化失败", result.stderr)
        self.assertEqual(self.root.read_text(encoding="utf-8"), "根路径已有文件")


if __name__ == "__main__":
    unittest.main(verbosity=2)
