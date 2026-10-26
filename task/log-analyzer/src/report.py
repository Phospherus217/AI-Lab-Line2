# -*- coding: utf-8 -*-
"""报告模块：把统计结果输出成 Markdown"""
import csv
from pathlib import Path

def build_markdown(summary,title="日志分析报告"):
    """生成 Markdown"""
    lines=[]
    lines.append(f"# {title}")
    lines.append("")

    # =====基本信息=====
    lines.append("## 一·基本信息")
    lines.append("")
    lines.append("| 项目 | 值 |")
    lines.append("| :---: | :---: |")
    lines.append(f"| 源文件 | '{summary['source']}' |")
    lines.append(f"| 总行数 | {summary['total_line']} |")
    # ... 有效行数、无效行数
    lines.append("")

    # ===== 二、级别分布 =====
    lines.append("## 二、级别分布")
    lines.append("")
    lines.append("| 级别 | 数量 | 占比 |")
    lines.append("| :---: | :---: | :---: |")
    counts = summary["level_counts"]
    percentage = summary["level_percentage"]
    for level, num in counts.items():
        lines.append(f"| {level} | {num} | {percentage[level]} |")
    lines.append(f"| **合计** | **{sum(counts.values())}** | 100.0% |")
    lines.append("")

    # ===== 三、报错 Top 5 =====
    lines.append("## 三、报错归类 TOP 5")
    lines.append("")
    if summary["error_top"]:  # 有报错才画表格
        lines.append("| 排名 | 报错内容 | 次数 |")
        lines.append("| :---: | :---: | :---: |")
        for i, (msg, num) in enumerate(summary["error_top"], start=1):
            lines.append(f"| {i} | {msg} | {num} |")
    else:
        lines.append("_没有 ERROR 级别的记录。_")
    lines.append("")

    # ===== 四、高频关键词 =====
    lines.append("## 四、高频关键词（来自 WARN / ERROR）")
    lines.append("")
    if summary["keyword_top"]:
        words = [f"'{w}'({n})" for w, n in summary["keyword_top"]]
        lines.append(" ".join(words))
    else:
        lines.append("_没有可提取的关键词。_")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_由 log-analyzer 自动生成。_")
    lines.append("")
    return "\n".join(lines)

def write_markdown(path, text):
    """把 Markdown 写入文件，自动创建父目录。"""
    target=Path(path)
    if target.parent and not target.parent.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(text)
    return target
