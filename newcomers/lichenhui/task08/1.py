import json
from pathlib import Path

# 1. 获取所有 .md 文件路径
# 请将 'test_data' 替换为你实际的测试文件夹路径
md_files = Path('test_data').glob('*.md')
results = {}

for file in md_files:
    # 2. 使用 with open 读取 utf-8 文本
    content = open(file, 'r', encoding='utf-8').read()
    
    # 3. 统计字数与行数
    chars = len(content)
    lines = len(content.splitlines())
    
    results[file.name] = {"chars": chars, "lines": lines}

# 4. 输出为 summary.json
with open('summary.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("统计完成，已生成 summary.json")