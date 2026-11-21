# -*- coding: utf-8 -*-
"""全局配置：路径、端口、窗口、超时。

为什么集中：这些值要写进 README，
换机器、换分辨率时只改这里。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # 项目根目录

# miniPaint 静态文件（解压后的目录）
MINIPAINT_DIR = ROOT / "env" / "miniPaint-master"

PORT = 8123
BASE_URL = f"http://127.0.0.1:{PORT}"

# 固定窗口：截图和坐标都按这个尺寸
VIEWPORT = {"width": 1400, "height": 1600}

# 超时（毫秒）：所有等待都必须有上限
TIMEOUT_MS = 15_000

# 输出目录
OUTPUT_DIR = ROOT / "output"