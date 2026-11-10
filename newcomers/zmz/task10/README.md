# md-checker 项目报告

## 1. 项目简介
本项目是 Markdown 文档检测工具，核心功能：扫描指定目录下 Markdown 文件，识别标题层级跳级问题并生成检测报告。

## 2. 项目文件清单
| 文件 | 说明 |
| ---- | ---- |
| main.py | 程序主源码 |
| requirements.txt | Python依赖声明 |
| Dockerfile | Docker镜像构建配置 |
| README.md | 项目说明文档 |
| docs/ | 存放待检测Markdown测试文件 |

## 3. 本地运行方式
```bash
python main.py -d ./docs -o result-local.md -t 5
-d：待扫描文档目录
• -o：报告输出路径
• -t：超时时间

## 4. 容器化运行方式

### 构建镜像
docker build -t md-checker .
docker run --rm -v $(pwd):/app md-checker -d ./docs -o result-docker.md -t 5

5. 运行结果说明
程序扫描完成后输出 Markdown 格式检测报告，包含文档目录、标题层级警告信息。
