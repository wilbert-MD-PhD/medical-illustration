# 安装 Medical Illustration 1.1.2

本页对应 1.1.2。只有该标签与附件实际可用后才使用远端入口；本地构建完成不表示 GitHub 已发布。发布前验收使用当前源码构建的完整普通目录。本版修正默认任务提示与初始化器分支说明；随包检查更新、更新和回退功能继续可用。

```text
请使用 $skill-installer 安装：
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.1.2/plugins/medical-illustration/skills/medical-illustration
先确认标签存在，核对实际技能目录，保留已有同名版本的本地改动，不重复安装。
安装后读取 references/first-run.md，按本次任务检查图像生成、中文字体、可编辑排字与 PDF 导出。
```

手动安装时，将仓库 `plugins/medical-illustration/skills/medical-illustration/` 或独立构建的 `medical-illustration/` 完整复制到宿主实际识别的技能目录。必须直接包含 SKILL.md、references、scripts、agents 和许可文件；不要只复制 SKILL.md 或套两层同名目录。刷新后确认实际加载 VERSION 为 `1.1.2`。已有同名目录先比较并合并修改，不覆盖旧项目主稿。

[1.1.2 Release](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.1.2) 发布后，`medical-illustration-1.1.2.zip` 是独立安装包，附同名 `.sha256`。GitHub 的 Source code 是完整仓库，其中 Skill 位于上述插件路径。

## 已安装用户：检查、更新、回退

1.1.1 起可直接对 Codex 说：“检查医学绘图 Skill 更新”“更新医学绘图 Skill”或“回退医学绘图 Skill”。默认查询最新正式 Release；一次更新指令即可完成未修改独立安装的下载、校验、备份和替换。发现本地改动或无法确认旧版基线时先列明差异，不自动丢弃修改。

**1.1.0 及更早版本没有更新器，首次需要接入。** 本版发布后，从本版完整包中运行 `scripts/update_skill.py`，显式指向旧安装目录；不要再次用首次安装命令覆盖已有目录。缺少 VERSION 或 SHA256SUMS 的旧安装会标为未知，选择完整备份后可替换。详见[操作命令、旧版接入与恢复](plugins/medical-illustration/skills/medical-illustration/references/updating.md)。

遇 GitHub 匿名 API 限流时，更新器自动复用已登录的 GitHub CLI（可选），不索取或打印令牌；没有可用登录时保留原安装，可稍后重试或使用离线包。

更新后先运行 `python3 "<实际安装目录>/scripts/update_skill.py" check --offline --install-dir "<实际安装目录>"`，确认版本为 `1.1.2`、`integrity=clean` 且差异为空，并检查 LICENSE-CODE、LICENSE-CONTENT.md 和 NOTICE.md 均存在。路径须来自实际安装结果；不能只校验构建目录。

更新完成须刷新宿主并核对实际加载路径与 VERSION；磁盘文件更新成功不等于已有对话已加载新规则。插件管理或缓存中的副本应通过宿主更新；本脚本拒绝覆盖它们。

## Illustrator 与其他依赖

macOS 运行器、预检和会话库已随包提供；自动派发需要 Illustrator 和系统自动化权限。可选裁切需 Pillow。Windows/Linux 可静态预检或使用 SVG/矢量工具，本包不提供这些平台的 Illustrator 自动派发。[完整调用及平台范围](plugins/medical-illustration/skills/medical-illustration/references/illustrator-runtime.md)。

图像服务、字体二进制与 Illustrator 许可证不随包提供。安装通过、工具已发现、实际生成/导出通过分别记录。[依赖与首次验收](plugins/medical-illustration/skills/medical-illustration/references/dependencies-installation.md)。

仓库保留 Marketplace 元数据，供支持该格式的宿主使用；未实测 Marketplace 安装，也不表示已经进入公共插件目录。

## English installation

This page targets 1.1.2. Use the versioned URL above and the [1.1.2 release](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.1.2) only after the tag and assets are available. A local build does not establish publication. Local acceptance uses the complete directory built from this source.

Install the entire Skill directory, preserve existing edits, and verify VERSION after refreshing the host. The asset is `medical-illustration-1.1.2.zip` with its `.sha256` checksum. Source code archives contain the whole repository.

From 1.1.1, the bundled updater supports `check`, `update`, and `rollback`. Existing older installations must bootstrap it from a complete new package and pass their actual `--install-dir`. Local edits require an explicit backup-and-replace choice; the updater never merges them silently. See the [update guide](plugins/medical-illustration/skills/medical-illustration/references/updating.md). On anonymous API HTTP 403/429, the updater can reuse an already authenticated GitHub CLI without extracting tokens or starting login. If unavailable, retry later or use an offline package. Plugin-managed copies must use their host updater.

The bundled Illustrator dispatcher supports macOS and requires the application and Automation permission. Static preflight works without Illustrator; the optional crop helper requires Pillow. Windows/Linux users can use the SVG/vector workflow or a separately verified host adapter for native AI output. Image services, fonts and commercial licenses are not bundled.

[中文主页](README.md) · [English homepage](README.en.md)
