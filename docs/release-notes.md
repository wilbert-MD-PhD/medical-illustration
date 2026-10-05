# Medical Illustration v1.3.4

修复同版本更新时，缺失或损坏的 `SHA256SUMS` 未被恢复，却返回 `already_current` 的问题。

- 只有本地完整性为 `clean` 且载荷相同时，才跳过替换。
- 清单缺失、格式损坏或哈希错误时，明确使用 `--replace-local` 后备份原安装并恢复完整包。
- 未明确选择替换时继续保护本地文件。完整安装重复更新仍不创建额外备份。
- 新增三种清单异常的回归验证，覆盖原文件保护、备份内容、修复结果和重复更新。

## 安装

附件为 `medical-illustration-1.3.4.zip` 与同名 `.sha256`。安装与更新步骤见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.4/INSTALL.md)。

## English

Fix same-version updates returning `already_current` while leaving a missing or damaged `SHA256SUMS` unrepaired. A no-op now requires a clean local integrity check as well as matching payloads. Explicit `--replace-local` repairs missing, malformed or incorrect manifests through the existing backup-and-replace transaction. Local edits remain protected by default, and repeated updates of a clean installation remain no-ops.
