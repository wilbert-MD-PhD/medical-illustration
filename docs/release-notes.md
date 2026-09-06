# v1.0.0-rc.3

本版修复安装与发布一致性，并补充首页和可编辑示例。

- 版本标签包含完整 Marketplace 与 Skill；独立 ZIP 从标签内的同一 Skill 目录生成。
- 修复中文 ZIP 文件名编码，增加默认解压、校验清单、相对链接和附件/源码一致性检查。
- 统一插件根、Skill 根和独立 ZIP 的安装说明；提供固定版本的安装器示例及两步插件命令。
- 合格的本地参考包可以核验后复用；缺项时再联网补齐。医学核验与人工审核要求保留。
- 增加无字 SVG、可编辑排字 SVG、PNG 预览和 PDF 审阅稿。示例无医学论断，状态为草稿。
- 加入三平台验证与从版本标签自动发布、下载附件回验的工作流。

**下载：** 手动安装选择 `medical-illustration-1.0.0-rc.3.zip`。自动 Source code 包含整个 Marketplace 仓库，Skill 位于 `plugins/medical-illustration/skills/medical-illustration/`。

**验证范围：** 初始化器 12 项回归测试，另有发布边界测试、文件校验和链接检查。实际运行结果见 Actions 与仓库 docs/validation.md。完整医学图像生成、Illustrator 原生 .ai 和独立新会话行为仍需对应验证，不以软件测试代替医学审核。

**旧版已知问题：** rc.2 标签只含 README，其上传 ZIP 的 4 个中文文件名缺少 UTF-8 标记；不要继续使用该标签或附件安装。旧标签保留以维持历史可追溯性。
