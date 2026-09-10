# Medical Illustration · 医学绘图

**把医学知识画成读得懂的故事，把结构与机制画成看得清的图。**

Medical Illustration 是在 Codex 中使用的医学绘图 Skill。告诉它主题、读者和用途，它会帮助你查找医学参考、编写脚本、设计画面、生成插图，再完成可编辑排字和检查。

[English](README.en.md) · [安装](INSTALL.md) · [版本发布](https://github.com/wilbert-MD-PhD/medical-illustration/releases)

## 它能帮你做什么

| 你想制作 | Skill 可以帮助你完成 |
|---|---|
| 面向患者和公众的科普漫画 | 从生活情境出发，用人物对白和连续画面讲清一个医学问题 |
| 教学与宣教用的医学插画 | 依据真实参考表现解剖层次、损伤位置与修复过程，配上清楚的标签 |
| 涉及医学结构的科研示意图 | 根据你提供的研究论断与证据组织结构和机制，区分已证实关系与假说 |

你可以指定角色、画风、篇幅和输出格式。文字、气泡、医学标签及后加箭头独立编辑，后续改词、移动标注和局部返修更方便。交付可包括 Markdown 脚本、彩色画面、排版源文件和 PDF。

## 看看实际产物

### 一张创可贴下面，发生了什么？

小满折纸飞机时划伤了手指。创可贴贴好了，伤口里面又发生了什么？这篇漫画从一个生活小意外出发，带读者看到止血、清理和表皮修复。

[![一张创可贴下面，发生了什么？](docs/showcase/bandage/comic-v1.4.jpg)](docs/showcase/bandage/review-v1.4.pdf)

[阅读 PDF](docs/showcase/bandage/review-v1.4.pdf) · [查看脚本](docs/showcase/bandage/script.md) · [制作过程](docs/showcase/bandage/README.md)

### 手腕疼痛的故事

TFCC（腕关节三角纤维软骨复合体）漫画把日常动作、人物对话和手腕结构放在同一个故事里。下面两页展示了另一种画风与中文排字效果。

| 第一页 | 第二页 |
|---|---|
| [![第一页](docs/showcase/tfcc/page-1.jpg)](docs/showcase/tfcc/page-1.jpg) | [![第二页](docs/showcase/tfcc/page-2.jpg)](docs/showcase/tfcc/page-2.jpg) |

[阅读两页 PDF](docs/showcase/tfcc/review.pdf) · [示例说明](docs/showcase/tfcc/README.md)

## 绘图有参考，来源可追溯

**Skill 会引导 Codex 主动寻找、下载并查看可信医学参考，再把参考图作为附件用于绘图。** 这需要可用的联网与图像工具，以及允许相应用途的图源；已有合格参考也可以直接使用。

创可贴漫画就使用了从 **Frontiers 出版社和 NIH/NIAID BioArt** 获取的参考。以下三张医学示意图经过图注与许可核对后保存到本地，并实际作为附件传入图像生成工具：

| 伤口与上皮覆盖 | 表皮细胞与真皮 | 巨噬细胞外形 |
|---|---|---|
| [![Nike 2022 Fig.1](docs/showcase/bandage/references/R05_Nike2022_Fig1.png)](https://doi.org/10.3389/fbioe.2022.865014) | [![Wang 2022 Fig.1](docs/showcase/bandage/references/R11_Inflammatory2022_Fig1.png)](https://doi.org/10.3389/fimmu.2022.789274) | [![NIH 巨噬细胞](docs/showcase/bandage/references/R02_NIH_macrophage.png)](https://bioart.niaid.nih.gov/bioart/309) |
| Nike 等，2022，Fig.1；CC BY 4.0。用于第 3、5 格皮肤层次与伤缘覆盖关系。 | Wang 等，2022，Fig.1；CC BY 4.0。用于表皮细胞形态及与真皮的位置关系。 | Ryan Kissinger / NIAID Visual & Medical Arts；Public Domain。用于第 4 格胞体、突起和细胞核。 |

从看图到成图，还要核对具体部位与结构关系。例如，通用皮肤参考中的毛囊没有照搬到指腹；中文、气泡和标签在生成后单独排版。原始图源、下载哈希和实际绘图附件都有记录，便于复查。

[查看参考与绘图过程](docs/showcase/bandage/README.md) · [来源与许可](docs/showcase/bandage/CREDITS.md)

## 开始使用

按[安装说明](INSTALL.md)安装后，可以把这样的请求发给 Codex：

```text
使用 $medical-illustration，为没有医学背景的读者制作一页关于伤口愈合的科普漫画。
从一个生活小故事开始，画面明亮清晰，对白自然。
请查找并使用可信医学参考，交付 Markdown 脚本、可编辑排版文件和 PDF。
```

科研图可以附上研究论断、文献、结构关系和目标版式；已有脚本或图片也可以直接交给它继续制作、排字或返修。

这是制作流程 Skill，需要配合图像生成工具、可用字体及矢量/PDF 编辑环境。具体输出取决于环境能力；使用 Illustrator 格式时需要相应软件。环境配置见[安装说明](INSTALL.md)。

## 检查与使用范围

制作过程中会对照参考检查结构，检查文字排版和跨页一致性，并保存来源及修改记录。这里的漫画可供查看制作效果；医学审签状态见各示例说明，人工医学审签仍待完成。[实际验证范围](docs/validation.md)

## 许可与反馈

作者 **wilbert**。内容、模板与示例采用 **CC BY-NC-SA 4.0**，可执行代码和 CI 采用 **MIT**。第三方参考图沿用各自原许可，见[示例署名](docs/showcase/bandage/CREDITS.md)。独立创作的新作品不因使用 Skill 自动继承许可；复制使用的模板和第三方材料按各自条款处理。

[许可范围](LICENSE.md) · [第三方材料说明](plugins/medical-illustration/skills/medical-illustration/NOTICE.md) · [问题反馈](https://github.com/wilbert-MD-PhD/medical-illustration/issues) · [维护与发布](docs/maintaining.md)
