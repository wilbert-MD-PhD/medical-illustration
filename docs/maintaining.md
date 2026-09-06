# 维护与发布

仓库根是 Marketplace；插件根为 `plugins/medical-illustration/`；Skill 根为 `plugins/medical-illustration/skills/medical-illustration/`。只维护这一份可发布 Skill，独立 ZIP 从同一来源构建。

## 修改后检查

1. 需要发布新版本时，同步更新 Skill 的 VERSION、初始化器 SKILL_VERSION 和插件 plugin.json 的 version。
2. 更新 CHANGELOG、首页的固定版本下载链接和 docs/release-notes.md。
3. 改动 Skill 文件后重新生成校验清单，再运行检查：

```bash
python3 scripts/release.py manifest
python3 scripts/release.py check
python3 plugins/medical-illustration/skills/medical-illustration/scripts/test_init_medical_project.py
python3 scripts/test_release.py
python3 scripts/release.py build
```

`dist/` 中生成独立 ZIP 和附件 SHA-256 文件。构建脚本不自动修复过期的清单；它会拒绝清单与文件不一致的包。ZIP 使用稳定时间戳和 UTF-8 文件名标记，默认 Python 解压后必须通过校验与相对链接检查。

示例的 SVG 是可编辑源；更新源文件后重新生成 PNG 和 PDF，并人工查看实际渲染。示例渲染脚本需 Node.js、Playwright、Chromium 和本机 Source Han Sans CN 字体，不是安装 Skill 的依赖。详见示例目录中的说明。

## 版本发布

1. 提交完整修改，等待 main 的 Validate CI 通过。
2. 在含完整文件的同一个提交上创建与 VERSION 一致的 `v<版本>` 标签并推送。
3. Release 工作流从标签检出源码；三平台测试通过后，自动构建并发布附件。
4. 工作流会重新下载公开附件并验证。检查 Release 页上的附件及 Source code 都对应该标签。

不要移动已发布标签，不手工用其他目录替换同名附件。旧版发现问题时保留历史记录，发布新版本并在旧 Release 中补充已知问题及升级链接。

## 许可

本目录文档采用仓库内容许可；可执行脚本及 CI 配置采用 MIT。不要将患者资料、私有母版、字体二进制或凭据加入仓库。
