# 安装、依赖与更新

安装完整 `medical-illustration/` 文件夹，包括 SKILL、references、scripts、agents、示例及许可；只复制 SKILL.md 会缺少资源。本 Skill 是工作流程，不捆绑图像模型、医学图谱、字体二进制或商业软件许可证。

## 对话安装

V1.0 标签发布后，可在支持 Skill 安装的 Codex 中发送：

```text
请使用 $skill-installer 安装：
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.0.0/plugins/medical-illustration/skills/medical-illustration
先核对实际技能目录，保留已有同名版本的本地改动，避免重复安装。
安装后读取 references/first-run.md，按当前任务检查所需制作能力。
```

个人安装路径依实际环境而定：以当前技能目录或安装器返回路径为准，不同时向多个位置复制同名版本。项目级目录可由宿主配置为 `.agents/skills/medical-illustration/`。安装后下一轮显式调用；未被发现时按宿主刷新或重启。文件可读不等于已验证自动发现。

手动安装时，从仓库 `plugins/medical-illustration/skills/medical-illustration/` 或本地独立构建目录复制完整文件夹。保留旧版快照；新旧目录先比较并合并用户改动，不盲目覆盖。默认交付为普通文件夹；只有明确选择 ZIP 发布附件时才压缩。

## 依赖按任务选择

- 初始化器和发布校验：Python 3.9+，仅标准库。初始化器不是使用 Skill 的必需步骤。
- 图像生成/编辑：实际可调用且满足本次输入需求的工具。可附入合规真实参考直接生成彩色画面；复杂结构按需约束。
- 医学内容：匹配的真实参考、实际查看及用途核验；图像证据与文字论断分别核对。
- 可编辑排字：Illustrator 或保留真实文字对象的矢量工具。指定 `.ai` 时需原生格式实际验收。
- 中文字体和 PDF：使用环境中实际可用、许可与用途匹配的字体及导出器；实际导出并看图。
- `humanize-writing`、`baoyu-comic`、三维工具、影像工具：可选，仅遇到对应任务才使用。缺失时用包内流程，不批量安装。
- 人工审阅：建议按内容邀请相关专家；仅缺签字可继续已授权制作并保持医学待审，明确先审后做时遵从。

详细实际测试见[首次环境检查](first-run.md)。包级检查不能证明图像生成、医学准确性或人工签字。

## 初始化器验收

从 Skill 根目录执行（或使用脚本实际路径）：

```bash
python3 scripts/test_init_medical_project.py
python3 scripts/init_medical_project.py /path/to/new-project
```

默认建立 5 个必要目录、5 份轻量模板（含来源与许可），不另建固定线稿或多轮审核目录。重复运行保留用户文件，补齐缺失模板；目录/文件冲突和根目录以下的符号链接在写入前拒绝。用户选择的根路径会解析到真实位置；不要在初始化同时改动目录结构，磁盘故障不保证事务回滚。

旧版 13 份模板不会被迁移或删除；沿用已有项目主稿即可，不为升级重建平行目录。
