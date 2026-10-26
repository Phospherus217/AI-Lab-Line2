import sys
import platform
 
print("=" * 40)
print("Hello AI-Lab Docker!")
print("=" * 40)
print(f"Python 版本 : {sys.version.split()[0]}")
print(f"运行平台    : {platform.system()} {platform.machine()}")
print(f"容器主机名  : {platform.node()}")
print("这段代码跑在容器里，不是在你的 Windows 上。")
