# Medical Illustration v1.3.2

修复发布检查将 Markdown 链接标题误当作文件路径的问题。带标题的链接在目标文件存在时现在可以通过检查。

- 支持双引号、单引号和括号标题。
- 正确提取尖括号中的路径，以及包含百分号编码空格、转义括号或嵌套括号的路径。
- 保留缺失文件与越界路径检查，新增回归用例。

## 安装

附件为 `medical-illustration-1.3.2.zip` 与同名 `.sha256`。安装与更新步骤见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.2/INSTALL.md)。

## English

Fix false broken-link errors for Markdown inline links with optional titles. The release checker now extracts the destination separately from double-quoted, single-quoted or parenthesized titles. Angle-bracket destinations, percent-encoded spaces, escaped parentheses and nested parentheses are covered by regression tests. Missing files and paths outside the checked root remain rejected.
