# Task01：现代 AI 编程环境与 CLI 协同工具配置

## 1. 环境清单

| 类别 | 选择/版本 | 用途 |
|---|---|---|
| 操作系统 | Windows 11（WSL2 / Ubuntu 24.04） | 本地开发与 Linux 命令行 |
| AI IDE | Trae | 智能代码编辑与 Agent 协同 |
| 终端 AI Agent | Codex CLI 0.146.0-alpha.3.1 | 终端交互式代码审查/解释 |
| 版本管理 | Git 2.55.0 | 代码与文档留痕 |
| Python 环境 | Conda `ailab` / Python 3.10.22 | 依赖隔离 |
| 容器 | Docker 29.1.3（WSL Ubuntu） | 环境打包与复现 |

## 2. 配置与上手步骤

1. 安装并打开 Trae，创建/打开项目工作区；
2. 配置终端 AI Agent（Codex CLI），确保终端可正常启动；
3. 使用 Conda 创建隔离环境：
   ```powershell
   conda create -n ailab python=3.10 pip
   conda activate ailab
   python --version
   ```
4. 配置国内镜像源（Conda/Pip 使用清华源）；
5. 配置 Git 用户信息与 SSH Key，完成仓库推送验证。

## 3. 验证记录

- [x] Trae 工作界面可打开（截图：`trae-ide.png`）
- [x] Codex CLI 可启动（截图：`codex-cli.png`）
- [x] MiMo 控制台可访问（截图：`mimo-api.png`）
- [ ] 终端中完成一次真实 AI 交互并截图
- [ ] 完成一次 API 连通性调用并截图（密钥打码）
- [ ] 记录一次真实报错与排错过程

> 截图中的 API 密钥必须打码；真实密钥只保存在本地 `.env`，并加入 `.gitignore`。

## 4. 已知问题与排错

- WSL 普通沙箱进程出现 `E_ACCESSDENIED`，在正常终端/管理员终端可启动；
- Docker Hub 直连不稳定，已在 `/etc/docker/daemon.json` 配置国内镜像加速；
- Codex CLI 需要 `HOME` 与 `CODEX_HOME` 环境变量，已写入用户环境。

## 5. 参考链接

- [Codex CLI 文档](https://github.com/openai/codex)
- [Trae 官网](https://www.trae.ai/)
- [Docker WSL2 后端文档](https://docs.docker.com/desktop/wsl/)