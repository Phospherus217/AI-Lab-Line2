"""练习2：Dict 字典操作"""

def dict_demo():
    student = {
        "name": "Zhangsan",
        "age": 18,
        "major": "Software"
    }
    print("原始字典：", student)

    # 查：get（找不到key不会报错，返回默认值）
    print("get name：", student.get("name"))
    print("get score，不存在返回0：", student.get("score", 0))

    # 增改
    student["score"] = 90
    print("新增score：", student)
    # 删除
    del student["major"]
    print("删除major：", student)

    # 字典推导式
    double_dict = {k: v * 2 for k, v in {"a": 1, "b": 2, "c": 3}.items()}
    print("字典推导式：", double_dict)


if __name__ == "__main__":
    dict_demo()
