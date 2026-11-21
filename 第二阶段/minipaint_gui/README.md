# miniPaint GUI 自动化绘图基线

用 Playwright 驱动本地部署的 miniPaint：自动新建画布、按预先算好的坐标数据逐笔画出线条，最后导出 PNG 并独立校验结果。

属于「观测 — 决策 — 执行 — 验证」闭环里的**执行 + 验证**两段：动作坐标事先准备好，程序负责把它们准确执行、留下日志、检查产物，而不是以"脚本没报错"当作成功。

对应培养方案「第 5 周：GUI 自动化与固定环境操作」的阶段交付，也可作为第 8 周综合项目的基线。

## 运行

```bash
python src\run.py
```

- 依赖：Python 3、Playwright（`pip install playwright` 然后 `playwright install chromium`）
- miniPaint 静态文件需放在 `env\miniPaint-master`

全程约 17 分钟（1.1 万多个绘制点），中途不输出进度属正常。

## 代码结构

| 文件 | 作用 |
| --- | --- |
| `src/run.py` | 主流程入口：建画布 → 绘制 → 导出 → 校验 |
| `src/server.py` | 本地起静态服务器托管 miniPaint |
| `src/browser.py` | 启动浏览器，固定窗口 1400×1600 |
| `src/locator.py` | miniPaint 界面元素的选择器，集中在一个文件 |
| `src/actions.py` | 界面动作：新建画布、选笔刷、按坐标画线、导出 |
| `src/trace.py` | `Trace` 类，记录每步动作、耗时与结果 |
| `src/verify.py` | 独立校验：导出尺寸、是否空白 |
| `src/sketch_data.py` | 线条坐标数据（归一化到 0~1000） |
| `src/config.py` | 路径、端口、窗口尺寸、超时 |

## 输出

每次运行在 `output\run_<时间戳>\` 下生成三件产物：

- `after_draw.png` — 画完后的界面截图
- `result.png` — 导出的最终图片
- `trace.json` — 各步骤是否成功、耗时、点数与校验指标

## 成果

![导出结果](docs/images/09_result.png)

1200×680，293 条线 / 11514 个点，非白像素占比 0.22，尺寸校验通过。

## 已知局限

- 线条位置来自预先提取的坐标，不是由模型看界面后决策，因此本仓库不含「决策」环节。
- 导出为位图，线条粗细统一，与手绘观感有差距。
- 跑完全程约 17 分钟，缺少中间进度提示；`trace.json` 中 `export` 一步的 `ms` 记的是累计耗时，不能当作该步单独耗时看。
