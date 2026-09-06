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


SKILL_VERSION = "1.0.0-rc.3"

TEMPLATE_NOTICE = (
    "\n---\n模板来源：medical-illustration；作者：wilbert；"
    "许可：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)。\n"
    "模板原文由初始化脚本复制；后续修改请记录。此声明适用于复制的模板内容，"
    "不自动覆盖使用者新增内容或独立创作作品。\n"
)

DIRECTORIES = [
    "00_项目规范",
    "01_证据/文献PDF",
    "01_证据/解剖参考图",
    "01_证据/授权记录",
    "02_人物母版/转面图",
    "02_人物母版/标准姿势",
    "02_人物母版/患者角色",
    "03_医学母版/解剖图",
    "03_医学母版/查体动作",
    "03_医学母版/医疗器械",
    "03_医学母版/医学影像",
    "04_脚本与分配表",
    "04_脚本与分配表/Prompt与渲染清单",
    "04_脚本与分配表/返修编辑合同",
    "05_线稿审校",
    "06_彩稿与排版",
    "07_审计记录",
    "08_印前文件",
    "99_废弃版本",
]

FILES = {
    "00_项目规范/项目说明.md": """# 项目说明

- 项目名称：
- 目标受众：
- 载体与开本：
- 交付载体：印刷 / 数字 / 未定
- 制作阶段：启动
- 印刷书面规格：印刷交付前确认；数字作品不适用
- 数字输出规格：目标平台、像素尺寸、显示尺寸、色彩、格式；初稿可暂定
- 项目负责人：
- 临床审稿人：
- 解剖审稿人：
- 当前状态：草稿
""",
    "00_项目规范/术语表.md": """# 术语表

| 中文标准名 | 英文/缩写 | 公众推荐说法 | 首次解释 | 禁用或易误导说法 | 证据编号 |
|---|---|---|---|---|---|
""",
    "01_证据/证据矩阵.md": """# 证据矩阵

| ID | 页面 | 拟表达结论 | 完整文献信息 | DOI/PMID/URL | 具体页/图/段 | 支持范围 | 绘图影响 | 核验范围 | 审核人 | 状态 |
|---|---:|---|---|---|---|---|---|---|---|---|
""",
    "01_证据/授权记录/素材授权台账.md": """# 素材授权台账

| 资产ID | 文件 | 标题/描述 | 作者/机构 | 原始URL | 下载日期 | 具体许可证 | 署名原文 | 修改说明 | 肖像/患者授权 | 可商用核验 | 经办人 |
|---|---|---|---|---|---|---|---|---|---|---|---|
""",
    "01_证据/解剖参考图/参考图登记表.md": """# 解剖参考图登记表

| 参考图ID | 本地文件 | 解剖区域 | 标题/描述 | 作者/机构 | 原始URL或书目/机构来源 | 取得或访问日期 | 来源类型 | 侧别/视角/层次 | 具体页/图号 | 许可证/使用范围 | 解剖约束 | 核验人 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
""",
    "04_脚本与分配表/页面清单.md": """# 页面清单

| 页码 | 唯一认知目标 | 图像类型 | 风险 H/M/L | 证据编号 | 解剖参考图 | 角色资产 | 医学母版 | 规格卡 | Prompt/渲染清单 | 审核人 | 状态 |
|---:|---|---|---|---|---|---|---|---|---|---|---|
""",
    "04_脚本与分配表/Prompt与渲染清单/模板.md": """# 标准 prompt

- 页面/图号：
- 用途与唯一认知目标：
- 画布与实际阅读尺寸：
- 场景与主体：
- 视角、镜头与构图：
- 人物、动作与角色资产：
- 医学空间规格：
- 解剖参考图与医学母版：
- 风格、色彩、光线与媒介：
- 锁定项：
- 允许变化项：
- 禁止项：
- 分层与无文底图要求：

# 渲染清单

- 标准 prompt 版本：
- 模型适配版：
- 模型/版本：
- 尺寸/质量/seed：
- 输入图及用途：
- 资产版本或哈希：
- 输出文件：
- 审核状态：
""",
    "04_脚本与分配表/返修编辑合同/模板.md": """# 返修编辑合同

- 页面/对象：
- 修改类型：医学事实层 / 非医学表现层 / 文字层
- 基准版本：
- 本次唯一变更集：
- 允许变化：
- 必须保持不变：
- 修改区/蒙版：
- 保护区/锁定图层：
- 母版、参考图和资产编号：
- 允许工具：
- 验收条件：
- 失败后回退方式：
""",
    "04_脚本与分配表/气泡排字记录.md": """# 气泡排字记录

| 气泡ID | 页码 | 成书尺寸 | 安全区/内边距 | 字体/字重 | 字号/下限 | 行距/行数 | 尾巴排除 | 换行 | 溢出 | 处理结果 | 审核人 |
|---|---|---|---|---|---|---|---|---|---|---|---|
""",
    "04_脚本与分配表/文案语义回归表.md": """# 文案语义回归表

| 页面/句号 | 医学事实稿 | 公众表达稿 | 事实/条件/否定 | 数值/时序 | 概率与强度 | 风险与行动建议 | 图文一致 | 结论 | 审核人 |
|---|---|---|---|---|---|---|---|---|---|

结论只使用：含义不变、退回修改、需更新证据并重审。
""",
    "07_审计记录/版本变更表.md": """# 版本变更表

| 日期 | 文件/页码 | 原版本 | 新版本 | 变更内容 | 影响范围 | 是否重审 | 审核人 |
|---|---|---|---|---|---|---|---|
""",
    "07_审计记录/问题清单.md": """# 问题清单

| ID | 等级 A/B/C | 页面/图号 | 对象 | 问题 | 修改要求 | 回归范围 | 负责人 | 状态 |
|---|---|---|---|---|---|---|---|---|
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
