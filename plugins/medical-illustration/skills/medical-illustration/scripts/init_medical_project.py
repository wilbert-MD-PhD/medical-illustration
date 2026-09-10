#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a non-destructive medical-illustration project scaffold."""

# License boundary:
# - Executable Python code in this file: MIT License (see ../LICENSE-CODE).
# - The DIRECTORIES, FILES and TEMPLATE_NOTICE content below: CC BY-NC-SA 4.0
#   (see ../LICENSE-CONTENT.md). Generated copies are not relicensed merely
#   because the MIT-licensed code writes them to disk.

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SKILL_VERSION = "1.0.0"

TEMPLATE_NOTICE = (
    "\n---\n模板来源：medical-illustration；作者：wilbert；"
    "许可：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)。\n"
    "模板原文由初始化脚本复制；后续修改请记录。此声明适用于复制的模板内容，"
    "不自动覆盖使用者新增内容或独立创作作品。\n"
)

DIRECTORIES = ['00_项目规范', '01_证据', '04_脚本与分配表', '06_彩稿与排版', '07_审计记录']

FILES = {
    '00_项目规范/项目说明.md': """# 项目说明

- 项目名称：
- 读者与项目目标：
- 当前主稿与视觉/角色基准：
- 工作规格与出版规格状态：
- 制作进度与人工审签状态（分别记录）：

唯一画面、调用记录及制作工具保存在正式目录；临时目录只存可重建文件。默认交付普通文件夹和文件链接，不自动压缩。
""",
    '01_证据/医学事实与来源.md': """# 医学事实与来源

按事实 ID 记录论断、来源、定位、支持范围和使用页面。

## 解剖图像来源与许可

每个实际图版/模型版本一条，含人工核对及上游来源。记录原作者/作品/版本/URL/图号/双页码、本地文件与哈希、医学支持范围、具体许可及凭据、各用途核验、实际调用链接和输入输出映射、修改与拟刊署名。共享凭据链接引用，同源多页合并。
""",
    '04_脚本与分配表/页面清单.md': """# 页面清单

| 页面 ID | 读者问题与视觉重点 | 当前脚本 | 来源/角色版本 | 生成记录 | 当前画面与检查状态 |
|---|---|---|---|---|---|

生图前记录实际可见文字、首页标题、各对白位置与预计行数；底图只留背景空间，不画气泡。生成后先按正常字号试排，再制作可编辑气泡、文字和标签。
""",
    '07_审计记录/问题与变更.md': """# 问题与变更

| 页面/版本 | 问题与检查类别 | 修改目标和影响范围 | 新版及复核结论 | 人工意见凭据（如有） |
|---|---|---|---|---|

制作、美术/编辑、医学图文对照、人工审签和印前状态分别记录。
""",
}

FILES["00_项目规范/模板来源与许可说明.md"] = """# 模板来源与许可说明

- 来源：medical-illustration，版本：""" + SKILL_VERSION + """。
- 作者：wilbert；Copyright © 2026 wilbert。
- 复制的文字模板采用 CC BY-NC-SA 4.0：
  https://creativecommons.org/licenses/by-nc-sa/4.0/
- 完整法律文本：https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
- 分享或改作这些模板内容时，保留署名、许可链接，标明修改并遵守非商业及相同方式共享条件；商业授权须另行取得。
- 初始化器可执行代码采用 MIT；代码许可不改变文字模板许可。
- 使用流程创作的新插画、漫画或文档不自动继承模板许可；实际复制的模板内容和纳入的第三方素材仍按各自许可处理。
- 脚本不覆盖已有文件，也不自动为已有模板补写署名。迁移旧项目时，请在分发复制的模板内容前核对来源声明。
- 修改记录：初始化为原模板副本；后续修改由使用者记录。
"""


def validate_path(root: Path, target: Path, *, directory: bool) -> None:
    """Reject conflicting types and symlinks below the selected project root."""
    if root.exists() and not root.is_dir():
        raise ValueError(f"项目根路径不是目录: {root}")
    relative = target.relative_to(root)
    current = root
    for index, part in enumerate(relative.parts):
        current = current / part
        if current.is_symlink():
            raise ValueError(f"项目内路径不能是符号链接: {current}")
        wants_dir = directory or index < len(relative.parts) - 1
        if current.exists() and not (current.is_dir() if wants_dir else current.is_file()):
            expected = "目录" if wants_dir else "普通文件"
            raise ValueError(f"路径类型冲突，应为{expected}: {current}")


def initialize(root: Path) -> tuple[int, int, int]:
    # Inspect every planned path before creating anything. Explicit root aliases
    # are resolved by main(); nested symlinks are rejected, even when dangling.
    for relative in DIRECTORIES:
        validate_path(root, root / relative, directory=True)
    for relative in FILES:
        validate_path(root, root / relative, directory=False)

    root.mkdir(parents=True, exist_ok=True)
    created_dirs = created_files = skipped_files = 0
    for relative in DIRECTORIES:
        target = root / relative
        validate_path(root, target, directory=True)
        if not target.exists():
            created_dirs += 1
        target.mkdir(parents=True, exist_ok=True)

    for relative, content in FILES.items():
        target = root / relative
        validate_path(root, target, directory=False)
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Exclusive creation also preserves a file created since preflight.
            with target.open("x", encoding="utf-8") as output:
                output.write(content + TEMPLATE_NOTICE)
        except FileExistsError:
            validate_path(root, target, directory=False)
            skipped_files += 1
        else:
            created_files += 1
    return created_dirs, created_files, skipped_files


def main() -> int:
    # Preserve the caller's encoding; escape characters it cannot represent.
    # Configure before argparse so help and error messages are covered too.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(
        description="创建医学科普插画项目目录；保留已有文件，拒绝类型冲突与项目内符号链接。"
    )
    parser.add_argument("project_dir", type=Path, help="目标项目目录")
    args = parser.parse_args()
    try:
        root = args.project_dir.expanduser().resolve()
        created_dirs, created_files, skipped_files = initialize(root)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"初始化失败: {error}", file=sys.stderr)
        return 1

    print(f"项目目录: {root}")
    print(f"新建目录: {created_dirs}")
    print(f"新建模板: {created_files}")
    print(f"跳过已有模板: {skipped_files}")
    if skipped_files:
        print("已有文件未修改；分发旧模板前请核对模板来源与许可说明。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
