# 机制关系与图注记录

按实际复杂度选择 Markdown 表或 JSON；不要求重复维护两份。图的尺寸/模型/读者/主旨、视觉参考及用途可链接到已有项目记录。

## 一条关系的最小记录

| ID | 起点→终点/区室 | 关系与直接性 | 证据状态/支持范围 | 来源与核验位置 | 实际图形 |
|---|---|---|---|---|---|
| 示例 | SR腔→肌浆，经RyR1 | Ca²⁺运输 | 文献共识；骨骼肌 | 已核验来源ID及正文/图号 | 带“Ca²⁺释放”的运输箭头 |

需要区分基因、蛋白、活性和细胞状态；物种/实验模型和时序在公共字段写一次，各边例外单独写。结构图源和连线证据可以是不同来源。参考登记包括本地文件、来源URL、图号/页码、用途与实际查看记录；源码/参考的哈希按项目需要保存。

## 可选机器可检格式

根对象含 `nodes`、`edges`、`sources` 三个数组，各记录含唯一字符串 `id`。节点含 `label` 和 `compartment`；来源含 `citation` 与 `checked_scope`。每条边含：

- `source`、`target`：节点 ID。
- `relation`：`activation` / `inhibition` / `association` / `transport` / `process` / `localization`。
- `evidence_status`：`established` / `observed` / `hypothesis`。
- `directness`：`direct` / `indirect` / `unspecified`；不由渲染器猜测。
- `source_ids`：来源 ID 数组，假说也记录用户提出或作者推断的来源。
- `line_style`：`solid` / `dashed` / `dotted`；此可选格式中约定假说用 dashed。
- `arrowhead`：`arrow` / `bar` / `none`。关联与定位用 none，抑制用 bar，其余用 arrow。
- 可补 `scope`、`note`、实际路径/对象 ID 等，不使用额外字段暗示已有实验证据。

这是本技能的一种记录约定，不是 SBGN 标准。检查脚本仅针对该格式。

## 图注与状态

图注按需要说明：核心机制、物种/模型、实线/虚线与符号、关键缩写、尺度/被省略中间步骤、必要来源署名。已确认的局限尽量紧贴相关机制，不用一条泛化免责声明掩盖错误。

制作记录另记：可编辑范围、实际工具/模型及输入、源文件/导出版本、结构对照结果、连线核验范围、人工医学审核状态、目标期刊政策核查。无图像生成调用时如实写未调用，而非编造模型日志。
