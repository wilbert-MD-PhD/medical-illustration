# 安装 Medical Illustration V1.0

将下面的安装请求发给 Codex，或从 [V1.0 Release](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.0.0) 下载独立 Skill 安装包。

```text
请使用 $skill-installer 安装：
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.0.0/plugins/medical-illustration/skills/medical-illustration
先核对当前实际技能目录，保留已有同名版本的本地改动，不重复安装。
安装后读取 references/first-run.md，按本次任务检查图像生成、中文字体、可编辑排字与 PDF 导出。
```

手动安装时，将仓库 `plugins/medical-illustration/skills/medical-illustration/` 或 `dist/medical-illustration/` 的完整内容复制到宿主实际识别的技能目录。不要只复制 SKILL.md，也不要套两层同名目录。个人目录随宿主配置而定；以当前环境或安装器报告为准。重启/刷新后确认实际加载版本。

仓库保留 Marketplace 元数据（`.agents/plugins/marketplace.json` 与插件根的 `.codex-plugin/plugin.json`），供支持该格式的宿主使用；V1.0 本次没有实测 Marketplace 安装，也不表示已进入公共插件目录。

Release 中的 `medical-illustration-1.0.0.zip` 是独立 Skill 安装包，附同名 `.sha256` 校验文件。解压后使用直接包含 SKILL.md 的 `medical-illustration/` 文件夹。GitHub 自动提供的 Source code 是整个仓库，安装目录位于上述插件路径。

首次验收要区分“文件安装通过”“工具已发现”“实际生成/导出通过”。包内有完整流程与模板，不包含图像服务权限或 Illustrator 许可证。已有成功证据可复用，未实际执行的能力标为未实测。[完整依赖与验收](plugins/medical-illustration/skills/medical-illustration/references/dependencies-installation.md)。

## English installation

Give `$skill-installer` the versioned GitHub URL above, or download `medical-illustration-1.0.0.zip` and its `.sha256` checksum from the [V1.0 release](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.0.0). Extract the complete Skill folder into the directory recognized by your host. Preserve local edits and avoid installing duplicate versions in multiple locations.

The Skill folder is `plugins/medical-illustration/skills/medical-illustration/` in the repository, or `dist/medical-illustration/` after the default directory build. It must directly contain SKILL.md and all supporting resources. Read `references/first-run.md` after installation. Tool availability, successful image generation, editable typography, and PDF export are separate checks.

[中文主页](README.md) · [English homepage](README.en.md)
