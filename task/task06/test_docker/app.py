"""Task 06 / Task 10 最小可运行示例：容器内运行 Python 并打印环境信息。"""
import platform
import sys
from datetime import datetime


def main() -> None:
    print("=" * 48)
    print("Hello AI-Lab Docker")
    print("=" * 48)
    print(f"运行时刻   : {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"Python 版本: {sys.version.split()[0]}")
    print(f"解释器路径 : {sys.executable}")
    print(f"操作系统   : {platform.system()} {platform.release()}")
    print(f"主机名     : {platform.node()}")
    print("=" * 48)


if __name__ == "__main__":
    main()
