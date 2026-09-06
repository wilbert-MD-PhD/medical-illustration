# v1.0.0-rc.4

本版补充返修规则，并把面向 Codex 使用者的安装简化为一个准确链接。

- 首页优先展示“在 Codex 中粘贴两行文字”的安装方式，提供可转发的 INSTALL.md；ZIP 与 Marketplace 保留在展开说明中。
- 纯文字、标签和气泡返修明确读取排字规范；医学变更只使受影响内容的批准失效。
- 缺少医学母版时，允许在已授权范围内依据合格参考重建待审线稿；参考不足时只阻断依赖它的部分，不以位图补丁代替重建。
- 修复校验清单忽略子目录同名 SHA256SUMS 文件的问题，增加“多余文件与后续篡改均被发现”的回归测试。
- CI 的 checkout、setup-python 和 upload-artifact 更新到 Node.js 24 版本，并固定到已核对的提交。
- 保留 rc.3 的 Unicode ZIP、源码/附件一致性与跨平台检查。

手动安装选择 `medical-illustration-1.0.0-rc.4.zip`。Source code 包含完整 Marketplace 仓库，Skill 位于 `plugins/medical-illustration/skills/medical-illustration/`。

验证包括初始化器、发布边界、文件校验、资源链接和公开附件回验；运行结果见 Actions。完整医学制图、原生 .ai 和独立新会话行为仍按 docs/validation.md 的范围分别验收，软件测试不能代替人工医学批准。
