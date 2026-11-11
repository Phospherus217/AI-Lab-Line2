# AI-Lab Line2 第一阶段项目（已完成）

姓名：李晨辉　　学号：2026009793

基于 PyTorch 的 Fashion-MNIST 图像分类实验：MLP 基线、CNN 基线、模型对照、验证集错误分析、学习率自主实验，以及最终测试集评估。

训练全部在 CPU 上完成（本机没有可用显卡），Notebook 都已执行并保留输出。

## 1. 目录里有什么

```text
AI-Lab_Line2_DL_Stage1_李晨辉_2026009793/
├── README.md                     ← 本文件
├── 实验报告.md                    ← 完整报告
├── AI使用说明.md                  ← AI 工具使用情况
├── 实验记录.csv                   ← 9 次实验的配置和结果
├── requirements.txt
├── analysis.py                   ← 验证集错误案例 / 混淆矩阵 / 各类别准确率脚本
├── notebooks/                    ← 5 个已执行的 Notebook
│   ├── 00_environment_check.ipynb
│   ├── 01_mlp_baseline.ipynb
│   ├── 02_cnn_baseline.ipynb
│   ├── 03_student_experiment.ipynb
│   └── 04_final_test_evaluation.ipynb
└── results/                      ← 全部指标、曲线、错误案例、混淆矩阵、权重
```

`data/` 不在包里，第一次运行会自动下载 Fashion-MNIST。

## 2. 环境

| 项目 | 版本 / 信息 |
|---|---|
| 操作系统 | Windows 11 |
| CPU | Intel Core i9-14900HX（24 核 / 32 线程），16 GB 内存 |
| GPU | 无（全程 CPU） |
| Python | 3.12.10 |
| PyTorch / torchvision | 2.15.0+cpu / 0.29.2+cpu |
| 其他 | NumPy 2.5.4、pandas 3.1.1、matplotlib 3.11.2、JupyterLab 4.6.6 |

## 3. 安装

在解压后的项目根目录执行（PowerShell，CPU）：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install torch torchvision
python -m pip install -r requirements.txt
```

我这边 `download.pytorch.org` 的 CPU 源下不动，换成了镜像源，最后得到 `torch 2.15.0+cpu`。
有 GPU 的话先按 PyTorch 官方选择器装匹配 CUDA 的版本，再用 `requirements.txt` 补其它依赖，不要之后用 CPU 版覆盖。

启动：

```bash
jupyter lab
```

## 4. 执行顺序

每个 notebook 用独立内核、从头跑一次：

1. `notebooks/00_environment_check.ipynb` —— 环境检查
2. `notebooks/01_mlp_baseline.ipynb` —— MLP 基线 + 学习率变体（1e-3 → 3e-4）
3. `notebooks/02_cnn_baseline.ipynb` —— CNN 基线、MLP/CNN 对照、验证集错误案例、通道变体（32/64 → 16/32）
4. `notebooks/03_student_experiment.ipynb` —— 学习率 1e-4 / 1e-3 / 1e-2 三组对照（各 3 轮）
5. `notebooks/04_final_test_evaluation.ipynb` —— 设置冻结后的最终测试（只跑一次）

路径以项目根目录为准，`data/` 和 `results/` 会自动创建。
本机顺序跑完大约 6 分钟（00 4 秒、01 70 秒、02 157 秒、03 134 秒、04 7 秒），不算第一次下数据。

## 5. 主要结果

| 实验 | 设置 | 验证准确率 | 测试准确率 |
|---|---|---:|---:|
| MLP 基线 | Adam 1e-3，5 轮，batch 128，seed 42 | 86.26% | 86.27% |
| MLP 学习率变体 | lr 3e-4，其余同基线 | 86.82% | — |
| CNN 基线 | Adam 1e-3，5 轮，batch 128，seed 42 | 90.88% | 90.75% |
| CNN 结构变体 | 通道 16/32（参数量约 49.1%） | 89.16% | — |
| 学习率 A | CNN，lr 1e-4，3 轮 | 84.46% | — |
| 学习率 B | CNN，lr 1e-3，3 轮 | 89.04% | — |
| 学习率 C | CNN，lr 1e-2，3 轮 | 89.06% | — |

验证集最大的混淆方向是 Shirt→T-shirt/top，98 次，占 Shirt 的 20.0%；其次 Shirt→Pullover 38 次、Shirt→Coat 36 次。十来个带样本编号的错误案例在 `results/cnn_validation_error_cases.csv` 里。

## 6. 复现

- 全局 `SEED = 42`，random / numpy / torch 都设了；训练验证划分用 `random_split(..., generator=torch.Generator().manual_seed(42))`。
- 每次训练会存 `*_history.csv`（逐轮）、`*_metrics.json`（最终指标）、`*_state_dict.pt`（权重）和 `*_curves.png`。
- 错误分析脚本在项目根目录运行 `python analysis.py`，前提是 `results/` 里已经有基线权重。它会生成混淆矩阵、各类别准确率，以及带全局样本编号的错误案例。

## 7. 已知问题

1. `03_student_experiment.ipynb` 直接调用 `CNN()` 却缺少类定义，原样运行会报 `NameError`。我已经补了和 `02_cnn_baseline.ipynb` 一样的 CNN 定义（超参数没动），并在单元格上方写了说明。
2. 错误案例图里的中文需要系统里有 Microsoft YaHei 或 SimHei，没有的话中文会变成方块，可以在绘图前换成系统已有的中文字体。
3. CPU 上 MLP 大概 5 秒一轮、CNN 大概 15–18 秒一轮，换机器耗时会变；固定种子下指标应该差不多，CPU 算子差异可能带来末位抖动。
4. `results/*.pt` 每个不到 2 MB，只是留档用。报告里的数字都已经写进 csv/json，删掉这些权重不影响任何结论和图表。

## 8. 说明

包里的 README、实验报告、AI使用说明、实验记录表和 `results/` 下的结果文件都是这次完成后自己整理的。
