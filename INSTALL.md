# 安装 Medical Illustration

将完整 `medical-illustration/` 目录提供给所用 Agent，再按本次任务配置工具。本包采用 [Agent Skills 格式](https://agentskills.io/specification)，接入方式由宿主能力决定。

## 一句话安装

将下面这一句话复制给 Codex、Claude Code 等具备联网和文件操作能力的 Agent：

```text
请从 https://github.com/wilbert-MD-PhD/medical-illustration 安装最新正式版 medical-illustration Skill，按仓库 INSTALL.md 选择适合当前 Agent 的安装方式，保留已有本地修改，并核验版本与文件完整性。
```

## 选择接入方式

| 环境 | 做法 |
|---|---|
| 原生支持 Skill 的 Agent | 使用该宿主实际可用的安装器，或复制完整目录到其配置的技能位置。刷新后核对加载路径和 VERSION |
| 可读取文件或资源的 Agent | 将完整目录放到可访问的工作区或资源存储，在任务中指定 `SKILL.md` 的实际路径或资源标识 |
| 仅支持附件或文本的 Agent | 提供 `SKILL.md` 和本次任务引用的分支资源，按[能力映射](plugins/medical-illustration/skills/medical-illustration/references/agent-integration.md)交接需要工具执行的步骤 |

不同宿主的目录、安装器和调用语法以其当前配置为准。完整目录直接包含 `SKILL.md`、`references/`、`scripts/`、版本清单及许可文件，避免套两层同名目录。已有同名版本先比较并保留用户修改，再按更新流程处理。

`agents/openai.yaml` 是可选 OpenAI 界面元数据，其他 Agent 可忽略。仓库外层的 Codex 插件与 Marketplace 元数据作为兼容入口保留。现有发布包仍包含界面文件，按 SHA256SUMS 核验全部已分发文件。

## 获取完整目录

- 本地源码：`plugins/medical-illustration/skills/medical-illustration/`。
- 本地构建：在仓库根运行 `python3 scripts/release.py build`，生成 `dist/medical-illustration/`。已有输出会保留，可用 `--output` 指定新目录。
- 正式 Release：[发布列表](https://github.com/wilbert-MD-PhD/medical-illustration/releases)。当前正式版为 [v1.3.0](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.3.0)，下载 `medical-illustration-1.3.0.zip` 及同名 `.sha256`。GitHub Source code 是完整仓库，Skill 位于上述源码路径。

本版 `VERSION` 为 `1.3.0`，安装后核对所选发布标签与实际目录版本。使用随包更新器离线检查文件完整性，命令见下文。

## 开始使用

```text
请读取 <实际目录或资源标识>/medical-illustration/SKILL.md。
为没有医学背景的读者制作一页伤口愈合科普漫画。
按任务读取相关参考文件，确认当前可用工具后，完成可信参考、分镜、画面和可编辑排字。
交付 Markdown 脚本、可编辑源文件及 PDF，并列明实际完成和待检查的部分。
```

支持技能名称调用时可直接说“使用 medical-illustration”。支持 `$medical-illustration` 的宿主也可沿用该语法。`$skill-installer` 仅在该安装器实际可用时使用。首次使用按[环境检查](plugins/medical-illustration/skills/medical-illustration/references/first-run.md)验收本次所需能力。

## 检查、更新与回退

从 1.1.1 起，可向具备命令执行能力的 Agent 说“检查医学绘图 Skill 更新”“更新医学绘图 Skill”或“回退医学绘图 Skill”。也可在终端运行随包脚本，显式传入任意位置的实际独立安装目录：

```bash
python3 "<实际安装目录>/scripts/update_skill.py" check --offline --install-dir "<实际安装目录>"
python3 "<实际安装目录>/scripts/update_skill.py" check --install-dir "<实际安装目录>"
python3 "<实际安装目录>/scripts/update_skill.py" update --install-dir "<实际安装目录>"
python3 "<实际安装目录>/scripts/update_skill.py" rollback --install-dir "<实际安装目录>"
```

更新默认查询最新正式 Release，完成校验、完整备份和替换。发现本地修改时列出差异，按用户已给出的处理授权继续。旧版无更新器时，从完整新包运行更新器并指向旧安装。插件管理的安装使用宿主更新机制。操作、离线包和恢复说明见[更新指南](plugins/medical-illustration/skills/medical-illustration/references/updating.md)。

更新后核对实际目录的 VERSION、`integrity=clean`、空差异和三个许可文件。原生 Skill 宿主刷新后核对加载版本，直接文件/资源加载方式重新读取更新内容。无命令工具时交接上述操作和待验证结果。

## 按任务准备工具

- 阅读规则、编写脚本和分镜可独立进行。来源检索、看图、生图、可编辑排字及 PDF 导出分别映射到当前环境可用能力。
- 辅助脚本使用 Python 3.9+。可选图片裁切需 Pillow。安装依赖时优先复用已有项目环境。
- 随包 Illustrator 自动派发支持 macOS，需要 Illustrator 和系统自动化权限。其他环境可用 SVG/矢量工具或经验证的原生格式适配器，见[运行说明](plugins/medical-illustration/skills/medical-illustration/references/illustrator-runtime.md)。
- PPTX 原生对象及同版 PDF/PNG 见[制作与交付](plugins/medical-illustration/skills/medical-illustration/references/pptx-delivery.md)，按任务选择，源稿与导出分别验收。
- 字体、图像服务和商业软件许可证按实际用途准备。完整能力对应与交接规则见[Agent 接入说明](plugins/medical-illustration/skills/medical-illustration/references/agent-integration.md)。

## English installation

Copy this one-line instruction to Codex, Claude Code or another agent with network and file access:

```text
Install the latest stable medical-illustration Skill from https://github.com/wilbert-MD-PhD/medical-illustration using the method in INSTALL.md that fits your current agent, preserve existing local edits, and verify the installed version and file integrity.
```

Provide the complete `medical-illustration/` folder to your agent. A native Skills host can load it from its configured skills location. Other agents can read `SKILL.md` and task-specific references through files, attachments, resource tools or injected context. Point to the actual entrypoint in your request. See [Agent Skills integration](https://agentskills.io/client-implementation/adding-skills-support) for the underlying loading model.

Use the source directory `plugins/medical-illustration/skills/medical-illustration/` or build a standalone folder with `python3 scripts/release.py build`. The published [v1.3.0 Release](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.3.0) provides the standalone ZIP and `.sha256`. Keep existing edits and verify the loaded VERSION. Local builds and remote publication are tracked separately.

`agents/openai.yaml` is optional host UI metadata. Other agents can ignore it while retaining the distributed files for checksum verification. The outer Codex plugin layout is a compatibility adapter. Native invocation syntax and installer names depend on the host; direct file/resource loading is also supported.

The updater uses Python 3.9+ and an explicit `--install-dir` for standalone installations at any location. Run `check`, `update`, or `rollback` with the commands above. Older installations can bootstrap the updater from a complete new package. Managed plugins use their host updater. See the [update guide](plugins/medical-illustration/skills/medical-illustration/references/updating.md) for local edits, backups and offline packages.

Map the workflow to available research, image, file, lettering and export tools. The bundled Illustrator dispatcher requires macOS, Illustrator and Automation permission. Other environments can use SVG/vector tools or a verified adapter. When tools are missing, deliver the completed script/specification and an explicit handoff, keeping execution, visual inspection and medical review status separate.

[中文主页](README.md) · [English homepage](README.en.md)
