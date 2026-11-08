"""Task 07 集合与函数练习 + Task 08 文件扫描脚本。"""

import json
from pathlib import Path

# ---- 集合：去重 ----
nums = [1, 2, 3, 3, 4, 6, 6, 7]
print("去重", list(set(nums)))
print("顺序不变去重", list(dict.fromkeys(nums)))

# ---- 集合：交并差 ----
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print("交集", a & b)
print("并集", a | b)
print("差集", a - b)          # 或 b - a
print("对称差", a ^ b)
print("集合推导式", {n * n for n in range(1, 11)})


# ---- 函数 ----
def greet(name, prefix="同学"):
    return f"你好，{prefix}{name}！"


def totals(*args):
    return sum(args)


def dictionary(**kwargs):
    return kwargs


print(greet("Ai-lab"))
print(greet("张三", "老师"))
print("和", totals(1, 2, 3, 4))
print(dictionary(name="小王", age=20))

# ---- Task 08：扫描 samples 下所有 .md 文件，写出 summary.json ----
root = Path(__file__).resolve().parents[2] / "samples"
out = Path(__file__).resolve().parents[2] / "summary.json"

result = {"files": [], "total_lines": 0, "total_chars": 0}

try:
    if not root.exists():
        raise FileNotFoundError(f"目录不存在：{root}")

    # rglob 会连子目录一起扫
    for md in sorted(root.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        result["files"].append({
            "file": md.name,
            "lines": line_count,
            "chars": len(text),
        })
        result["total_lines"] += line_count
        result["total_chars"] += len(text)

except FileNotFoundError as e:
    print("出错了：", e)

finally:
    print("扫描结束")

# 写出 JSON：ensure_ascii=False 保证中文正常显示
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))
