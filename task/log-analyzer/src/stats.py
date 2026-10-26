# -*- coding: utf-8 -*-
"""统计模块：从解析结果里算出各项指标。"""
import re
from collections import Counter
import re

"""用于排序"""
LEVEL_ORDER = ["DEBUG", "INFO", "WARN", "ERROR"]
"""防止重复单词一直占榜单"""
STOPWORDS = {
    "the", "and", "for", "after", "with", "from", "this", "that",
    "failed", "______", "unexpected", "not", "found",
    "http", "sql", "select",
}

def level_counts(records):
    counter=Counter()
    for record in records:
        """records是列表嵌套字典"""
        counter[record["level"]]+=1
    result={}
    for level in LEVEL_ORDER:
        result[level]=counter.get(level,0)
    return result

def level_percentage(counts):
    total = sum(counts.values())
    result = {}
    for level,num in counts.items():
        percentage = (num/total) if total else 0
        result[level] = f"{percentage:.1%}"
    return result

def time_range(records):
    if not records:
        return "-","-"
    times = [r["timestamp"] for r in records]
    """时间列表"""
    return min(times), max(times)

def normalize(message_str):
    """把消息中数字换为#"""
    return re.sub(r"\d+","#",message_str)

def error_top(records,top_n=5):
    """报错归类"""
    counter=Counter()
    for record in records:
        if record["level"]=="ERROR":
            counter[normalize(record["message"])]+=1
    return counter.most_common(top_n)

"""['a', 'is', 'OK', 'DB']    ← 全抓，全是噪音
    [A-Za-z_]{3,}  →  []          ← 太短的全跳过"""
def keyword_top(records,top_n=5):
    counter=Counter()
    for record in records:
        if record["level"] not in ("WARN","ERROR"):
            continue
        for word in re.findall(r"[A-Za-z_]{3,}",record["message"]):
            word=word.lower()
            if word in STOPWORDS:
                continue
            counter[word]+=1
    return counter.most_common(top_n)

def filter_by_level(records,level):
    """只保留指定级别。level 为空时原样返回。"""
    if not level:
        return records
    level=level.upper()
    return [r for r in records if r["level"]==level]

def build_summary(source,records,total,invalid):
    """汇总"""
    counts=level_counts(records)
    strat,end=time_range(records)
    return {
        "source":source,
        "total_line":total,
        "valid_line":len(records),
        "invalid_line":invalid,
        "time_strat":strat,
        "time_end":end,
        "level_counts":level_counts(records),
        "level_percentage":level_percentage(counts),
        "error_top":error_top(records),
        "keyword_top":keyword_top(records,10)
            }