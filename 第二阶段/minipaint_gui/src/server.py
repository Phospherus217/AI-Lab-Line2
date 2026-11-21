# -*- coding: utf-8 -*-
"""启停本地静态服务器。

为什么需要：Playwright 打开的是 URL，
用 file:// 会有跨域、下载、缓存等问题。
"""
import socket
import subprocess
import sys
import time

from config import MINIPAINT_DIR, PORT


def wait_port(host="127.0.0.1", port=PORT, timeout=10.0) -> None:
    """轮询端口，直到能连上。

    为什么不用 sleep 固定秒数：
    机器快慢不同，固定等待要么不够、要么浪费。
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket() as s:
            s.settimeout(0.2)
            if s.connect_ex((host, port)) == 0:
                return
        time.sleep(0.1)
    raise TimeoutError(f"端口 {port} 没就绪")


def start_server() -> subprocess.Popen:
    """启动 python -m http.server。"""
    if not MINIPAINT_DIR.exists():
        raise FileNotFoundError(f"找不到 miniPaint：{MINIPAINT_DIR}")

    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--directory", str(MINIPAINT_DIR)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    wait_port()
    return proc


def stop_server(proc: subprocess.Popen) -> None:
    """先温和终止，不行再强杀。"""
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()

if __name__ == "__main__":
    proc = start_server()  # ① 开始：起服务器
    try:
        # ... 打开浏览器、操作 ...
        pass
    finally:
        stop_server(proc)  # ② 结束：关服务器（无论成功失败）