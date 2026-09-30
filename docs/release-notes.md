# Medical Illustration v1.3.1

修复发布包完整性检查：缺少 `scripts/check_mechanism_graph.py` 时，即使重新生成 SHA256SUMS，发布检查也会明确报错并阻止构建。新增回归测试覆盖这一情形。

本版同时包含 main 分支此前已合入的许可更新：自有核心 Skill、脚本及运行模板采用 MIT，原创文档、漫画和展示贡献采用 CC BY 4.0，第三方材料保留原许可。初始化器为新项目复制完整 MIT 声明并保留已有文件。

## 安装

附件为 `medical-illustration-1.3.1.zip` 与同名 `.sha256`。安装与更新步骤见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.1/INSTALL.md)。

## English

The release check now rejects packages missing `scripts/check_mechanism_graph.py`, even when SHA256SUMS has been regenerated. A regression test covers this failure mode.

This release also includes the licensing changes previously merged into main: MIT for the original core Skill, scripts and runtime templates; CC BY 4.0 for original documentation, comics and showcase contributions. Third-party materials retain their respective licenses. New projects receive the complete MIT notice without overwriting existing files.
