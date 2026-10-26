visits = ["张三", "李四", "张三", "王五", "李四",
          "张三", "赵六", "王五", "张三"]
print(f"总来访次数:{len(visits)}")
print(f"不同人数:{len(set(visits))}")
def count(visits):
    count={}
    for visit in visits:
        count[visit]=count.get(visit,0)+1
    return count
print(f"来访明细:{count(visits)}")
def count_last_2(count):
    count_=[]
    for visit,times in count.items():
        if times>=2:
            count_.append(visit)
    return count_
print(f"来访>=2次:{count_last_2(count(visits))}")
"""保留原始顺序去重"""
def unique(visits):
    unique=[]
    for visit in visits:
        if visit not in unique:
            unique.append(visit)
    return unique
print(f"去重后顺序:{unique(visits)}")