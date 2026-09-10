# 维护与发布

仓库根保留 Marketplace；插件根为 `plugins/medical-illustration/`，唯一 Skill 源为其下 `skills/medical-illustration/`。独立目录和可选 ZIP 都从这一份源构建，不从个人安装目录临时打包。

## 本地检查

版本变化同步 VERSION、初始化器 SKILL_VERSION、plugin.json、安装和发布说明。双语主页面向首次访问者，只介绍用途、效果、参考使用和上手方法；版本新增、修复和迁移信息集中到 Release 文案。然后运行：

```bash
python3 scripts/release.py manifest
python3 scripts/release.py check
python3 plugins/medical-illustration/skills/medical-illustration/scripts/test_init_medical_project.py
python3 scripts/test_release.py
python3 scripts/release.py build
git diff --check
```

默认输出 `dist/medical-illustration/` 普通目录，已有目标会拒绝覆盖；清单与内容不一致时不会自动修复。更换 `--output` 可建立新批次；输出必须位于 Skill 源目录之外，指向源目录内部的真实路径或符号链接均在写入前拒绝。确需 ZIP 时显式执行 `python3 scripts/release.py build --format zip --output /path/to/new-output`。ZIP 使用稳定时间戳与 UTF-8 文件名，构建后验证解压及哈希；回归测试仅在临时目录验证 ZIP。

公开示例修改后重新导出并逐图检查，主页修改后检查中英文渲染和链接。退役示例不进入主页、Skill 载荷或发布附件；发布检查会拒绝重新带入已排除的示例目录。归档与旧构建仅留在仓库外。Illustrator 辅助库须另做宿主验收，不能以其他排版工具或漫画专用脚本的结果代替。

## 发布到 GitHub

1. 再次核对远端 main 和版本标签；先处理新增改动，不覆盖远端历史。
2. 检查 diff，提交本目录修改，推送并等待当前提交的 Validate CI。
3. 确认本次明确要创建 GitHub Release 及 ZIP 附件后，在同一提交创建与 VERSION 一致的 `v<版本>` 标签并推送。
4. Release 工作流验证标签、三平台测试后，显式选择 ZIP 构建并创建 Release，再下载附件校验。

本地整理不自动提交、推送、打标签或发布。不要移动既有版本标签。若后续不需要 ZIP 附件，应先调整 Release 工作流再推标签；普通分支推送只运行验证。

保持上一代许可与来源声明；不加入患者资料、书库原件、私有角色、认证数据、字体二进制或机器绝对路径。历史展示文件只在来源和范围明确时保留，过时样式标为历史。
