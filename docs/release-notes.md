# Medical Illustration v1.0.0-rc.5

用于 Codex 的医学科普插画与漫画工作流程。首次使用请打开 [安装与依赖检查说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/main/INSTALL.md)，复制整段给 Codex。

## 手动下载选哪个

| 文件 | 用途 |
|---|---|
| medical-illustration-1.0.0-rc.5.zip | 完整独立 Skill，手动安装选此文件 |
| medical-illustration-1.0.0-rc.5.zip.sha256 | ZIP 校验文件，无需作为 Skill 安装 |
| Source code | 完整仓库，包含主页示例；Skill 位于 plugins/medical-illustration/skills/medical-illustration/ |

## 本版更新

- 新增首次环境检查：图像工具、中文字体、可编辑排字和 PDF 导出须分别验收。
- 补齐按需安装免费组件的指引，说明哪些权限、软件与人工审核不能由 Skill 安装提供。
- 更新可直接转发的安装与使用说明。
- 发布标签包含作者提供的两页 TFCC 主页示例；展示素材位于仓库 docs/showcase，不增加独立 Skill 安装包体积。

包结构、初始化器、校验和、Unicode 解压与跨平台验证见 Actions。图片生成能力因使用者环境而异；完整医学制图、新会话行为和人工审签不以软件测试代替，范围见 [验证说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.0.0-rc.5/docs/validation.md)。
