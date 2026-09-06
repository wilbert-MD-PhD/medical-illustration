# medical-illustration · 医学绘图

为医学科普插画、漫画和信息图提供证据核验、医学母版、文案、可编辑排字、返修和交付流程。适用于 Codex 或支持读取 SKILL.md 及相对资源的 agent 环境。

这是工作流程 Skill，不自带图像模型、Adobe Illustrator、医学图谱或人工审稿服务。高风险医学内容必须由当前项目的临床与解剖审稿人审核，AI 和安装成功不能代替签字。

## 安装

最简单：把以下两行粘贴给 Codex。安装器会识别链接中的版本和子目录；已有同名安装时先核对，保留用户改动。

```text
请使用 $skill-installer 将下面这个 Skill 安装到我的个人技能目录，并检查安装结果：
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.0.0-rc.4/plugins/medical-illustration/skills/medical-illustration
```

以下为手动安装步骤：

1. 下载 v1.0.0-rc.4 或更新版本的独立 Skill ZIP，或在仓库选择 Code → Download ZIP。rc.2 标签缺少源码，上传 ZIP 存在中文文件名编码问题，请使用新版本。
2. 独立 Skill ZIP：复制解压后的 `medical-illustration/`；源码 ZIP：复制 `plugins/medical-illustration/skills/medical-illustration/`。两者均须保留整个文件夹。
3. 项目使用：放到 `<项目根目录>/.agents/skills/medical-illustration/`；个人使用：放到 `~/.agents/skills/medical-illustration/`。
4. 查看技能列表和实际路径，确认加载的是本包。未出现时重新开启会话。已有同名版本先备份、核对，避免重复安装。

兼容路径、Windows、依赖与验收步骤见 [安装说明](references/dependencies-installation.md)。当前版本见 [VERSION](VERSION)。本目录是 Skill 根；GitHub 仓库采用 Marketplace 布局，源码中的路径为 `plugins/medical-illustration/skills/medical-illustration/`。Release 的独立 Skill ZIP 解压后直接得到 `medical-illustration/`。

## 开始使用

```text
使用 $medical-illustration 为一页仅用于手机阅读的科普生活场景建立页面任务卡、风险分级和结构化 prompt。当前只做草稿，不开始生成图像；无医学论断的字段注明不适用。
```

可查看 [实际可编辑排字示例](examples/editable-lettering/README.md)，包含 SVG、PNG 和 PDF 草稿及检查记录。

其他工作模式包括完整项目、单幅制作、局部返修和印前交付。无真实素材的草稿示例见 [通用示例](examples/generic-visit-preparation/示例说明.md)。纯数字作品执行数字交付检查；印刷作品在印前锁定前取得出版方书面规格。

## 工具与运行

- 编写和审阅流程无需运行脚本。可选初始化器需要 Python 3.9+，仅使用标准库。
- 图像生成工具、baoyu-comic 和 humanize-writing 均为可选；缺少 humanize-writing 可手工受控润色。
- 最终排字需要 Illustrator 或具备可编辑文字、分层、锁定和所需导出能力的等价矢量工具。用户指定 .ai 时按指定格式验收。
- 解剖内容需要本地可核验参考包、合法素材与适用人工审核，包内不附带第三方医学资产。

在本目录运行（Windows 可用 `py -3`）：

```bash
python3 scripts/init_medical_project.py "你的项目目录"
python3 scripts/test_init_medical_project.py
```

初始化器保留已有文件，先检查类型冲突并拒绝项目内部符号链接。新模板自带来源说明；已有模板不被改写。请在独立项目目录运行，不将产物写回 Skill 发布目录。

## 许可与反馈

作者：wilbert。内容和文字模板采用 [CC BY-NC-SA 4.0](LICENSE-CONTENT.md)，可执行 Python 代码采用 [MIT](LICENSE-CODE)。代码中的模板数据仍属于内容许可范围。复制模板须保留署名和许可；使用流程独立创作的新作品不会自动采用本包许可，详见 [NOTICE.md](NOTICE.md)。商业使用内容部分需要另行取得授权。

发布后可通过本仓库 Issues（如已启用）反馈问题或联系作者询问授权；请提供包版本、环境、复现步骤及去除个人信息的最小示例，不提交患者资料或凭据。若 Issues 未启用，请使用仓库作者公开提供的联系方式。

本版本为发布候选；修改与验证范围见 [CHANGELOG.md](CHANGELOG.md)。
