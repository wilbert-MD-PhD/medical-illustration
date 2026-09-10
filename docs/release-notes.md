# Medical Illustration v1.0.0

首个正式版本整合实际制作中成熟的医学绘图流程，延续上一代安装和校验基础设施。

- 支持真实参考约束下直接生成整页、连续场景和单幅彩色无字画面；按内容选择线稿、三维与拆层。
- 补齐本地参考复用、可信原始图源主动下载、实际看图及附图、独立来源核对、用途许可与上游来源链。
- 加入独立创可贴漫画 v1.4：展示从 Frontiers 与 NIH/NIAID 获取三张参考、真实传入绘图和返修的过程，附原图、署名、下载哈希与调用记录。
- 生图前按实际文案规划首页标题、对白和标签空间；底图不生成气泡/尾巴/文字框，生成后先试排。
- 保持文字、气泡、医学标签和后加箭头可编辑；新增可选 Illustrator 排字库。
- 人工未签可继续已授权制作并保持医学待审；移除固定审核关卡和不必要的模板负担。
- 轻量初始化继续保护已有文件、拒绝异常路径、保留中文兼容与模板署名。
- 主页按用途、成品效果与上手方法组织，版本变化集中在 Release 说明；精简随包示例。
- 默认构建普通文件夹；仅显式请求 ZIP 时压缩。更新双语首页、安装文档、示例、测试和校验。

安装见[仓库安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/main/INSTALL.md)。从 RC 升级请保留本地改动；不要自动覆盖旧项目主稿。历史示例与旧版记录保留原语义，不作为当前模板。

此版本的“正式”指软件包版本。医学作品仍按实际状态记录，包级测试不替代医学审签、图像模型评估或原生 AI/印前验收。具体验证范围见[验证说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.0.0/docs/validation.md)。

## 下载与安装

- `medical-illustration-1.0.0.zip`：独立 Skill 安装包，解压后得到完整的 `medical-illustration/` 目录。
- `medical-illustration-1.0.0.zip.sha256`：安装包 SHA-256 校验值。
- GitHub 自动提供的 Source code：完整仓库，包含主页、示例漫画及维护工具。


## English

The first stable release brings together the production-tested workflow and the earlier installation and verification infrastructure. It adds flexible reference-constrained color generation, local reference reuse and source chains, text-space planning without baked-in bubbles, trial lettering, editable text/bubbles/labels, an optional Illustrator helper, truthful review states, and lightweight non-destructive initialization. Ordinary folders are the default build output; ZIP requires an explicit choice.

A new bandage comic (v1.4) documents retrieval of three references from Frontiers and NIH/NIAID, actual reference attachments, revisions and editable lettering, with source credits and hashes.

Preserve local edits when upgrading from an RC. Stable package status does not certify medical accuracy or print readiness of generated work. Image-model evaluation, Illustrator host validation, human medical approval, and remote CI must be reported separately.

The homepage presents use cases, finished artwork and setup for first-time visitors. Version changes are collected in release notes; bundled examples have been reduced.

Download `medical-illustration-1.0.0.zip` for the standalone Skill and the matching `.sha256` file to verify it. GitHub’s Source code archives contain the entire repository, including showcase artwork and maintenance tools.
