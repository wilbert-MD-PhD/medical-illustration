# Medical Illustration v1.1.0

加入科研绘图独立分支与可追溯腕骨漫画示例，并补齐 Illustrator 自动化随包依赖。漫画脚本与科研机制图各走适用流程。

- 以医生《腕骨与关节组成》v1.1 展示5幅解剖图的来源对应，提供具体图版/页码、实际附件、五组局部对照及原始参考预览。主页移除创可贴参考图表，保留漫画和来源档案。
- 改善对照图中英文字符宽度、图注间距和留白，恢复双语主页验证与 Release 入口。
- 新增科研图规格、结构与关系证据记录、连线语义和可选 JSON 检查；漫画任务不自动载入科研记录。
- 随包提供 macOS Illustrator 运行器、静态预检、文档会话库和可选 Pillow 裁切工具，删除个人路径与私有项目配置依赖。
- 排字库接入显式文档登记、原生 AI 检查点、嵌入链接和 finally 收尾；保留已有文档，超时保留未确认锁。
- 保持非覆盖初始化、Unicode 路径、目录构建与校验；新增运行组件及关系记录测试。

## 升级与安装

见[1.1.0 安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.1.0/INSTALL.md)。保留实际安装目录的修改；不迁移或删除旧项目模板，不移动既有 v1.0.0 标签。

macOS 自动派发需 Illustrator 和正常系统自动化权限；Windows/Linux 可静态预检或使用 SVG/矢量工作流。图像服务、字体和商业软件许可不在安装包内。[本版本验证范围](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.1.0/docs/validation.md)。

软件版本不构成医学审签或印前批准。腕骨示例仍医学待审；来源与文件匹配不保证所有医学细节均正确。

## 下载附件

创建本版本 Release 后提供：

- `medical-illustration-1.1.0.zip`：独立 Skill 安装包。
- `medical-illustration-1.1.0.zip.sha256`：安装包校验值。
- Source code：完整仓库，包括主页、展示图片及维护工具。

## English

Version 1.1.0 adds a separate research-figure workflow, explicit mechanism evidence records and a consistency checker. A six-page doctor comic documents five anatomy assets, exact reference locations, actual generation inputs and five detail comparisons. The bilingual homepages restore status links and improve comparison typography.

The package includes the macOS Illustrator dispatcher, preflight, document-session library and optional Pillow crop helper. The lettering library uses explicit ownership and native AI checkpoints. Existing documents remain protected; uncertain timeouts retain the shared lock. Windows/Linux support static preflight and the SVG/vector workflow, not automatic Illustrator dispatch through this adapter.

Preserve local edits when upgrading. After release, install the complete Skill from `medical-illustration-1.1.0.zip` and verify its checksum. Package checks, host execution, visual inspection and human medical approval are distinct; the comic remains pending medical review.
