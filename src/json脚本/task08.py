"""
#注:
该脚本应与所统计文件在同一目录下
"""
import json
from pathlib import Path

def readjson(root):
    count={}
    for f in root.rglob("*.md"):
        with open(f,"r",encoding="utf-8") as file:
            content=file.read().strip()
            contentlen=len(content)
            contentlines=len(content.splitlines())
            count[f.name]=[contentlines,contentlen]
    return count

def dumpjson(data):
    with open("summary.json","w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=4)

def loadjson():
    with open("summary.json","r",encoding="utf-8") as f:
        data=json.load(f)
        return data

def main():
    root = Path("testdata")
    dumpjson(readjson(root))
    print(loadjson())

if __name__=="__main__":
    main()


