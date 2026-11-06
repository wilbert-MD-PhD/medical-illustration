# Medical Illustration v1.3.7

修复机制图关系校验：当 `relation` 误填为数组或对象时，检查器会报告字段错误，并继续检查其余关系。新增无效类型和有效数据的回归测试。

## 安装

附件为 `medical-illustration-1.3.7.zip` 和同名 `.sha256`。详见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.7/INSTALL.md)。

## English

Fix mechanism graph validation to report invalid relation types without stopping validation of the remaining edges.
