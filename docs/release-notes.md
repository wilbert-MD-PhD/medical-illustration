# Medical Illustration v1.3.8

修复 Illustrator 预检漏查 `#include` 和 `$.evalFile(new File(...))` 字面量依赖的问题。预检递归检查这些依赖，缺失文件和相对路径会报错，无法识别的引入会提示另查。

## 安装

附件为 `medical-illustration-1.3.8.zip` 和同名 `.sha256`。详见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.8/INSTALL.md)。

## English

Fix Illustrator preflight to inspect literal `#include` and `$.evalFile(new File(...))` dependencies recursively and warn about unrecognized includes.
