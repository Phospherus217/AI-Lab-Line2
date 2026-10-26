# log-analyzer · 日志分析工具

一个轻量命令行工具：读取文本日志，按级别统计数量与占比、把同类报错归类排序、提取高频关键词，并输出 Markdown 报告。附带 Dockerfile，一条命令即可在容器中复现运行。

> AI-Lab 通识任务 Task 10（综合微项目 · 选项 B 日志与数据清洗工具）交付物。

---

## 功能

- **解析日志**：识别四段式文本日志（`日期 时间 级别 消息`），格式不符的行自动跳过并计数
- **级别统计**：按 `DEBUG / INFO / WARN / ERROR` 统计数量与占比，顺序固定
- **报错归类**：把消息中的**数字归一化为 `#`**，让「超时 5231ms」「超时 8102ms」合并成同一类错误
- **高频关键词**：从 `WARN / ERROR` 消息中提取至少 3 个字符的英文词，自动过滤 `error`、`timeout` 这类废词
- **按级别过滤**：`--level ERROR` 只看某一级别，报告标题自动加「（仅 ERROR）」
- **双模式输出**：不带 `-o` 只在终端打印统计；带 `-o` 才生成 Markdown 文件
- **容器化**：`docker build` + `docker run` 即可运行，无需安装 Python 环境

---

## 环境要求

| 项目 | 要求 |
| --- | --- |
| Python | 3.10 或更高 |
| 第三方依赖 | **无**（只使用标准库） |
| 容器运行 | Docker Desktop / Docker Engine |

---

## 快速开始

**⚠️ 必须在项目根目录执行**（能看到 `src`、`samples`、`output` 三个文件夹的位置）。

```bash
cd log-analyzer
```

### 1. 只看统计，不生成文件

```bash
python src/main.py -i samples/app.log
```

### 2. 生成 Markdown 报告

```bash
python src/main.py -i samples/app.log -o output/report.md
```

### 3. 只看 ERROR 级别

```bash
python src/main.py -i samples/app.log -l ERROR
```

### 4. 组合使用

```bash
python src/main.py -i samples/app.log -l ERROR -o output/errors.md
```

### 5. 查看帮助

```bash
python src/main.py --help
```

---

## 命令行参数

| 参数 | 简写 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `--input` | `-i` | ✅ | — | 日志文件路径 |
| `--output` | `-o` | ❌ | `None` | Markdown 报告保存路径；**不传则只在终端打印** |
| `--level` | `-l` | ❌ | `None` | 只统计指定级别，可选 `DEBUG/INFO/WARN/ERROR` |

`usage` 由 `argparse` 自动生成：

```
usage: log-analyzer [-h] -i INPUT [-o OUTPUT] [-l {DEBUG,INFO,WARN,ERROR}]
```

---

## 输出示例

### 终端输出

```
日志分析报告

总行数   : 125
有效行数 : 120
无效行数 : 5
级别分布 :
  DEBUG    17  14.2%
  INFO     45  37.5%
  WARN     33  27.5%
  ERROR    25  20.8%

报错 TOP:
  1. 请求处理异常: TypeError unexpected argument  (6 次)
  2. 数据库连接失败: connection refused  (6 次)
  3. 请求处理异常: KeyError 'user_id'  (4 次)
  4. 文件读取失败: PermissionError  (4 次)
  5. 数据库连接超时: timeout after #ms  (3 次)

[完成] Markdown 报告：output\report.md
```

### `output/report.md`

```markdown
# 日志分析报告

## 一、基本信息

| 项目 | 值 |
| --- | --- |
| 源文件 | `samples/app.log` |
| 总行数 | 125 |
| 有效行数 | 120 |
| 无效行数 | 5 |
| 时间范围 | 2026-10-24 10:00:03 ~ 2026-10-24 11:33:30 |

## 二、级别分布

| 级别 | 数量 | 占比 |
| --- | --- | --- |
| DEBUG | 17 | 14.2% |
| INFO | 45 | 37.5% |
| WARN | 33 | 27.5% |
| ERROR | 25 | 20.8% |
| **合计** | **120** | 100.0% |

## 三、报错归类 TOP 5

| 排名 | 报错内容（数字已归一化为 #） | 次数 |
| --- | --- | --- |
| 1 | 请求处理异常: TypeError unexpected argument | 6 |
| 2 | 数据库连接失败: connection refused | 6 |
| 3 | 请求处理异常: KeyError 'user_id' | 4 |
| 4 | 文件读取失败: PermissionError | 4 |
| 5 | 数据库连接超时: timeout after #ms | 3 |

## 四、高频关键词（来自 WARN / ERROR）

`typeerror`(6) `argument`(6) `connection`(6) `refused`(6) `keyerror`(4) `user_id`(4) `permissionerror`(4)
```

