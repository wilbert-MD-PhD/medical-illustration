# 安装并开始使用 Medical Illustration

打开 **Codex 桌面端**，选择一个保存漫画的本地文件夹，把下面整段发给 Codex：

```text
请使用 $skill-installer 安装医学绘图 Skill：https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.0.0-rc.5/plugins/medical-illustration/skills/medical-illustration
安装到我的个人技能目录，保留已有改动。安装后读取其中 references/first-run.md，检查并补齐当前任务需要的免费依赖，验证中文排字和 PDF 导出，并确认当前 Codex 是否能实际生成图片。需要登录、付费或配置密钥时告诉我具体操作，不要把“安装成功”当成“能出图”。最后告诉我如何启用 Skill，并询问漫画主题、读者和页数。
```

安装后按 Codex 提示刷新技能；若未出现，重启 Codex。然后发送你的需求，例如：

```text
使用 $medical-illustration，为普通读者制作两页关于【我的主题】的医学科普漫画。
先核验依据和分镜，再制作无字底板、独立可编辑的中文文字层和 PDF 审阅稿。
医学审核未完成的内容标为待审；先完成不受阻的草稿部分。
```

## 安装后应得到什么

- Skill 的实际安装路径、版本及文件校验结果。
- 图像生成、中文字体、可编辑排字与 PDF 导出的可用性结果；排字和 PDF 要有实际测试文件。
- 只有在图像工具成功返回测试图后，才把“图片生成”标记为已实测。优先复用本次会话已成功的结果；新增测试可能消耗额度，按当前授权执行。
- 如有缺口，明确下一步是登录、启用工具还是配置本地密钥；不在对话中发送密钥。

Skill 是工作流程。它不能为账号增加图像生成权限，也不附带 Illustrator 许可证、医学图谱或人工审稿人。Python 初始化器只用标准库；`humanize-writing`、`baoyu-comic`、Illustrator 都不是普遍必装项。具体免费替代路径见 [首次环境检查](plugins/medical-illustration/skills/medical-illustration/references/first-run.md)。

需要能访问本地文件和 GitHub 的 Codex 环境。已有同名版本先核对路径和本地改动，避免重复安装。

## Release 页的下载文件

- **medical-illustration-1.0.0-rc.5.zip**：完整独立 Skill，手动安装选它。
- **.zip.sha256**：ZIP 完整性校验文件，无需作为 Skill 安装。
- **Source code**：整个仓库，包含主页素材；不是独立 Skill ZIP。

[主页示例](README.md#看看实际产物) · [手动下载](https://github.com/wilbert-MD-PhD/medical-illustration/releases/tag/v1.0.0-rc.5) · [官方 Skill 说明](https://developers.openai.com/codex/skills/)
