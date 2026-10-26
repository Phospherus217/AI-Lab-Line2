# -*- coding: utf-8 -*-
"""日志解析模块：把一行文本解析成结构化记录。"""

from datetime import datetime
from pathlib import Path

VALID_LEVELS = {"DEBUG","INFO","WARN","ERROR"}

def parse_line(line):
    line=line.strip()
    if not line.strip():
        return None
    parts=line.split(" ",3)
    if len(parts) < 4:
        return None
    data_str,time_str,level_str,message_str=parts
    if level_str not in VALID_LEVELS:
        return None
    timestamp=f"{data_str} {time_str}"
    try:
        datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    return {"timestamp":timestamp,"level":level_str,"message":message_str.strip()}

def parse_file(path):
    """记录列表
    总行数
    无效"""
    records=[]
    total=0
    invalid=0
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            total+=1
            record=parse_line(line)
            if record is None:
                invalid+=1
                continue
            records.append(record)
    return records,total,invalid

def parse_file_safe(path):
    """文件路径异常或编码错误时使用"""
    if not Path(path).exists():
        raise FileNotFoundError(f"路径文件不存在:{path}")
    try:
        return parse_file(path)
    except UnicodeDecodeError:
        raise ValueError(f"文件不是 UTF-8 编码：{path}")