# 依赖、安装与验收

首次使用先执行 [首次环境检查与开始制作](first-run.md)，按任务补齐依赖并产出实际验收文件。Skill 安装成功不等于图像工具、字体或 PDF 导出已就绪。

## 依赖分类

### 必需环境与能力

- 支持从技能目录读取 `SKILL.md` 及相对路径资源的 Codex 或兼容 agent 环境。
- 对新项目目录的读写权限。使用初始化脚本时需 Python 3.9 或更新版本（仅依赖标准库）；也可不运行脚本，手工建立同等记录。
- 能够获取并在本地核验权威文献、解剖参考图及其来源和许可；如果当前任务含解剖或具体医学论断，这是制作而非仅安装的必需条件。
- 能保存分层、可编辑的医学母版和无字底图，并对导出的 PDF/图像执行实际视觉检查。
- 需要最终可编辑文字时，必须具备 Adobe Illustrator 或能产生等价分层矢量文件的工具。

### 可选技能与工具

- `$humanize-writing`：只用于已锁定医学事实稿后的受控公众表达润色。不可用时可手工改写并执行同样的逐句语义回归。
- `baoyu-comic`：用于知识漫画的内容分析、角色规划和分镜草案；它不替代 G1–G11。
- `imagegen` 或其他生成工具：用于低风险角色、生活场景、构图候选和非医学表现层。
- 信息图工具、3D Slicer、Blender、DICOM 去标识化工具、差异图和 PDF 预检工具：仅在对应产物需要时使用。

可选工具缺失时，先使用已说明的人工流程或满足要求的替代工具。只有对应能力全部不可用，或无法满足用户明确指定的格式时，才交付上一个可验收阶段的产物并标记待办；保留有效审核记录，不伪称完成缺失的工作。

### 人工环节

- 项目负责人：确定受众、载体、范围、人员和发布决定。
- 相关临床审稿人：审核论断、病程、查体、治疗、康复、风险和行动建议。M 级页至少需一名相关临床审稿人。
- 解剖审稿人：审核结构、层次、侧别、视角、附着和空间关系。H 级页需临床与解剖双审。
- 医学插画师或负责医学线稿的人员：依据已核验参考制作事实层。
- 编辑/文字校对人员：确认术语、语义、可读性、图文一致和声明。
- 授权或法务负责人：核对字体、图像、影像、肖像、模型和衍生作品条款。
- 印前人员：依出版社书面规格检查尺寸、出血、色彩、字体、透明度、套印和 PDF。

AI、自检脚本、工具运行成功和视觉相似度都不属于人工签字。审稿责任必须由当前项目的实际责任人承担。

## 安装

必须保留整个 `medical-illustration/` 目录，不要只复制 `SKILL.md`。

### 通过 Codex 对话安装（推荐）

将包含版本与子目录的完整链接发给 `$skill-installer`：

```text
请使用 $skill-installer 将下面这个 Skill 安装到我的个人技能目录，并检查安装结果：
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.0.0-rc.5/plugins/medical-illustration/skills/medical-illustration
```

适用于可访问本地文件与 GitHub 的 Codex 环境。安装器应保留完整 Skill 文件夹，报告实际安装路径；安装器本身不会自动覆盖已有同名目录。使用者有旧版本时先核对路径和本地改动，再按其更新请求处理。安装完成后下一轮尝试调用；列表未刷新时重启 Codex。安装器默认路径随环境版本可能不同，以当前环境实际可发现的个人技能目录为准。

### 从 GitHub 下载

下载 v1.0.0-rc.5 或更新版 Release 的独立 Skill ZIP（不要使用有缺陷的 rc.2），或从仓库 Code → Download ZIP 下载源码。独立 Skill ZIP 的根文件夹是 `medical-illustration/`；源码 ZIP 内的 Skill 位于 `plugins/medical-illustration/skills/medical-illustration/`。解压后找到同时包含 `SKILL.md`、`agents/`、`references/`、`scripts/` 和许可文件的目录；将该目录整体复制并命名为 `medical-illustration`。不要只复制主文件，也不要将外层压缩包目录嵌套成两层同名 Skill。

### 项目级安装

将完整文件夹放到 `<项目根目录>/.agents/skills/medical-illustration/`。

### 个人级安装

将完整文件夹放到 `~/.agents/skills/medical-illustration/`；Windows 使用当前用户主目录下的 `.agents/skills/medical-illustration/`。

