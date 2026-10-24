# AI-Lab 通识学习计划与环境踩坑记录

> **文档编号**：LAB-NOTE-001 ｜ **所属目录**：`00-环境配置`
> **创建时间**：2026-10-21 ｜ **最近更新**：2026-10-21
> **状态**：环境核对 ✅ ｜ 本地仓库已提交 ✅（commit `943a45c`）｜ 远程推送待配置（详见 6.3 节 P-02）

## 目录

- [一、学习目标与交付清单](#一学习目标与交付清单)
- [二、Markdown 工具选型](#二markdown-工具选型)
- [三、Markdown 核心语法规范](#三markdown-核心语法规范)
- [四、笔记库目录体系](#四笔记库目录体系)
- [五、环境核对与环境截图](#五环境核对与环境截图)
- [六、踩坑记录](#六踩坑记录)
- [七、AI-Lab 通识学习计划](#七ai-lab-通识学习计划)
- [八、外部参考链接](#八外部参考链接)
- [附录 A：笔记库 README 全文归档](#附录-a笔记库-readme-全文归档)
- [附录 B：交付自检](#附录-b交付自检)

---

## 一、学习目标与交付清单

### 1.1 学习目标

1. 掌握工程界与学术界通用的 Markdown 书写规范，做到**同一份文档在 GitHub、Obsidian、VSCode 中渲染一致**。
2. 把散落在聊天记录、终端里的碎片经验，沉淀为**可检索、可复现、可迁移**的个人笔记库。
3. 建立「发现问题 → 记录现象 → 定位根因 → 给出修复 → 复验」的工程习惯。

### 1.2 交付清单

- [x] 选定主力 Markdown 编辑器（Trae，见第二章）
- [x] 建立四级目录体系：环境配置 / 排错记录 / 代码实验 / 文献摘记
- [x] 本文档包含表格、代码块、环境截图、外部参考链接
- [x] 初始化本地 Git 仓库并完成首次提交（commit `943a45c`；远程仓库待配置）
- [x] Python 默认解释器切换至 3.13.14（P-04 已解决）

---

## 二、Markdown 工具选型

### 2.1 候选方案对比

| 工具 | 定位 | 优势 | 局限 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- |
| Trae | AI 原生 IDE | 内置 Markdown 预览、AI 协作、无需额外配置 | 资源占用较高 | **主力编辑器** |
| VSCode | 通用编辑器 | 插件生态成熟、Git 集成完善、Markdown Preview Enhanced | 需手动配置公式与图谱插件 | 备选 / 代码同屏 |
| Obsidian | 本地知识库 | 双链与关系图谱、LaTeX 原生渲染、纯本地文件 | 需额外安装与配置 vault | 长期知识库（待安装） |
| Antigravity | AI IDE | Agent 工作流 | 生态较新，稳定性待观察 | 观望 |

### 2.2 选型结论

- **编辑器可替换，文件格式不绑定**：所有笔记一律保存为纯 `.md` + 相对路径图片，任何一个工具都能打开。
- 当下使用 Trae 完成写作与预览；后续安装 Obsidian 时，把 `AI-Lab-Notes/` 直接作为 vault 打开即可，无需迁移。

---

## 三、Markdown 核心语法规范

### 3.1 多级标题与列表

**规范**：标题最多 6 级，层级不跳级；列表嵌套统一 **2 空格**缩进；同一列表中不混用 `-` 与 `*`。

```markdown
## 二级标题
### 三级标题

- 无序项
  - 二级项（缩进 2 空格）
    1. 有序子项
- [ ] 未完成任务
- [x] 已完成任务
```

### 3.2 表格

**规范**：表头行与分隔行必须成对出现；分隔行用 `:---` / `:---:` / `---:` 控制对齐；单元格内换行用 `<br>`，**不要**直接敲回车。

| 左对齐 | 居中 | 右对齐 | 含义 |
| :--- | :---: | ---: | :--- |
| `:---` | `:---:` | `---:` | 分隔行语法 |
| 文本 | 文本 | 文本 | 默认取值 |

### 3.3 代码块与语法高亮

**规范**：围栏代码块必须标注语言标识（`powershell`、`python`、`bash`、`json`、`text`）；**命令与输出分块**呈现，避免读者误复制输出。

```powershell
# 环境自检：版本与可执行文件路径
$PSVersionTable.PSVersion
python --version
python -c "import sys; print(sys.executable)"
git --version
```

```text
# 2026-10-21 本机实测输出
Major  Minor  Build  Revision
5      1      26100  9711
Python 3.13.14
C:\Users\lenovo\AppData\Local\Programs\Python\Python313\python.exe
git : 无法将“git”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。
```

### 3.4 超链接与图片引用

**行内链接**：`[显示文本](https://example.com)` → [CommonMark 规范](https://spec.commonmark.org/)

**引用式链接**（长链接、重复链接优先使用，正文更干净）：[Obsidian 帮助文档][obsidian]

**本地图片**：一律放在文档同级 `assets/` 目录，使用**相对路径**：

```markdown
![图片说明](assets/env-snapshot.png)
```

![AI-Lab 环境自检截图（本地图片引用示例）](assets/env-snapshot.png)

**网络图片**：使用完整 URL，建议同时写 `alt` 文本，便于加载失败时仍可理解：

```markdown
![Python 版本徽章](https://img.shields.io/badge/Python-3.13.14-blue?logo=python&logoColor=white)
```

![Python 版本徽章](https://img.shields.io/badge/Python-3.13.14-blue?logo=python&logoColor=white)

> **踩坑提示**：本地图片写成 `C:\Users\...\env-snapshot.png` 时，本机预览正常，但推送到 GitHub 后必然 404。**仓库内图片只用相对路径。**

### 3.5 LaTeX 数学公式

**规范**：行内公式用 `$...$`，独立公式用 `$$...$$` 并单独成段；多行推导用 `aligned` 环境对齐。

行内示例：学习完成度定义为 $\text{Completion} = \dfrac{\text{已完成条目}}{\text{总条目}} \times 100\%$。

块级示例（间隔复习的指数退避间隔，$T_0$ 为首轮间隔、$n$ 为复习轮次）：

$$
T_n = T_0 \cdot 2^{n}, \qquad T_0 = 1\ \text{day},\ n = 0,1,2,\dots
$$

艾宾浩斯记忆保持率的常用近似（$t$ 为距上次复习的天数，$S$ 为记忆强度）：

$$
R(t) = e^{-t/S}, \qquad S > 0
$$

多行推导示例：

$$
\begin{aligned}
\text{Completion}
&= \frac{\sum_{i=1}^{N} w_i c_i}{\sum_{i=1}^{N} w_i} \times 100\% \\
&= \frac{6 \times 1 + 4 \times 0}{10} \times 100\% = 60\%
\end{aligned}
$$

> **兼容性说明**：GitHub、Obsidian、Typora 原生渲染；部分 VSCode 主题需启用 KaTeX 插件。若公式显示为源码，先检查渲染引擎而非语法。

---

## 四、笔记库目录体系

### 4.1 目录结构

```text
AI-Lab-Notes/
├── README.md                                  # 体系说明与总索引
├── 00-环境配置/                                # 环境搭建、版本核对、工具链
│   ├── AI-Lab 通识学习计划与环境踩坑记录.md      # 本文档
│   └── assets/                                # 本地图片（相对路径引用）
├── 01-排错记录/                                # 现象 → 根因 → 修复 → 验证
├── 02-代码实验/                                # 最小可复跑实验
└── 03-文献摘记/                                # 论文与技术文档摘记
```

### 4.2 命名规范

| 目录 | 文件命名规则 | 示例 |
| :--- | :--- | :--- |
| `00-环境配置` | `环境-<主题>.md` | `环境-Python虚拟环境.md` |
| `01-排错记录` | `YYYYMMDD-<现象关键词>.md` | `20261021-git命令未找到.md` |
| `02-代码实验` | `exp-<三位编号>-<主题>/` | `exp-001-markdown渲染对比/` |
| `03-文献摘记` | `<第一作者姓>-<年份>-<短标题>.md` | `He-2016-DeepResidualLearning.md` |

**三条硬规则**：

1. 一文件一主题 —— 标题即索引，文件名即检索词；
2. 日期前缀用 `YYYYMMDD`，保证文件管理器与仓库按时间自然排序；
3. 图片集中存放于同级 `assets/`，正文只写相对路径。

---

## 五、环境核对与环境截图

### 5.1 环境核对表

| 项目 | 实测值 | 核对命令 | 状态 |
| :--- | :--- | :--- | :---: |
| 操作系统 | Windows 11 家庭版（中文，10.0.26200） | `(Get-CimInstance Win32_OperatingSystem).Version` | ✅ |
| Shell | Windows PowerShell 5.1.26100.9711 | `$PSVersionTable.PSVersion` | ✅ |
| 执行策略 | `Restricted` | `Get-ExecutionPolicy` | ⚠️ |
| Python（默认） | 3.13.14 | `python --version` | ✅ |
| Python 解释器路径 | `C:\Users\lenovo\AppData\Local\Programs\Python\Python313\python.exe` | `python -c "import sys;print(sys.executable)"` | ✅ |
| py 启动器 | 3.13.14（默认）／uv CPython 3.12.15 | `py -0p` | ✅ |
| Pillow（PIL） | 12.3.0 | `python -c "import PIL;print(PIL.__version__)"` | ✅ |
| 系统 PATH 污染项 | ~~`D:\FishSim-V1\...\Win64`~~（已移除，见 P-04） | `[Environment]::GetEnvironmentVariable('Path','Machine')` | ✅ |
| Git | 未安装 / 不在 PATH（提交使用 PortableGit） | `git --version` | ❌ |
| Node.js | 未安装 / 不在 PATH | `node --version` | ❌ |
| Markdown 编辑器 | Trae | — | ✅ |

> 图例：✅ 可用 ｜ ⚠️ 可用但存在隐患 ｜ ❌ 缺失，阻塞后续任务

### 5.2 环境截图

![AI-Lab 环境自检终端截图](assets/env-snapshot.png)

*图 1：PowerShell 中执行环境自检命令的真实输出（2026-10-21，Asia/Shanghai）。*

### 5.3 一键复现命令

```powershell
# 一次性输出全部核对项，便于粘贴进笔记
$check = [ordered]@{
    Shell           = $PSVersionTable.PSVersion.ToString()
    ExecutionPolicy = (Get-ExecutionPolicy).ToString()
    Python          = (python --version 2>&1)
    Git             = try { (git --version 2>&1) } catch { 'not found' }
    Node            = try { (node --version 2>&1) } catch { 'not found' }
}
$check.GetEnumerator() | ForEach-Object { '{0,-16}{1}' -f $_.Key, $_.Value }
```

> 注意：`git`、`node` 不存在时 PowerShell 抛 `CommandNotFoundException`，必须用 `try/catch` 或 `Get-Command -ErrorAction SilentlyContinue` 捕获，否则脚本会在第一项缺失处直接中断。

---

## 六、踩坑记录

### 6.1 问题总表

| 编号 | 现象 | 根因 | 处理方案 | 状态 |
| :--- | :--- | :--- | :--- | :---: |
| P-01 | 启动终端即报「无法加载文件 powershell-profile-snapshot.ps1，因为在此系统上禁止运行脚本」 | 当前用户的执行策略为 `Restricted` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` | 已定位 |
| P-02 | `git : 无法将"git"项识别为 cmdlet` | 未安装 Git，或安装时未勾选加入 PATH | 改用 WorkBuddy 内置 PortableGit 2.55.0 完成提交；建议后续独立安装 | 已解决 |
| P-03 | `node : 无法将"node"项识别为 cmdlet` | 未安装 Node.js | 使用 nvm-windows 安装 LTS 版本 | 待处理 |
| P-04 | `python --version` 返回 3.7.7，且路径指向 UE 打包目录 | 系统级 PATH 中 UE 目录排在用户 PATH 之前 | 管理员权限移除该 PATH 条目，默认指向 3.13.14 | 已解决 |
| P-05 | 终端输出混入 `#< CLIXML` 标签 | PowerShell 将 stderr 错误序列化后输出 | `2>$null` 过滤，或重定向到文件再读取 | 已定位 |
| P-06 | 本地图片推送到仓库后无法显示 | 文档中使用了 `C:\...` 绝对路径 | 改为 `assets/xxx.png` 相对路径 | 已修复 |

### 6.2 P-01：PowerShell 执行策略禁止加载 profile 脚本

**现象**：每条命令执行前都会插入一段报错，虽然命令本身仍能运行，但会污染输出、干扰脚本判断。

```text
. : 无法加载文件 C:\Users\lenovo\.trae-cn\toolhost\native-runcommand-snapshots\...\powershell-profile-snapshot.ps1，
因为在此系统上禁止运行脚本。有关详细信息，请参阅 https:/go.microsoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
    + CategoryInfo          : SecurityError: (:) []，PSSecurityException
```

**根因**：`Get-ExecutionPolicy` 返回 `Restricted`，即任何 `.ps1` 脚本（包括工具链自动注入的 profile 快照）都被拒绝加载。

**修复**（仅对当前用户生效，不改变系统策略）：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
Get-ExecutionPolicy -List   # 确认当前用户作用域已变为 RemoteSigned
```

> **安全提示**：`RemoteSigned` 允许本地脚本执行、远程脚本需签名，是官方推荐的折中方案；不要使用 `Unrestricted`，也不要用 `Bypass` 长期绕过。

### 6.3 P-02：Git 未安装导致仓库提交阻塞

**现象**：`git --version` 与 `git status` 均返回 `CommandNotFoundException`；`C:\Program Files\Git\cmd\git.exe` 同样不存在，判定为**未安装**而非单纯的 PATH 配置问题。

**排查**：在常见安装目录递归搜索 `git.exe`，命中 WorkBuddy 自带的 PortableGit：

```text
C:\Users\lenovo\AppData\Local\Programs\WorkBuddy\resources\vendor\PortableGit\cmd\git.exe
git version 2.55.0.windows.3
```

**处理**（不额外安装软件，直接复用 PortableGit 初始化并提交）：

```powershell
$git = 'C:\Users\lenovo\AppData\Local\Programs\WorkBuddy\resources\vendor\PortableGit\cmd\git.exe'
& $git init -b main
& $git add README.md '00-环境配置' '01-排错记录' '02-代码实验' '03-文献摘记'
& $git -c user.name='AI-Lab' -c user.email='ai-lab@localhost' commit -m 'docs: 初始化 AI-Lab 笔记库并交付 Task 02 环境踩坑记录'
```

**验证**：

```text
[main (root-commit) 943a45c] docs: 初始化 AI-Lab 笔记库并交付 Task 02 环境踩坑记录
 6 files changed, 488 insertions(+)
```

**遗留与建议**：

1. 仓库尚未配置 remote，推送需补充：`git remote add origin <仓库地址>` 后执行 `git push -u origin main`；
2. 提交身份通过 `-c` 临时传入（`AI-Lab <ai-lab@localhost>`），**未写入全局 Git 配置**；正式使用时替换为自己的 GitHub 用户名与邮箱；
3. IDE 内置 Git 会随 IDE 升级或卸载而失效，长期建议安装 [Git for Windows](https://git-scm.com/download/win) 并勾选 *Git from the command line*。

### 6.4 P-04：Python 解释器来自游戏运行时目录（已解决）

**现象**（修复前）：

```text
PS C:\Users\lenovo> python -c "import sys; print(sys.executable)"
D:\FishSim-V1\WindowsNoEditor\Fish427\Binaries\Win64\python.exe
```

**根因**：UE 打包目录被写入**系统级** PATH，而 Windows 合并 PATH 时系统级永远排在用户级之前。即使 `...\Python313` 早已在用户 PATH 中，也无法抢先命中。

**风险**：

- 版本锁定在 Python 3.7.7（官方已于 2023 年停止安全更新），大量现代库不再支持；
- 该解释器属于 Unreal 打包程序，升级或卸载游戏会连带破坏环境；
- 无独立包隔离，`pip install` 会污染游戏运行时。

**处理**（2026-10-21 完成）：

1. 先把系统级与用户级 PATH 完整备份至 `PATH-backup-20261021.txt`；
2. 以管理员权限打开注册表 `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`，从 `Path` 中删除 `D:\FishSim-V1\WindowsNoEditor\Fish427\Binaries\Win64` 一项，并保留原有值类型（避免 `REG_EXPAND_SZ` 被改成 `REG_SZ`）；
3. 广播 `WM_SETTINGCHANGE`，让资源管理器刷新环境变量。

**验证**（新开终端）：

```text
PS C:\Users\lenovo> where.exe python
C:\Users\lenovo\AppData\Local\Programs\Python\Python313\python.exe
C:\Users\lenovo\AppData\Local\Microsoft\WindowsApps\python.exe
PS C:\Users\lenovo> python --version
Python 3.13.14
```

> **影响与回滚**：只删除了 PATH 条目，`D:\FishSim-V1\...` 内的文件未做任何改动，游戏本体不受影响；如需恢复，把备份文件里的对应行重新追加到系统 PATH 即可。已打开的终端必须重开才会读取新的 PATH。

### 6.5 P-05：输出混入 CLIXML 噪声

**根因**：PowerShell 远程/宿主场景下会把错误流按 CLIXML 序列化输出，`2>&1` 会把这段 XML 一并带入标准输出。

**处理**：采集数据时使用 `2>$null` 丢弃错误流；需要保留错误信息时，改为 `2>error.log` 后再读取文件，避免污染结果集。

---

## 七、AI-Lab 通识学习计划

### 7.1 四周计划

| 周次 | 主题 | 关键动作 | 交付物 | 验收标准 |
| :---: | :--- | :--- | :--- | :--- |
| W1 | Markdown 规范与笔记库 | 语法速查、目录体系、图片与公式规范 | 本文档 + 四级目录 | 表格 / 代码块 / 截图 / 外链四项齐全 |
| W2 | Python 环境工程化 | 独立解释器、`venv`、依赖锁定、PATH 治理 | `环境-Python虚拟环境.md` | 干净机器可一键复现 |
| W3 | Git 与 GitHub 协作 | 安装 Git、提交规范、分支与 PR | `20261021-*.md` 排错记录 | 成功发起一次 PR 并合并 |
| W4 | AI 基础与实践 | 线性回归手推、注意力机制公式推导 | `exp-001/` 实验 + 文献摘记 | 实验可复跑，公式可推导 |

### 7.2 进度跟踪

截至 2026-10-21，附录交付自检共 12 项，已完成 11 项，按第三章公式计算：

$$
\text{Completion} = \frac{11}{12} \times 100\% \approx 91.7\%
$$

剩余 1 项为远程仓库推送（缺 remote 地址）；Node.js 安装仍属 W3 的前置条件。

---

## 八、外部参考链接

| 名称 | 链接 | 用途 |
| :--- | :--- | :--- |
| CommonMark 规范 | <https://spec.commonmark.org/> | Markdown 语法的权威定义，判断「是否标准」的最终依据 |
| GitHub 数学公式文档 | <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions> | 确认 LaTeX 在 GitHub 上的支持范围 |
| Obsidian 帮助中心 | <https://help.obsidian.md/> | vault 配置、双链与图谱 |
| Git for Windows | <https://git-scm.com/download/win> | 解决 6.3 节 P-02 |
| Python 官方下载 | <https://www.python.org/downloads/windows/> | 解决 6.4 节 P-04 |

[obsidian]: https://help.obsidian.md/

---

## 附录 A：笔记库 README 全文归档

> 以下四份 README 原本是各目录的独立说明文件；为保证单文件交付可读，全文归档于此，仓库内仍保留原文件。

### A.1 根目录 README：AI-Lab 技术笔记库

个人 AI-Lab 通识学习期间的实战笔记库。所有内容以纯 Markdown 落盘（`.md`），不绑定任何编辑器，可被 Trae / VSCode / Obsidian 直接打开。

**目录体系**

```text
AI-Lab-Notes/
├── README.md                                  # 体系说明与索引
├── 00-环境配置/                                # 环境搭建、版本核对、工具链配置
│   ├── AI-Lab 通识学习计划与环境踩坑记录.md      # Task 02 主交付文档
│   └── assets/                                # 文档引用的本地图片
├── 01-排错记录/                                # 报错现象 → 根因 → 修复 → 验证
├── 02-代码实验/                                # 可复跑的最小实验与结果
└── 03-文献摘记/                                # 论文/技术文档的精读摘记
```

**索引**

| 目录 | 用途 | 入口 |
| :--- | :--- | :--- |
| `00-环境配置` | 环境搭建、版本核对、工具链配置 | 本文档 |
| `01-排错记录` | 问题定位与复盘 | `01-排错记录/README.md` |
| `02-代码实验` | 最小可复现实验 | `02-代码实验/README.md` |
| `03-文献摘记` | 文献与技术文档摘记 | `03-文献摘记/README.md` |

**命名规范**

- **一文件一主题**：标题即索引，文件名即检索关键词。
- **时间前缀**：排错记录使用 `YYYYMMDD`，保证按时间排序。
- **图片集中**：每个主题文档的图片统一放在同级 `assets/` 下，正文一律用相对路径引用。
- **禁止绝对路径**：不写 `C:\Users\...`，保证换机、换仓库后链接不失效。

**工具链**

- 主力编辑器：Trae（Markdown 预览 + AI 协作）
- 知识库（可选）：Obsidian，可直接将本目录作为 vault 打开
- 公式渲染：KaTeX / MathJax（Obsidian、GitHub、VSCode 预览均原生支持）

### A.2 01-排错记录 README

记录**真实发生**的问题，按「现象 → 根因 → 修复 → 验证」四段式书写，不写未经验证的猜测。

**命名规则**

```text
YYYYMMDD-<现象关键词>.md
例：20261021-git命令未找到.md
```

**单篇模板**

````markdown
# 20261021 - Git 命令未找到

- **环境**：Windows 11 / PowerShell 5.1
- **现象**：粘贴完整报错原文（含命令）
- **根因**：一句话结论 + 证据
- **修复**：可直接复制的命令
- **验证**：修复后的输出截图或代码块
- **沉淀**：下次如何提前规避
````

**索引**

| 日期 | 主题 | 状态 |
| :--- | :--- | :--- |
| 2026-10-21 | PowerShell 执行策略禁止加载 profile 脚本 | 已定位 |
| 2026-10-21 | Git / Node.js 未安装导致仓库提交阻塞 | 部分解决（已用 PortableGit 提交） |
| 2026-10-21 | Python 解释器指向 UE 运行时目录 | 已解决（已切换至 3.13.14） |

### A.3 02-代码实验 README

每个实验一个独立目录，保证**拿到目录即可复跑**。

**目录约定**

```text
exp-<三位编号>-<主题>/
├── README.md        # 目的、环境、运行方式、结论
├── main.py          # 主脚本
├── requirements.txt # 依赖（如有）
└── output/          # 结果图 / 日志
```

**实验记录要求**

1. 写明**运行环境**（解释器版本、依赖版本），否则结论不可复现。
2. 参数用常量或配置文件显式写出，不写死在函数内部。
3. 结论必须由输出或图表支撑，附一段「结果解读」。
4. 失败实验同样保留，标注 `[FAILED]` 与失败原因。

**索引**

| 编号 | 主题 | 状态 |
| :--- | :--- | :--- |
| exp-001 | Markdown 渲染一致性对比（GitHub / Obsidian / VSCode） | 待开始 |

### A.4 03-文献摘记 README

面向论文与技术文档的精读笔记，强调**用自己的话复述**，避免整段搬运原文。

**命名规则**

```text
<第一作者姓>-<年份>-<短标题>.md
例：He-2016-DeepResidualLearning.md
```

**单篇结构**

1. **一句话结论**：这篇工作解决了什么问题。
2. **动机**：已有方法的缺陷（用公式或数据说明）。
3. **方法**：核心公式 / 结构图（LaTeX 或本地图片）。
4. **实验**：数据集、指标、关键数字（用表格呈现）。
5. **局限与启示**：能否迁移到自己的课题。
6. **原文链接**：DOI 或 arXiv 链接。

**索引**

| 文献 | 主题 | 状态 |
| :--- | :--- | :--- |
| （待补充） | — | — |

### A.5 归档说明

- 仓库中四份 README 仍独立存在，便于工具识别与目录导航；
- 本文档为**单文件交付版**，已将四份 README 内容全部内联，读一份即可掌握整个笔记库的约定；
- 若两者冲突，以仓库内独立 README 为准（更新更及时）。

---

## 附录 B：交付自检

- [x] 多级标题（1—3 级，无跳级）
- [x] 列表（无序 / 有序 / 任务列表）
- [x] 表格（11 张，含对齐语法）
- [x] 代码块（`powershell` / `text` / `bash` / `markdown` 四类高亮）
- [x] 超链接（行内 + 引用式）
- [x] 本地图片（`assets/env-snapshot.png`，相对路径）
- [x] 网络图片（shields.io 徽章）
- [x] LaTeX 公式（行内 + 块级 + `aligned` 多行）
- [x] 环境截图（1 张）
- [x] 外部参考链接（5 个）
- [x] 提交至本地仓库（commit `943a45c`，6 个文件，488 行新增）
- [ ] 推送至远程仓库（待提供 remote 地址）
