# 项目示例：通用人类医生讲解腕骨与关节

需要解释“解剖结构怎样得到可信参考约束”，或为漫画建立逐结构来源对应时，使用本例。它是《腕骨与关节组成》六页漫画的独立 Skill 示例 v1.1：通用人类医生与阿旋讲解，5 幅原解剖图保留在 6 处放置，中文对白、标签与引线后期排版。

## 从成图追溯到依据

以下对应来自本例原解剖彩稿的实际生成附件记录。图谱/教材提供医学关系依据；M01–M04 是右侧 BodyParts3D 模型投影，M06 是解释性冠状定位线稿；B01–B05 是生成彩稿。

| 成图位置与资产 | 要核对的关系 | 图谱/教材实际附件 | 其他输入与支持范围 |
|---|---|---|---|
| 第1页 B01，全手掌面 | 指骨、掌骨、腕骨及前臂骨的分区与邻接 | Gray219；《Wrist and Hand》书页52，Fig.4.18 | M01 约束右手几何和机位。教材图只补充腕部关系，不覆盖整只手的所有细节 |
| 第2页 B02，腕骨掌面 | 两排腕骨、邻接和豌豆骨的掌侧遮挡 | Gray219；书页52，Fig.4.18 | M02 约束几何；教学色组、编号在制作中另加 |
| 第3页上 B03，腕骨背面 | 背面可见形态与掌侧结构遮挡 | Gray220；书页52，Fig.4.18 | M03 提供背面投影。图源页面有掌背描述冲突，方向按实际图像、模型与教材核对 |
| 第3页下 B04，掌尺侧 | 三角骨与豌豆骨的前后位置 | 书页52 Fig.4.18；书页53 Fig.4.19a | M04 提供掌尺侧投影。两张教材图属同一来源，不算两份独立证据 |
| 第4–5页 B05，冠状定位 | 桡骨、近排腕骨、尺侧关节盘及接口位置 | Gray336；书页53，Fig.4.19a | M06 是解释性线稿；同次附入 B02 只为配色，不作为医学证据 |

第5页动作另有 Delva 等（2020）及 Zhang 等（2024）的 Fig.1 真人动作附件，只约束可见手形和动作方向，不支持临床动作幅度或疗效结论。第6页圆片是教学道具，不冒充骨骼形态。

## 可信来源与具体定位

- Henry Gray. *Anatomy of the Human Body*. 1918，图版219、220、336。原图入口：[Gray219](https://commons.wikimedia.org/wiki/File:Gray219.png)、[Gray220](https://commons.wikimedia.org/wiki/File:Gray220.png)、[Gray336](https://commons.wikimedia.org/wiki/File:Gray336.png)。本例保留原方向，核对时明确左右手与观察角度的差别。
- Omid Khalilzadeh, Clarissa Canella, Laura M. Fayad. *Wrist and Hand*. In: *Musculoskeletal Diseases 2021–2024: Diagnostic Imaging*. Springer, 2021. DOI [10.1007/978-3-030-71281-5_4](https://doi.org/10.1007/978-3-030-71281-5_4)。[开放章节](https://www.ncbi.nlm.nih.gov/books/NBK570159/)；[Fig.4.18](https://www.ncbi.nlm.nih.gov/books/NBK570159/figure/ch4.Fig18/) 用于掌背侧腕部关系，[Fig.4.19a](https://www.ncbi.nlm.nih.gov/books/NBK570159/figure/ch4.Fig19/) 用于尺侧软组织关系。书页52/53对应本地章节 PDF 第12/13页；完整书页曾附入生成，采用范围限于相关示意子图。
- BodyParts3D，© The Database Center for Life Science（DBCLS），本例使用 v4.0 简化99模型的右手与远端前臂部件。[官方来源与许可](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html)。模型是有出处的几何来源，不是实物照片或文献结论；具体资产按其版本和许可记录处理。
- Delva ML, Lajoie K, Khoshnam M, Menon C. *Wrist-worn wearables based on force myography: on the significance of user anthropometry*. 2020;19:46. [PMID 32532358](https://pubmed.ncbi.nlm.nih.gov/32532358/)，DOI 10.1186/s12938-020-00789-w。
- Zhang X, Li T, Sun M, Zhang L, Zhang C, Zhang Y. *Replay-Based Incremental Learning Framework for Gesture Recognition Overcoming the Time-Varying Characteristics of sEMG Signals*. 2024;24:7198. [PMID 39598975](https://pubmed.ncbi.nlm.nih.gov/39598975/)，DOI 10.3390/s24227198。

2026-09-14 重查了教材元数据、相关图注与许可页，以及两项动作研究的 PubMed 元数据；这不表示重新完成两项研究的全文核查。

## 在其他作品中复用的方法

1. 按医学对象列出需要解释的结构关系，给出成图位置和具体图号/书页，记录每个来源能支持的范围及未覆盖内容。
2. 实际看参考。用于生成的图片保存文件、版本、SHA-256 与调用附件清单；仅用于人工核对、几何约束或配色的材料分别注明用途。
3. 成图后对照实际结构、侧别、方向、遮挡和标注。展示裁图另外记录坐标，不冒充原始生成附件；不为制造一致性而静默镜像参考图。
4. 改编角色时保护已确认的解剖底图并继承来源链。本例 v1.1 保留 5 幅底图及 6 处放置；外部标签有调整，保留核验不表示整页像素相同。

使用项目现有脚本或来源表即可，不要求为这些字段另建一套台账。完整阅读页、原图、对照图板、`reference-map.json`、`preservation-check.json` 和逐项许可保存在维护仓库的 `docs/showcase/wrist/`；本说明随 Skill 分发，不复制大体积 PDF 或第三方素材。

本例状态为**制作完成，医学待审**。来源齐全、哈希匹配与视觉对照各说明自身核验范围，不能自动推导出医学批准、全部结构无误或印前放行。
