# -*- coding: utf-8 -*-
"""命令行入口：日志分析工具。"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from parser import parse_file
from stats import build_summary,filter_by_level
import report

def build_arg_parser():
    """定义命令行参数。"""
    ap = argparse.ArgumentParser(
        prog="log-analyzer",
        description="日志分析工具：统计级别分布、报错归类、高频关键词",
    )
    ap.add_argument("-i", "--input", required=True, help="日志文件路径")
    ap.add_argument(
        "-o", "--output", default=None,
        help="生成 Markdown 报告到指定路径（不传则只在终端打印统计）",
    )
    ap.add_argument(
        "-l", "--level", default=None,
        choices=["DEBUG", "INFO", "WARN", "ERROR"],
        help="只统计指定级别的记录",
    )
    return ap

def main():
    args = build_arg_parser().parse_args()
    records, total, invalid = parse_file(args.input)

    if args.level:
        records = filter_by_level(records, args.level)
        if not records:
            print(f"[提示] 没有 {args.level} 级别的记录。", file=sys.stderr)
            return 1
        """
        return 1 通俗约定
        0	成功（只有 0 算成功）
        1	一般错误
        2	用法错误（argparse 用这个）
        127	命令不存在
        130	被 Ctrl+C 中断
        """

    summary = build_summary(args.input, records, total, invalid)

    title = "日志分析报告"
    if args.level:
        title += f"（仅 {args.level}）"

    print(title)
    print("\n")
    print(f"总行数   : {total}")
    print(f"有效行数 : {len(records)}")
    print(f"无效行数 : {invalid}")
    print("级别分布 :")
    for level, num in summary["level_counts"].items():
        percentage = summary["level_percentage"][level]
        print(f"  {level:<6} {num:>4}  {percentage}")
    print("\n")
    if summary["error_top"]:
        print("报错 TOP:")
        for i, (msg, num) in enumerate(summary["error_top"], start=1):
            print(f"  {i}. {msg}  ({num} 次)")
    else:
        print("报错 TOP: 没有 ERROR 记录")

    if args.output:
        markdown = report.build_markdown(summary, title)
        out = report.write_markdown(args.output, markdown)
        print()
        print(f"[完成] Markdown 报告：{out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())