以上路径依据 [OpenAI 技能文档](https://developers.openai.com/codex/skills/#where-codex-loads-local-skills)，核验日期 2026-09-06。某些既有环境仍使用 `.codex/skills` 或用户配置目录的 `skills`；只在当前环境明确使用该路径时选择兼容位置。

### 版本和重复安装

`VERSION` 标识这个发布包的版本；以当前下载包为安装来源，不混入其他项目的同名安装。安装前查看技能列表里的实际路径，备份旧版本并由使用者选择保留哪一份；同名技能不会自动合并。不要盲目同时安装到 `.agents` 和 `.codex`。更新后刷新技能列表，未出现时重新开启会话。

验收时通过技能路径确认加载的是这个版本。GitHub 仓库采用 Marketplace 布局：仓库根包含 `.agents/plugins/marketplace.json`，插件根为 `plugins/medical-illustration/`，Skill 根为其下的 `skills/medical-illustration/`。独立 ZIP 由同一版本标签中的 Skill 根生成，不混入宿主医学项目或个人安装内容。

## 验收

### A. 包结构

确认以下文件可读：

```text
README.md
VERSION
CHANGELOG.md
SKILL.md
agents/openai.yaml
references/dependencies-installation.md
references/workflow.md
references/copy-and-lettering.md
references/generation-and-assets.md
references/revision-and-prompting.md
references/qa-and-prepress.md
references/templates.md
scripts/init_medical_project.py
scripts/test_init_medical_project.py
examples/generic-visit-preparation/示例说明.md
LICENSE-CONTENT.md
LICENSE-CODE
NOTICE.md
```

### B. 元数据与链接

- `SKILL.md` 的 YAML frontmatter 能被识别，技能名为 `medical-illustration`。
- `agents/openai.yaml` 中的默认 prompt 显式包含 `$medical-illustration`。
- 打开 `SKILL.md` 中的相对链接，确认不依赖原作者电脑的绝对路径。

如果当前环境附带 Codex skill 验证器，运行：

```bash
python3 <skill-creator 目录>/scripts/quick_validate.py <medical-illustration 目录>
```

结果应包含 `Skill is valid!`。

### C. 非破坏性脚本测试

在一个新的临时目录中运行：

```bash
python3 scripts/init_medical_project.py <临时目录>/medical-illustration-smoke-test
python3 scripts/init_medical_project.py <临时目录>/medical-illustration-smoke-test
```

从 Skill 根目录运行命令，或将脚本路径改为实际绝对路径；Windows 可用 `py -3` 替代 `python3`。首次运行应创建 13 份模板（含模板来源与许可说明）；第二次保留已有内容。已有模板不会自动插入新署名，迁移旧项目时需核对来源说明。

运行包含异常路径用例的自动测试：

```bash
python3 scripts/test_init_medical_project.py
```

脚本在写入前检查全部计划路径；目录与文件类型冲突、项目内部符号链接（包括失效链接）均报错并返回非零。用户选定的项目根路径会先解析到真实位置；该根目录以下不跟随符号链接。初始化期间请勿由其他进程同时改动目录结构；预检不能保证磁盘写入故障时事务回滚。

### D. 行为验收

在新会话中输入：

```text
使用 $medical-illustration 为一页医学科普对话页建立页面任务卡、风险分级、结构化 prompt 和审核状态。不要开始生成图像。
```

验收点：

- 先定义页面目标和 H/M/L 风险，而不是直接生成图像。
- 医学论断会绑定证据；无法核验时会标记待核或删除。
- 解剖内容会要求本地参考图、来源/许可登记和医学母版。
- 会区分工具检查与人工签字，不把 AI 输出称为“医学通过”。
- 未完成适用医学审核时保留草稿或医学待审；已批准内容只在受影响时失效。
- 纯数字草稿不因缺出版社规格停止；正式数字交付另记输出检查与发布决定。
- 没有 Illustrator 但有合格矢量工具时继续排字；没有 humanize Skill 时可手工受控润色。
- 只改装饰且保护区复核通过时记录批准继承；医学已通过而只差印前时保留医学批准。

自动脚本测试不能代替这些行为验收，也不能签署医学审核。

### E. 示例项目

打开 `examples/generic-visit-preparation/`，确认：

- 不含 TFCC、原项目角色、病例、解剖母版、影像或私有授权素材；
- 示例状态为 `草稿`，不宣称医学通过；
- 示例仅演示页面任务、结构化 prompt、渲染清单与审计字段。
