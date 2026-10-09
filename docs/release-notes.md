# Medical Illustration v1.3.5

修复更新器会接受缺少必需脚本、但内外校验和一致的安装包，替换后仍显示 `clean` 的问题。

- 在替换安装前独立检查必需组件，缺失时报告具体路径并保留现有安装。
- 校验排字库，以及从 1.1.0 引入的 Illustrator 运行组件和机制校验器、从 1.1.1 引入的更新器；同一数字版本的 RC 使用相同要求。
- 保留旧版包兼容性、无更新器旧安装的接入、完整备份和回退。OpenAI 界面元数据仍为可选。
- 新增重新生成内外校验和后的残缺包拒绝、版本边界和旧安装升级/回退测试。

## 安装

附件为 `medical-illustration-1.3.5.zip` 与同名 `.sha256`。安装与更新步骤见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.5/INSTALL.md)。本修复在 1.3.5 更新器中生效；旧安装完成升级后，后续更新将使用新的组件检查。

## English

Fix the updater accepting incomplete packages with matching inner and outer checksums. It now checks required scripts before replacing an installation and reports any missing component. Requirements follow the component's introduction version, including release candidates, while preserving legacy package support, bootstrap updates, complete backups and rollback. Optional OpenAI UI metadata remains optional.
