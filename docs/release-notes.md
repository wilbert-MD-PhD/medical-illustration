# Medical Illustration v1.3.3

修复运行 Illustrator 预检后，回退因 Python 自动缓存而误报本地修改的问题。

- 回退的修改判定忽略 `__pycache__`、`.pyc`、`.pyo` 和 `.DS_Store`，兼容已有事务记录。
- 正文、脚本、用户新增文件和 `SHA256SUMS` 的真实修改仍受保护。
- 备份保留所有文件。并发修改检查、备份完整性及恢复校验继续使用完整哈希。
- 新增真实预检后回退、缓存增删改及真实修改保护回归测试。

## 安装

附件为 `medical-illustration-1.3.3.zip` 与同名 `.sha256`。安装与更新步骤见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.3/INSTALL.md)。

## English

Fix rollback being blocked by runtime caches created during normal use, including Illustrator preflight. Change detection now excludes `__pycache__`, `.pyc`, `.pyo` and `.DS_Store` from both current and historical snapshots. Real content changes, including `SHA256SUMS`, remain protected. Backups retain every file, and concurrency, backup integrity and restoration checks still compare complete fingerprints.
