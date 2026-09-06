# medical-illustration

医学科普插画、漫画与信息图的证据核验、医学母版、文案、可编辑排字、返修和交付工作流。

## 在 Codex 中安装

本仓库同时提供 Codex Marketplace。使用者可在终端执行：

```bash
codex plugin marketplace add wilbert-MD-PhD/medical-illustration
```

然后在 Codex 的 Plugins Directory 中从 **Medical Illustration Marketplace** 安装 **Medical Illustration**。安装后可直接说：

```text
使用 Medical Illustration Skill 制作一页具有医学证据链和出版质检记录的医学科普插画。
```

这是一项仓库 Marketplace 安装方式；要让陌生用户只说“请安装 Medical Illustration Skill”就能按名称发现，仍须通过 OpenAI 公共插件目录的审核与上架。

## 手动下载与安装

从 [Releases](https://github.com/wilbert-MD-PhD/medical-illustration/releases) 下载最新的 `medical-illustration-1.0.0-rc.2.zip`，解压后将其中完整的 `medical-illustration/` 文件夹复制到：

- 项目级：`<项目根目录>/.agents/skills/medical-illustration/`
- 个人级：`~/.agents/skills/medical-illustration/`

归档保留了 Skill 所需的 `SKILL.md`、references、examples、scripts、许可证与校验清单；解压后可在该目录执行：

```bash
shasum -a 256 -c SHA256SUMS
python3 scripts/test_init_medical_project.py
```

v1.0.0-rc.2 发布包 SHA-256：`4c688b8ad0d7e4d1566c23d478b777216a8e4a2736f255f0c2357cded91246e5`。

Release 归档与仓库 Marketplace 都保留 Skill 所需目录层级。内容采用 CC BY-NC-SA 4.0，`scripts/` 中的可执行 Python 代码采用 MIT；医学审核责任、第三方材料和生成作品的权利边界见包内 `NOTICE.md`。
