# Medical Illustration v1.3.6

修复 Illustrator JSX 依赖预检对 JavaScript 转义路径的误判。使用转义斜杠或 Unicode 的绝对路径现在能正确解析，并继续检查依赖脚本。

本版同时发布此前合入 main 的运行器修复：保留包含占位符文字的路径，忽略注释和字符串中的假依赖，并保留对真实依赖和动态依赖的检查。

## 安装

附件为 `medical-illustration-1.3.6.zip` 和同名 `.sha256`。详见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.6/INSTALL.md)。

## English

Fix JSX dependency preflight parsing of escaped JavaScript paths, including escaped slashes and Unicode. This release also includes the previously merged fixes for wrapper paths and inactive dependency examples.
