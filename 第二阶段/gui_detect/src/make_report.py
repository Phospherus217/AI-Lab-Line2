import csv

from config import OUTPUT_DIR


def summarize(rows):
    """打印一行总结，方便快速看结果。"""
    count = len(rows)

    # 平均精确率、平均召回率
    average_recall = sum(row["recall"] for row in rows) / count if count else 0
    average_precision = sum(row["precision"] for row in rows) / count if count else 0

    print(f"{count} 张图：平均精确率 {average_precision:.3f}，平均召回率 {average_recall:.3f}")

def save_csv(rows, output_path = None):
    output_path = output_path or (OUTPUT_DIR / "excle.csv")

    if not rows:
        return

    field_names = list(rows[0].keys())

    with open(output_path, "w", newline="", encoding="utf-8-sig") as file :
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)
    print(f"已保存{output_path}")

def save_markdown(rows, output_path = None):
    output_path = output_path or (OUTPUT_DIR / "report.md")

    if not rows:
        return

    # 表头：取第一条记录的键
    field_names = list(rows[0].keys())

    lines = ["# 检测报告", ""]

    # 表头行
    lines.append("| " + " | ".join(field_names) + " |")

    # 分隔行（必须是三个减号）
    lines.append("|" + "|".join(["---"] * len(field_names)) + "|")

    # 每条记录一行
    for row in rows:
        cells = [str(row[name]) for name in field_names]
        lines.append("| " + " | ".join(cells) + " |")

    # 一次性写出，用换行连接
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已保存{output_path}")