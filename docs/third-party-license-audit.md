# 第三方许可清单与待处理项

审计日期：2026-09-27。范围为当前维护仓库及其公开示例，不覆盖本地全部历史项目、参考书库或外部依赖的每个版本。核对现有 CREDITS、sources.json、reference-map.json、实际文件哈希和 PDF 字体表。本次在线复核 MIT、CC BY 4.0、BodyParts3D 和霞鹜文楷官方许可，其余图源沿用原制作凭据，不声称全部重新在线确权。

## 处理结论

现有公开素材记录中未发现明确采用 NC 的第三方条目。旧 CC BY-NC-SA 限制来自自有内容声明，现已按作者授权调整。以下待处理项保持现状，尚未替换、移除或申请授权。

| 编号 | 文件或组成部分 | 已知状态与缺口 | 后续选项 |
|---|---|---|---|
| U01 | `showcase/tfcc/base-1.png`、`base-2.png`、`page-1.jpg`、`page-2.jpg`、`review.pdf` | 作者提供作品，原始参考图、角色来源及实际输入链未随公开材料登记。原创贡献可按 CC BY 4.0 授权，混合成品尚不能确认全部素材权利 | 补原制作来源与授权记录，再决定保留、替换或移除受影响部分 |
| U02 | `showcase/wrist/comparisons/reference-details.pdf`、五张对照 PNG 中 HarmonyOS Sans SC 排字 | pdffonts 确认 PDF 嵌入 Regular、Medium 子集，仓库未附本次所用字体版本的许可凭据。未认定为 NC | 补对应字体包原许可，或重排为已有 OFL 凭据的字体 |
| V01 | `showcase/wrist/scaffolds/`、`artwork/`，及其在对照图和漫画中的出现 | 现官网 CC BY 4.0 与记录中的旧 OBJ 头 CC BY-SA 2.1 JP 不同。本批继续保留 BY-SA 2.1 JP。SA 本身不等于 NC | 按已记录 SA 条款复用，或取得适用于具体旧包的许可确认后再调整。不得直接统一改标 CC BY 4.0 |

TFCC PDF 已识别为 LXGW WenKai / WenKai Mono 的 Regular、Medium、Light 子集，官网为 OFL 1.1，不再将字体家族列为未知。精确字体版本与原包仍建议归档。合成图和 PDF 的原创许可不能消除其第三方部件条款。

## 已登记素材（逐文件哈希见附表）

| 素材 | 保留许可 | 来源与具体使用记录 |
|---|---|---|
| 创可贴 R05 Nike 2022 Fig.1 | CC BY 4.0 | [CREDITS](showcase/bandage/CREDITS.md)、[来源记录](showcase/bandage/sources.json) |
| 创可贴 R11 Wang 2022 Fig.1 | CC BY 4.0 | 同上 |
| 创可贴 R02 NIAID Macrophage | Public Domain，保留来源署名 | 同上 |
| Gray219、Gray220、Gray336 | Public Domain，保留来源署名 | [腕骨 CREDITS](showcase/wrist/CREDITS.md) |
| Springer Fig.4.18、Fig.4.19 所在书页 | CC BY 4.0，依原记录核对图注排除项 | 同上 |
| Delva 2020 Fig.1、Zhang 2024 Fig.1 | CC BY 4.0，沿用原凭据 | 同上 |
| BodyParts3D M01/M02/M03/M04/M06 与 B01–B05 | 本批保留 CC BY-SA 2.1 JP | 同上及 [reference-map](showcase/wrist/reference-map.json) |
| LXGW WenKai / WenKai Mono 嵌入子集 | SIL OFL 1.1 | [官方许可](https://github.com/lxgw/LxgwWenKai/blob/main/OFL.txt)，2026-09-27 查看官网与实际 PDF 字体表 |
| HarmonyOS Sans SC 嵌入子集与栅格排字 | 原字体条款，具体版本凭据待补 | U02 |

创可贴其他实际生成输入 R01（NIAID，Public Domain）、R07（Kim 2017，CC BY 4.0）及仅内部核对素材继续保留 [CREDITS](showcase/bandage/CREDITS.md) 中的逐项记录。它们未作为独立原图分发在本仓库，使用方式不能据此改写。SMART-Servier 吞噬图沿用该文件的 CC BY-SA 3.0，不替换成网站其他版本许可。

## 文件级清单

[third-party-assets.json](third-party-assets.json) 列出所有公开示例 PNG/JPG/PDF 的路径、大小、SHA-256、许可范围与证据文件。混合产物注明组成部分条款，未将整件标为纯 CC BY。参考文件的原作者、URL、图号和修改方式继续以各示例 CREDITS 为准。

## 依据

- [MIT 正文](https://opensource.org/license/mit)
- [CC BY 4.0 正文](https://creativecommons.org/licenses/by/4.0/legalcode)
- [BodyParts3D 官方许可](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html)

字体和图源版权、来源说明保留。后续处理 U01/U02 时先形成具体替换或移除清单，再更新文件、示例来源映射及本表。
