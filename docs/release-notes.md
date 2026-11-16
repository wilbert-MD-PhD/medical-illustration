# Medical Illustration v1.3.9

修复 Illustrator 预检将正则表达式中的引号误判为字符串、从而漏查后续受限制调用和依赖的问题。无法可靠区分的斜杠语法会中止派发并提示改写。

## 安装

附件为 `medical-illustration-1.3.9.zip` 和同名 `.sha256`。详见 [安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.3.9/INSTALL.md)。

## English

Fix Illustrator preflight so quotes in regular expression literals do not hide subsequent restricted calls or dependencies. Ambiguous slash syntax stops dispatch for review.
