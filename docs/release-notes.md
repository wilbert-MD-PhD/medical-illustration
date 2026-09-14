# Medical Illustration v1.1.2

修复默认提示词偏向科研图、初始化器用途与分支规则不一致的问题，并明确旧安装的完整包升级与验收。

- 默认提示词依据用户实际任务选择漫画、医学插画或科研绘图分支。
- 初始化器帮助、项目说明、Skill 入口和安装文档统一限定为漫画与医学插画；独立科研图沿用专用流程。
- 完整包包含文字空间、无气泡生图规则、更新器及三个许可文件；这些已有能力通过完整升级进入旧安装，无需逐文件手工补丁。
- 安装验收检查实际安装目录的 VERSION、清单差异和许可文件，避免把维护源码更新当成安装已更新。旧目录完整备份，已有项目不迁移。

## 安装与升级

见 [1.1.2 安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.1.2/INSTALL.md)。已具备更新器的独立安装可说“更新医学绘图 Skill”；1.1.0 及更早版本先从完整新包取得更新器，显式指定旧安装目录。缺版本或有效基线时先检查差异，按用户授权完整备份后替换。

附件为 `medical-illustration-1.1.2.zip` 与同名 `.sha256`；ZIP 是更新器所需的独立安装包。GitHub Source code 为完整仓库。插件管理的安装由宿主更新。

[验证范围](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.1.2/docs/validation.md)区分包校验、回归测试、宿主及医学审核。本次不重新生图或执行 Illustrator；更新完成后刷新宿主并核对实际加载版本。

## English

Version 1.1.2 makes the default prompt select the appropriate comic, medical illustration, or research figure workflow. The initializer help, generated project description, and documentation now consistently limit the scaffold to comics and medical illustrations; standalone research figures use their dedicated workflow.

Upgrade the entire package to receive the existing text-space rules, bubble-free generation guidance, updater, and license files. Verify the actual installed directory, not just the source checkout. Standalone updates preserve a complete backup; project files remain in place. Refresh the host and verify the loaded version after installation. This patch does not claim new image-generation, Illustrator host, medical, or prepress approval.
