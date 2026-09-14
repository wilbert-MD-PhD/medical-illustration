# 图源、修改与许可

原制作核验日期：2026-09-10。2026-09-14 主页更新时，重新核对了本地附件与成图的 SHA-256、六页预览及三组局部对照；在线重查 NCBI 教材元数据、Fig.4.18/4.19 图注与许可、BodyParts3D 官方许可页，以及 [Delva 2020](https://pubmed.ncbi.nlm.nih.gov/32532358/) / [Zhang 2024](https://pubmed.ncbi.nlm.nih.gov/39598975/) 的 PubMed 元数据。原生 AI 与原始生成调用沿用既有制作核验；本次未重新生成漫画，也未重新完成两项动作研究的全文核查。此文件随六页阅读稿与主页预览一起分发。

## BodyParts3D 模型与衍生医学图

来源：**BodyParts3D，© The Database Center for Life Science（DBCLS）**。[官方数据库许可](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html)。

本批使用 v4.0 简化99模型中的右手/远端前臂部件。原模型投影改变了相机、颜色分组和输出方式；B01–B04在模型投影约束下生成彩稿，B05在冠状定位线稿及图谱约束下生成。中文标签、编号、接口线和边缘渐变随后在 Illustrator 添加。模型投影不等于实物照片，生成彩稿不代表数据库作者认可。

官方页面（更新2025-02-27，2026-09-10重新访问）标示 CC BY 4.0；本批已下载的旧 OBJ 文件头仍记载 CC BY-SA 2.1 JP。为保留本批既有来源链，`scaffolds/`、`artwork/` 及阅读稿中对应的衍生解剖图继续保留 [CC BY-SA 2.1 JP](https://creativecommons.org/licenses/by-sa/2.1/jp/) 的署名与相同方式共享说明，**不对这些部件附加仓库的非商业限制**。该条不自动覆盖独立创作的人物、文字或整个混合页面的其他组成部分。

## Gray 原图

Henry Gray，*Anatomy of the Human Body*，1918，图版219、220、336。来源页均标记公有领域：

- [Gray219](https://commons.wikimedia.org/wiki/File:Gray219.png) → `references/gray219.jpg`
- [Gray220](https://commons.wikimedia.org/wiki/File:Gray220.png) → `references/gray220.jpg`
- [Gray336](https://commons.wikimedia.org/wiki/File:Gray336.png) → `references/gray336.png`

本目录复用本地实际输入原件，不镜像重排。前两幅既有输入以 JPEG 保存；网页原文件为 PNG。网页描述中存在侧别/掌背冲突，保留原图并在对应表说明，不能根据文件名替代视觉判断。

## 开放教材图页

Omid Khalilzadeh、Clarissa Canella、Laura M. Fayad. *Wrist and Hand*. 2021. In: *Musculoskeletal Diseases 2021–2024: Diagnostic Imaging*. DOI [10.1007/978-3-030-71281-5_4](https://doi.org/10.1007/978-3-030-71281-5_4)。[NCBI开放章节](https://www.ncbi.nlm.nih.gov/books/NBK570159/)。

© The Author(s) 2021，[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。章节声明覆盖无单独排除署名的插图，本次核对的 Fig.4.18/4.19 未见排除署名：

- `references/springer-p52.png`：书页52、章节 PDF 第12页，[Fig.4.18](https://www.ncbi.nlm.nih.gov/books/NBK570159/figure/ch4.Fig18/)。
- `references/springer-p53.png`：书页53、章节 PDF 第13页，[Fig.4.19](https://www.ncbi.nlm.nih.gov/books/NBK570159/figure/ch4.Fig19/)，本例核对重点为a子图。

处理：将已获取章节渲染为 PNG，保留书页和图注；未把原书页放进漫画正文。完整书页确实曾作为图像附件传入原医学彩稿生成，相关示意图用于空间核对；公开说明不将病变 MRI 或无关子图解释为生成依据。网页图注与本地书页版本在个别 MRI 编号描述上有差异，本例不使用这些编号作论据。

## 人物、文字与字体

本例医生由 image_gen 依专用人类医生母图生成，人物及环境为 AI 生成插画；采用阿旋人物的绘画风格参考。阿旋继续沿用；用户已明确她不属于需要排除的私有资产。原豹形角色和其专属标识已从新示例画面移除，原始含角色的内部编辑输入不收入公开示例目录。

独立人物、作者文字和排版说明沿用仓库内容许可；第三方原图与衍生解剖部件按上方逐项许可处理。使用 Skill 创作的新作品不自动获得或继承本例素材许可。

正文采用霞鹜文楷（LXGWWenKai）。阅读 PDF 嵌入所需字体子集；原生文字可编辑，编辑环境需安装对应字体。本目录不分发字体二进制。

## v1.1新增动作参考

- Delva ML, Lajoie K, Khoshnam M, Menon C. *Wrist-worn wearables based on force myography: on the significance of user anthropometry*. 2020;19:46. Fig.1. DOI [10.1186/s12938-020-00789-w](https://doi.org/10.1186/s12938-020-00789-w). CC BY 4.0。文件：`references/motion-delva-fig1.jpg`。
- Zhang X, Li T, Sun M, Zhang L, Zhang C, Zhang Y. *Replay-Based Incremental Learning Framework for Gesture Recognition Overcoming the Time-Varying Characteristics of sEMG Signals*. 2024;24:7198. Fig.1. DOI [10.3390/s24227198](https://doi.org/10.3390/s24227198). © Authors 2024, CC BY 4.0。文件：`references/motion-zhang-fig1.jpg`。

两图沿用项目已获取并登记的原始文件。本轮再次查看并实际附入P005生图，用于可见手形及屈伸/旋转方向约束；成图不复制受试者身份、实验装置和原图标记。网页直接访问遇到验证/限流，当前原始元数据与许可依据沿用本地原始网页/XML凭据，不声称本轮在线页面重验成功。

2026-09-14 展示返修：对照扩为五组，新增全手骨骼与背侧腕部；使用鸿蒙黑体（HarmonyOS Sans SC）重新排版，中英文按正常字宽显示、左对齐，不使用分散字距。图片内容与观察方向不重绘、不镜像；PDF文字独立保留，字体子集嵌入，不另分发字体文件。维护入口为仓库 `scripts/build_wrist_comparisons.py`，需显式提供本机字体路径。

`comparisons/`中的图板为展示用等比裁切与排版，来源坐标和哈希见`crop-map.json`；保留各原图方向，不冒充原调用附件，也不代表原作者认可生成结果。

## 状态

当前为制作示例，医学待审。图源署名、生成记录及技术检查不构成原作者背书、医学审签或印前批准。