---

## 日志格式

每行四段，用空格分隔：

```
<日期> <时间> <级别> <消息>
```

示例：

```
2026-10-24 10:00:03 INFO  配置加载完成，共 459 项
2026-10-24 10:04:07 ERROR 请求处理异常: TypeError unexpected argument
2026-10-24 10:05:46 WARN  请求重试第 37 次
```

| 段 | 格式 | 校验规则 |
| --- | --- | --- |
| 日期 | `YYYY-MM-DD` | 必须能被 `strptime` 解析 |
| 时间 | `HH:MM:SS` | 必须能被解析 |
| 级别 | `DEBUG` / `INFO` / `WARN` / `ERROR` | 不在此集合内视为脏数据 |
| 消息 | 任意文本 | 可含空格，**必须放在最后一段** |

### 脏数据如何处理

以下情况整行被丢弃，并计入「无效行数」：

| 情况 | 例子 |
| --- | --- |
| 空行 | （空） |
| 段数不足 4 | `2026-10-24 10:30:00 INFO` |
| 日期非法 | `2026-13-45 10:00:00 INFO 假日期` |
| 级别未知 | `2026-10-24 10:00:00 FATAL 未知级别` |
| 整行无时间戳 | `这行没有时间戳，是脏数据` |

### 自带测试数据

`samples/app.log` 共 **125 行**（120 有效 + 5 种脏数据），可直接用于验证：

| 指标 | 预期值 |
| --- | --- |
| 总行数 | 125 |
| 有效行数 | 120 |
| 无效行数 | 5 |
| DEBUG / INFO / WARN / ERROR | 17 / 45 / 33 / 25 |

---

## 项目结构

```
log-analyzer/
├── README.md
├── requirements.txt          # 依赖清单（仅说明无第三方依赖）
├── Dockerfile
├── .dockerignore
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py               # 入口：命令行参数 + 流程串联
│   ├── parser.py             # 解析：文本行 → 结构化记录
│   ├── stats.py              # 统计：级别、占比、报错归类、关键词
│   └── report.py             # 输出：Markdown 报告
├── samples/
│   └── app.log               # 测试日志（125 行）
└── output/                   # 生成结果（已 gitignore）
```

### 模块职责

| 模块 | 只负责 | 不关心 |
| --- | --- | --- |
| `parser.py` | 把一行文本变成字典 | 怎么统计、怎么输出 |
| `stats.py` | 从记录列表算指标 | 数据从哪来、结果长什么样 |
| `report.py` | 把指标变成 Markdown | 指标怎么算出来的 |
| `main.py` | 解析参数、串流程 | 每一步内部怎么实现 |

---

## Docker 运行

### 1. 构建镜像

```bash
docker build -t log-analyzer:1.0 .
```

> **最后的 `.` 不能漏** —— 表示用当前目录作为构建上下文。

### 2. 运行容器

```bash
docker run --rm -v "${PWD}/samples:/data" -v "${PWD}/output:/output" log-analyzer:1.0 -i /data/app.log -o /output/report.md
```

| 部分 | 作用 |
| --- | --- |
| `--rm` | 运行结束自动删除容器 |
| `-v "${PWD}/samples:/data"` | 把宿主机 `samples` 挂载到容器 `/data` |
| `-v "${PWD}/output:/output"` | 把宿主机 `output` 挂载到容器 `/output` |
| `-i /data/app.log` | **容器内路径**，不是宿主机路径 |
| `-o /output/report.md` | 写到挂载点，文件才能留在宿主机 |

> **Windows PowerShell 用 `${PWD}`**，CMD 用 `%cd%`。
> **`-v` 必须写成「宿主机路径:容器路径」**，少一个冒号会挂到错误位置。

### 3. 容器输出

```
日志分析报告

总行数   : 125
有效行数 : 120
无效行数 : 5
级别分布 :
  DEBUG    17  14.2%
  INFO     45  37.5%
  WARN     33  27.5%
  ERROR    25  20.8%

[完成] Markdown 报告：/output/report.md
```

### 4. 验证可复现

```bash
# 本地跑一份
python src/main.py -i samples/app.log -o output/report_local.md

# 容器跑一份
docker run --rm -v "${PWD}/samples:/data" -v "${PWD}/output:/output" log-analyzer:1.0 -i /data/app.log -o output/report_docker.md
```

