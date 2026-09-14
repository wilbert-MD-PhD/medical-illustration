# Illustrator 运行与收尾

只管理本次调用显式创建或打开的文档，保存后关闭这些文档，保留应用和原有标签。

## 平台与依赖

完整 Skill 包含 `scripts/illustrator_run.py`、`illustrator_preflight.py` 与 `illustrator_session.jsx`，三者保持同一目录；运行器和预检只需 Python 3.9+ 标准库。可选的 `illustrator_assets.py` 裁切工具还需要 Pillow。

自动派发使用 macOS 的 AppleScript、Adobe Illustrator 和正常的系统自动化权限。Windows/Linux 可以运行 `--check-only` 和包级测试，不能用此适配器自动派发。其他平台可用[首次环境检查](first-run.md)中的 SVG/矢量工作流；需要原生 AI 时使用宿主已验证的受管适配器并实际验收。静态检查通过不表示 Illustrator 已就绪。

宿主/项目已明确指定同等串行运行器时，沿用其实际入口，不替换全局安装。所有同一 macOS 用户下的副本共用一把锁，不得并行绕开。

## 调用

从实际 Skill 根目录执行，或使用该安装目录的真实脚本路径。任务和运行目录由当前项目提供；新运行目录必须尚不存在。

```sh
python3 scripts/illustrator_run.py /path/to/job.jsx --check-only
python3 scripts/illustrator_run.py --status
python3 scripts/illustrator_run.py /path/to/job.jsx --run-dir /path/to/new-run --timeout 600
```

预检递归检查绝对路径字面量的 JSX 依赖；拒绝直接 app.open、app.documents.add、按 SaveOptions 直接关闭文档、activeDocument 和 app.quit。动态路径、别名和代码需另查；预检不是安全沙箱。

任务 JSX 由运行器加载，不自行再包一层 session.run：

```javascript
var s = IllustratorSession.current;
var d = s.create(DocumentColorSpace.RGB, 420, 588);
// 在 d 上排字或绘图；输出目录先创建，路径换成当前项目的新版本。
s.saveOutputs(d, '/path/to/new-page.ai', '/path/to/new-page.pdf', '1');
s.close(d);
d = null;
```

运行目录保存预检、wrapper、派发输出、进度、完成记录和恢复 AI。使用可选[排字库](illustrator-lettering.md)时，也在该会话中调用。

## 文档归属与保存

- `s.create` 或 `s.open(path, 'work'/'read')` 显式登记文档。已打开目标拒绝接管；要修改时先建立独立工作副本。不得按名称或全体差集认领。
- `s.saveOutputs` 要求新的 AI/PDF 路径，原生 AI 保存后 checkpoint，再导出 PDF；嵌入链接，PDF 不自动打开。自定义 saveAs 后调用 `s.checkpoint`，它只验证路径、非空和保存状态。
- `s.close` 只关闭已登记且妥善保存的文档。重开用 `s.open(path, 'read')`，逐个检查、关闭；关闭后不用旧 DOM 引用。
- 未保存工作由 finally 尝试另存恢复 AI，成功才关闭并报告未完成；恢复失败保留文档并报错，不能丢弃未保存内容。应用崩溃不能保证执行 finally。
- 交互设置由 finally 恢复；默认临时隐藏提示，所以输入、字体与输出冲突必须先查。不要批量修改软件偏好。
- `s.textSummary` 返回关闭后仍可使用的纯数据；不替代字体、溢出、视觉、医学或印前检查。`embed/remove/createOutline/close` 后不用旧对象，逐字符扫描仅用于已定位问题。

## 锁与异常

macOS 锁为 `/private/tmp/codex-illustrator-<用户UID>.lock`，跨项目、跨安装副本共用。

| 退出码 | 含义 |
|---|---|
| 0 | 宿主返回匹配完成记录，脚本与收尾完成 |
| 1 | 脚本/恢复过程报错，但宿主已返回完成记录；检查恢复文件和保留文档 |
| 2 | 超时或派发未确认，锁保留；参数/不支持平台错误也用此码，按输出区分 |
| 65 | 静态预检失败，尚未派发 |
| 75 | 已占锁，尚未派发 |

超时不表示 Illustrator 已停止。先读 owner.json、completion.txt、派发输出、progress.txt 与应用状态，确认旧调用已结束且未保存文档已处理，再清理这一把已失效锁并记录依据。不能仅按 PID 消失判断 AppleEvent 已停止；无自动解锁、强退或超时抢锁。

## 可选裁切工具

`scripts/illustrator_assets.py` 不依赖作者项目配置。矩形以左上角为原点，canvas 是原始置入画布宽高，clip 为 x、y、宽、高，单位一致：

```sh
python3 scripts/illustrator_assets.py /path/to/source.png --canvas 420 588 --clip 40 60 120 80 --output /path/to/crops
```

也可导入 `crop_asset(source, canvas, clip, output)`。不覆盖原图、不重采样，保留 ICC，返回源/裁图哈希、像素盒与置入位置。实际图片须有对应授权；继续保留原蒙版，不把裁图拉伸到旧整页框。
