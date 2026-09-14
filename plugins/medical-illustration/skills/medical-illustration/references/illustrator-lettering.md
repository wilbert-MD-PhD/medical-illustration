# Illustrator 可编辑排字辅助库

[scripts/illustrator-lettering.jsx](../scripts/illustrator-lettering.jsx) 是可选 ExtendScript 库。加载时不创建或修改文档，调用时才工作；需要 Adobe Illustrator，不是独立 Node 程序。不设固定分镜、标题栏或页脚。使用前完成[文字空间规划与试排](text-space-and-visible-copy.md)。

坐标为 pt，原点在本页左上角，文字 y 值为基线。将以下占位路径换成实际位置，通过[受管运行器](illustrator-runtime.md)执行自己的调用文件；要求 IllustratorSession.current 已建立：

```javascript
#target illustrator
$.evalFile(File('/path/to/medical-illustration/scripts/illustrator-lettering.jsx'));
var book = ComicPage.create({width:420, height:588,
    fontRegular:'Your-Regular-PostScript-Name', fontMedium:'Your-Medium-PostScript-Name'});
book.page('P001', '/path/to/page-base.png');
book.text('实际标题', 26, 32, {size:18, bold:true});
book.bubble('第一行对白\n第二行对白', [30,55,180,48], [90,120], {size:11, fillOpacity:60});
book.text('实际标签', 80, 280, {size:11, label:true});
book.line([[100,286],[140,305]], {width:0.8});
book.save('/existing/output/page-v1.ai', '/existing/output/page-v1.pdf');
```

- 字体参数是实际 PostScript 名称；未指定时尝试 LXGWWenKai-Regular / LXGWWenKai-Medium。缺字体明确报错，不静默替换。字体文件不随包分发。
- `page` 链接底图，`save` 在原生 AI 中嵌入，比例不匹配时报错，不拉伸解剖；ID 仅作画板元数据。省略图片只得到空白画板。
- `text` 保留可编辑文字；`line` 按输入点建立路径，不推断医学箭头方向。标签端点需实际看图核对。
- `bubble` 用同一轮廓绘制主体/尾巴，底色默认 60% 不透明度，文字和边线为 100%。当前只支持上/下尾巴；左右或曲线尾巴由编辑器调整。超宽/超高文字报错，需改行或重新布局。
- `save` 要求输出目录已存在，并拒绝覆盖同名 AI/PDF。工作规格不是印刷批准；导出后必须重开 AI、实际查看 PDF、核对字体/透明度与医学内容。
- 报错由受管会话尝试恢复保存和关闭；恢复失败保留文档并报告。本库不承诺事务回滚。`pages` 和 `textRecords` 可供调用方保存记录。

1.0.0 历史宿主验收曾超时；1.1.0 已改用显式文档会话。当前验证范围见维护仓库 docs/validation.md，不将语法检查或 SVG 渲染替代原生宿主验收。
