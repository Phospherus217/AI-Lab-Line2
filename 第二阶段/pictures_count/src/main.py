from pathlib import Path
from collections import Counter
import csv

"""所有图片格式"""
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
SIZE=["B","KB","MB","GB","TB"]

def word_scan(path):
    list=[]
    for p in path.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        list.append({"路径":p,"类型":p.suffix,"大小":human_size(p.stat().st_size)})
    return list

def human_size(size):
    size = float(size)
    for unit in SIZE:
        if size < 1024 or unit == "GB":
            return f"{size:.2f} {unit}"
        size /= 1024

def count_words(list):
    count=Counter()
    for item in list:
        count[item["类型"]]+=1
    return count

def summary_words(list):
    print(f"图片总数量:{len(list)}")
    print(f"各种图片数量:")
    for key,value in count_words(list).items():
        print(f"{key}:{value}个")

def write_csv(path):
    with open("../output/summary.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f,fieldnames=["路径","类型","大小"])
        writer.writeheader()
        writer.writerows(word_scan(path))
    print("已写入output/summary.csv")

if __name__ == "__main__":
    root = Path("../input")
    summary_words(word_scan(root))
    write_csv(root)