两份报告**只有「源文件」那一行不同**（`samples/app.log` vs `/data/app.log`），统计数字完全一致 —— 这就是容器可复现的证明。

---

## 设计说明

### 为什么用 `split(None, 3)` 而不是 `split()`

消息里可能有空格：

```
2026-10-24 10:04:07 ERROR 请求处理异常: TypeError unexpected argument
└── 第1段 ──┘ └第2段─┘ └3段┘ └──────── 第4段完整保留 ────────┘
```

`split(None, 3)` 表示**最多切 3 次**，得到的第 4 段是完整消息。直接 `split()` 会把消息切碎，无法还原。

`None` 表示按任意空白切分并**自动合并连续空格**，比 `split(" ", 3)` 更健壮。

### 为什么要把数字归一化

```
数据库连接失败: timeout after 5231ms     1 次
数据库连接失败: timeout after 8102ms     1 次
数据库连接失败: timeout after 1204ms     1 次
```

这三条本质是同一个错误，但文本不同，统计时会各占一个名额，看不出真实分布。

用 `re.sub(r"\d+", "#", message)` 归一化后统一为：

```
数据库连接失败: timeout after #ms        3 次
```

这才是「报错统计」的意义。注意必须用 `\d+`（整串数字换一个 `#`），用 `\d` 会变成 `####`，位数不同仍然合并不了。

### 为什么 `level_counts` 要多绕一步

`Counter` 的遍历顺序是「首次出现顺序」，日志第一条是 INFO，那 INFO 就会排第一；换一份日志顺序又变了，报告无法稳定阅读。

所以先定义固定的 `LEVEL_ORDER`，再按它取一遍，保证每次输出都是 `DEBUG → INFO → WARN → ERROR`。

### 为什么 `-o` 的默认值是 `None`

`default="output/report.md"` 会导致**每次运行都写文件**，用户无法「只看统计」。

改成 `default=None` 后，`if args.output:` 才能区分「没传」和「传了」，实现两种模式：

- 不传 `-o`：只打印，不产生文件
- 传 `-o`：打印 + 生成报告

### 为什么 Dockerfile 先 COPY requirements.txt

Docker 按层缓存。先复制依赖清单再 `pip install`，只要 `requirements.txt` 没变，这一层就命中缓存；改代码时只需重建 `COPY src/` 这一层。

如果先 `COPY src/`，每次改代码都会让依赖重装一遍。

实测：改一行代码后重新构建，正确顺序 **0.7 秒**（`pip install` 层 `CACHED`），错误顺序要重跑依赖安装。

### 为什么有 `ENTRYPOINT` 还要 `CMD`

- `ENTRYPOINT ["python", "src/main.py"]` —— 固定执行什么程序
- `CMD ["--help"]` —— 不传参数时的默认值

组合效果：`docker run ... -i /data/app.log` 会变成执行 `python src/main.py -i /data/app.log`，用户不需要每次都写 `python src/main.py`。

---

## 常见问题

| 现象 | 原因 | 解决 |
| --- | --- | --- |
| `FileNotFoundError` | 相对路径基准是**当前工作目录** | 先 `cd` 到项目根目录再运行 |
| `[错误] 日志文件不存在：xxx` | 路径写错或文件没生成 | 用 `Test-Path` / `ls` 确认文件存在 |
| 报告里中文乱码或 `\uXXXX` | `open()` 没加 `encoding`，或 `json.dump` 没加 `ensure_ascii=False` | 所有 `open()` 都加 `encoding="utf-8"` |
| 关键词为空 | 正则写错（如 `[A-Za-z_]+]` 多了 `]`） | 用 `r"[A-Za-z_]{3,}"` |
| 报错内容带数字没合并 | `error_top` 没调用 `normalize` | 统计前先 `normalize(record["message"])` |
| `docker: invalid reference format` | `docker run` 最后写成了文件夹路径 | 用镜像名 `log-analyzer:1.0` |
| 容器报 `can't open file '/app/src/main.py'` | `-v` 挂载到了 `/app`，覆盖了镜像内的代码 | 挂载点改为 `/data`、`/output` |
| 容器报「日志文件不存在：/data/app.log」 | 宿主机目录为空（`-v` 会自动建空目录） | 检查宿主机 `samples/app.log` 是否存在 |
| `docker build requires exactly 1 argument` | 漏了最后的 `.` | `docker build -t 名字:版本 .` |

---

## 许可

仅用于 AI-Lab 通识课程学习。
### 本文档由DeekSeek生成

### 特别鸣谢:爱吃白饭的大肥鱼
