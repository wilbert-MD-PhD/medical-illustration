# Medical Illustration · 医学绘图

**把医学证据、画面制作和可编辑交付，组织成一套可追溯的工作流程。**

面向医学科普插画、漫画和信息图，帮助 Codex 从页面目标出发，整理证据与参考图、编写分镜和文案、保护已确认的医学结构，并完成排字、返修与交付检查。

[![Validation](https://github.com/wilbert-MD-PhD/medical-illustration/actions/workflows/validate.yml/badge.svg)](https://github.com/wilbert-MD-PhD/medical-illustration/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/wilbert-MD-PhD/medical-illustration?include_prereleases)](https://github.com/wilbert-MD-PhD/medical-illustration/releases)

[下载安装](#下载安装) · [查看示例](#看看实际产物) · [使用方法](#开始使用) · [验证范围](docs/validation.md) · [English](README.en.md)

## 它能帮你做什么

| 你的任务 | Skill 提供的工作方式 | 可保留的产物 |
|---|---|---|
| 从零策划医学科普页 | 定义受众、页面目标、风险和医学证据 | 页面任务卡、证据矩阵、术语表、分镜与 prompt |
| 绘制医学内容 | 核验本地参考，明确侧别、层次和医学结构 | 参考图登记、医学母版与空间规格 |
| 添加中文对白或标签 | 复用底图，独立管理可编辑文字与气泡 | SVG、指定格式源文件、PDF 审阅稿与排字记录 |
| 修改已有作品 | 明确变更区，复用已批准资产，复核保护区 | 修改版本、差异检查和审核继承记录 |
| 准备数字或印刷交付 | 按载体完成医学、文字和输出检查 | 交付文件、来源说明与审校记录 |

这是一项 **工作流程 Skill**。图像生成、矢量编辑软件和人工医学审核由使用环境提供；安装包包含指令、参考流程、模板、初始化器和示例，不捆绑医学图谱或图像模型。未完成适用审核的作品保留草稿或医学待审状态。

## 看看实际产物

**TFCC 医学科普漫画：从无字底板到填字后的 PDF 审阅稿。** 以下两页展示场景叙事、人物连续性和中文排字效果。

| 第一页 · 受伤场景 | 第二页 · 日常动作 |
|:---:|:---:|
| [![第一页填字效果](docs/showcase/tfcc/page-1.jpg)](docs/showcase/tfcc/page-1.jpg) | [![第二页填字效果](docs/showcase/tfcc/page-2.jpg)](docs/showcase/tfcc/page-2.jpg) |

[**查看两页 PDF 审阅稿**](docs/showcase/tfcc/review.pdf) · [第一页无字底板](docs/showcase/tfcc/base-1.png) · [第二页无字底板](docs/showcase/tfcc/base-2.png) · [示例说明](docs/showcase/tfcc/README.md)

<details>
<summary>展开对比：两页无字底板</summary>

| 第一页 · 无字底板 | 第二页 · 无字底板 |
|:---:|:---:|
| [![第一页无字底板](docs/showcase/tfcc/base-1.png)](docs/showcase/tfcc/base-1.png) | [![第二页无字底板](docs/showcase/tfcc/base-2.png)](docs/showcase/tfcc/base-2.png) |

</details>

示例保留 PDF 审阅稿状态，用于展示制作效果。

## 下载安装

**在 Codex 对话框中粘贴以下内容，即可安装并检查制作环境。**

```text
请使用 $skill-installer 将下面这个 Skill 安装到我的个人技能目录，保留已有改动。
安装后按 references/first-run.md 检查图片生成、中文排字与 PDF 导出，按需补齐免费依赖：
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.0.0-rc.5/plugins/medical-illustration/skills/medical-illustration
```

适用于可访问本地文件和 GitHub 的 Codex 桌面端、CLI 或 IDE。安装后在下一轮调用 `$medical-illustration`；未显示时重启 Codex。图像生成权限由当前账号与工具环境提供。

[**分享安装与使用说明**](INSTALL.md) · [首次环境检查](plugins/medical-illustration/skills/medical-illustration/references/first-run.md)

<details>
<summary>其他安装方式：手动 ZIP / Marketplace</summary>

### 手动安装 ZIP

1. **[下载 v1.0.0-rc.5 独立 Skill ZIP](https://github.com/wilbert-MD-PhD/medical-illustration/releases/download/v1.0.0-rc.5/medical-illustration-1.0.0-rc.5.zip)**，或前往 [Releases](https://github.com/wilbert-MD-PhD/medical-illustration/releases) 选择更新版本。
2. 解压后将完整 `medical-illustration/` 文件夹放到下面任一位置。
3. 确认目录里直接存在 `SKILL.md`，刷新技能列表；未显示时重新启动 Codex。

| 安装范围 | 位置 |
|---|---|
| macOS / Linux 个人级 | `~/.agents/skills/medical-illustration/` |
| Windows 个人级 | `%USERPROFILE%\.agents\skills\medical-illustration\` |
| 当前项目 | `<项目根目录>/.agents/skills/medical-illustration/` |

如果使用 **Code → Download ZIP** 或 Release 的 **Source code**，下载的是整个仓库。需要复制的 Skill 在 `plugins/medical-illustration/skills/medical-illustration/`。只复制 `SKILL.md` 会缺少必要资源。

**旧版说明：** `v1.0.0-rc.2` 的标签只有 README，附件 ZIP 也存在中文文件名编码缺陷。请使用 `rc.5` 或更新版本，详见 [发布说明](docs/release-notes.md)。

### 通过 Codex Marketplace 安装插件

使用支持 `codex plugin` 的 CLI：

```bash
codex plugin marketplace add wilbert-MD-PhD/medical-illustration
codex plugin add medical-illustration@medical-illustration-marketplace
```

第一条添加来源，第二条安装插件。也可以添加来源后，在插件目录的 **Medical Illustration Marketplace** 中安装 **Medical Illustration**。命令不支持时使用对话安装或手动 ZIP。

GitHub 仓库 Marketplace 是明确指定来源的安装方式；公共插件目录按名称发现需要另行上架。

[完整安装、依赖与验收说明](plugins/medical-illustration/skills/medical-illustration/references/dependencies-installation.md)

</details>

## 开始使用

**制作你的第一篇漫画：** 将方括号内容替换为自己的需求。

```text
使用 $medical-illustration，为[目标读者]制作[页数]页关于[主题]的医学科普漫画。
先核验依据、规划角色和分镜，再按适用审核流程制作无字底板、
可编辑中文文字层和 PDF 审阅稿。未完成医学审核的内容保留待审状态。
```

**给已有画面排字：**

```text
使用 $medical-illustration 为我的现有底图添加中文对白。
复用底图，保持人物、医学结构、箭头和构图不变。
文字与气泡独立可编辑，交付 SVG 源文件和 PDF 审阅稿。
```

**复用本地医学参考：**

```text
使用 $medical-illustration 核验我提供的本地参考包和来源记录。
合格资料直接复用，缺项再补检索。先制作供人工审核的线稿，
记录待审项和当前版本。
```

完整项目可从证据核验推进到分镜、线稿、合成排字与交付；单页和局部返修只执行适用步骤。已有审核是否继续有效，按变更影响判断。

## 环境与验证

- **指令与模板：** 支持读取 `SKILL.md` 及相对资源的 Codex 或兼容 agent。
- **初始化器与打包工具：** Python 3.9+，只使用标准库。
- **图像生成：** 可使用环境提供的生成工具；主要用于低风险场景与表现层。
- **可编辑交付：** Illustrator 或满足文字编辑、分层及所需导出能力的矢量工具；指定 `.ai` 时单独验收。
- **医学内容：** 合法参考资料、证据核验和适用人工审稿。已有合格本地参考可以复用。
- **可选工作流：** `humanize-writing`、`baoyu-comic` 缺失时可采用包内说明的替代流程。

CI 检查 Windows、macOS、Linux 上的初始化、资源链接、版本一致性、文件校验和 Unicode ZIP 解压。**这些测试验证软件包；医学准确性、真实模型生成质量与人工签字须另行验证。** [查看实测范围与场景](docs/validation.md)。

## 维护与反馈

发现安装或流程问题，请通过 [Issues](https://github.com/wilbert-MD-PhD/medical-illustration/issues) 提供版本、环境、复现步骤和去除个人信息的最小示例。改进代码和文档前可先阅读 [维护与发布](docs/maintaining.md)。

作者：**wilbert**。内容、模板和示例采用 **CC BY-NC-SA 4.0**，可执行代码采用 **MIT**。使用流程独立创作的新作品不自动继承本包许可；复制模板和第三方素材须遵循各自条款。商业使用内容部分请联系作者取得授权。[许可范围](LICENSE.md) · [责任与第三方材料](plugins/medical-illustration/skills/medical-illustration/NOTICE.md)
