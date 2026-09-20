# Medical Illustration v1.2.0

将医学绘图 Skill 的接入方式扩展到不同 Agent，按实际可用能力完成漫画、医学插画与科研绘图。

- 增加原生 Skill、直接文件/资源加载、附件或文本交接说明，提供通用自然语言入口。
- 按来源检索、看图、生图、排字、导出和脚本执行映射工具，能力不足时交付可完成内容和具体待办。
- 安装和首次运行说明使用宿主实际配置路径，专属调用语法、安装器与 OpenAI 界面元数据作为可选适配保留。
- 独立包校验支持省略 OpenAI 界面元数据，继续核验清单中全部已分发文件。更新器支持任意位置的完整目录和显式安装路径，保留本地修改、备份与回退保护。
- Illustrator 沿用历史共用锁，确保不同 Agent 和旧运行器操作同一应用时串行执行。

## 安装与升级

见[安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.2.0/INSTALL.md)及[Agent 接入与能力映射](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.2.0/plugins/medical-illustration/skills/medical-illustration/references/agent-integration.md)。本地构建输出完整普通目录，正式发布附件使用 `medical-illustration-1.2.0.zip` 与同名 `.sha256`。已有独立安装通过随包更新器操作，插件安装由宿主管理。

医学证据、实际参考附件、可编辑交付、逐页视觉检查及人工审核状态沿用既有规则。[验证记录](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.2.0/docs/validation.md)列出本地检查范围。各宿主的自动发现和专属工具仍需在该环境验收。

## English

Version 1.2.0 makes the workflow usable across agents through native Skills loading, direct file/resource access, or task-specific context and handoff. Instructions map research, image, file, lettering and export requirements to the tools actually available.

OpenAI UI metadata and the existing Codex plugin layout remain optional adapters. Standalone package validation accepts packages without the UI adapter while checking every file declared in the manifest. The updater supports explicit installation paths and discovers its own complete directory wherever it is installed, retaining backup, rollback and local-edit protection.

The Illustrator dispatcher keeps its legacy shared lock for compatibility across agents and installed versions. Medical evidence, editable output and review requirements remain in force. Host discovery and actual production tools are verified in each environment, separately from local package regression tests.
