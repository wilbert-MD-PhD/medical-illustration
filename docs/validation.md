# 验证范围

检查日期：2026-09-10。本地 macOS；软件包检查、示例制作和人工医学审签分别记录。

| 检查 | 结果 |
|---|---|
| 版本、Skill/插件入口、资源链接与 SHA-256 | 通过；独立 Skill 的 24 个载荷文件及清单一致 |
| 初始化器 | 12 项测试通过，覆盖用户改动保护、补齐文件、中文与非 UTF-8 控制台、异常路径和模板署名 |
| 发布工具 | 10 项测试通过，覆盖目录构建、不覆盖交付、Unicode ZIP 临时往返与可重复性、篡改/越界拒绝、源目录及符号链接边界、退役示例禁止发布 |
| 可选 Illustrator 辅助库 | 语法检查通过；Illustrator 29.4.0 宿主调用超时（-1712），该库的原生 AI/PDF 验收未完成 |
| 创可贴漫画 | 已完成实际参考下载、看图、附图生成、返修及本例专用 JSX 排版；AI 文件重开检查通过，PDF 已渲染查看 |
| TFCC 展示 | 五个图像/PDF 文件保持已公开文件的原始哈希，未新增医学批准 |

## 漫画制作证据

[创可贴漫画](showcase/bandage/README.md)的三张重点参考保留原始 URL、许可、下载哈希及成功生图调用记录。最终 AI 文件包含 22 个可编辑文本框、16 个半透明圆角框、6 个说话尾巴、1 个嵌入底图，无外链图像；PDF 为单页 561 × 701 pt。

本例使用专用 JSX 完成排版，有用户反馈参与。其结果不代表随包通用 Illustrator 辅助库、所有图像模型或独立新会话行为已经通过验收。作品人工医学审签仍待完成。

## 尚未完成的验证

仓库配置了 Windows、macOS、Linux 与 Python 3.9/3.13 的 CI 矩阵；每个提交的跨平台结果见 [Validate 工作流](https://github.com/wilbert-MD-PhD/medical-illustration/actions/workflows/validate.yml)，正式版标签与附件构建结果见 [Release 工作流](https://github.com/wilbert-MD-PhD/medical-illustration/actions/workflows/release.yml)。Marketplace 安装、独立新会话行为及通用 Illustrator 辅助库宿主验收未完成。

软件测试不代替作品医学审签或印前批准。完整的行为验收还需检查参考复用、参考缺失处理、文字空间不足时的修订、局部返修范围以及工具缺失时的真实状态记录。
