# 安装 Medical Illustration 1.1.0

本页对应 1.1.0。只有该标签与附件实际可用后才使用远端入口；本地构建完成不表示 GitHub 已发布。发布前验收使用当前源码构建的完整普通目录。旧版不包含本次新增的科研分支、腕骨映射和受管运行组件。

```text
请使用 $skill-installer 安装：
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.1.0/plugins/medical-illustration/skills/medical-illustration
先确认标签存在，核对实际技能目录，保留已有同名版本的本地改动，不重复安装。
安装后读取 references/first-run.md，按本次任务检查图像生成、中文字体、可编辑排字与 PDF 导出。
```

手动安装时，将仓库 `plugins/medical-illustration/skills/medical-illustration/` 或独立构建的 `medical-illustration/` 完整复制到宿主实际识别的技能目录。必须直接包含 SKILL.md、references、scripts、agents 和许可文件；不要只复制 SKILL.md 或套两层同名目录。刷新后确认实际加载 VERSION 为 `1.1.0`。已有同名目录先比较并合并修改，不覆盖旧项目主稿。

[1.1.0 Release](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.1.0) 发布后，`medical-illustration-1.1.0.zip` 是独立安装包，附同名 `.sha256`。GitHub 的 Source code 是完整仓库，其中 Skill 位于上述插件路径。

## Illustrator 与其他依赖

macOS 运行器、预检和会话库已随包提供；自动派发需要 Illustrator 和系统自动化权限。可选裁切需 Pillow。Windows/Linux 可静态预检或使用 SVG/矢量工具，本包不提供这些平台的 Illustrator 自动派发。[完整调用及平台范围](plugins/medical-illustration/skills/medical-illustration/references/illustrator-runtime.md)。

图像服务、字体二进制与 Illustrator 许可证不随包提供。安装通过、工具已发现、实际生成/导出通过分别记录。[依赖与首次验收](plugins/medical-illustration/skills/medical-illustration/references/dependencies-installation.md)。

仓库保留 Marketplace 元数据，供支持该格式的宿主使用；未实测 Marketplace 安装，也不表示已经进入公共插件目录。

## English installation

This page targets 1.1.0. Use the versioned URL above and the [1.1.0 release](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.1.0) only after the tag and assets are available. A local build does not establish publication. Local acceptance uses the complete directory built from this source.

Install the entire Skill directory, preserve existing edits, and verify VERSION after refreshing the host. The asset is `medical-illustration-1.1.0.zip` with its `.sha256` checksum. Source code archives contain the whole repository.

The bundled Illustrator dispatcher supports macOS and requires the application and Automation permission. Static preflight works without Illustrator; the optional crop helper requires Pillow. Windows/Linux users can use the SVG/vector workflow or a separately verified host adapter for native AI output. Image services, fonts and commercial licenses are not bundled.

[中文主页](README.md) · [English homepage](README.en.md)
