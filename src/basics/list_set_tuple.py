


def list_operate():
    lst = [2, 5, 8, 5, 2, 9, 11]
    # 去重，转集合再转回列表
    unique_lst = list(set(lst))
    print("原始列表：", lst)
    print("去重后：", unique_lst)
    # 切片
    print("切片 [1:4]:", lst[1:4])


def set_calc():
    s1 = {1, 2, 3, 4, 5}
    s2 = {4, 5, 6, 7, 8}
    print("交集：", s1 & s2)
    print("并集：", s1 | s2)
    print("差集 s1-s2：", s1 - s2)


def tuple_test():
    t = (10, 20, 30)
    print("元组：", t)
    print("元组不能修改，t[0] = 99 会报错")


if __name__ == "__main__":
    list_operate()
    set_calc()
    tuple_test()