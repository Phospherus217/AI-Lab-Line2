"""练习3：Tuple、Set、函数参数 *args **kwargs"""

def set_operation(set_a, set_b):
    """集合交、并、差运算"""
    union_set = set_a | set_b
    inter_set = set_a & set_b
    diff_set = set_a - set_b
    print(f"并集：{union_set}")
    print(f"交集：{inter_set}")
    print(f"差集 a-b：{diff_set}")


def func_demo(name, age=18, *args, **kwargs):
    """
    函数演示：默认参数、可变位置参数*args、可变关键字参数**kwargs
    :param name: 姓名
    :param age: 年龄，默认18
    :param args: 不定长位置参数
    :param kwargs: 不定长关键字参数
    """
    print(f"name: {name}, age: {age}")
    print(f"*args 内容：{args}")
    print(f"**kwargs 内容：{kwargs}")


if __name__ == "__main__":
    # 元组测试：不可变
    t = (1, 2, 3)
    print("元组：", t)
    # t[0] = 99  # 放开这行会报错：元组不可修改

    # 集合去重 + 交并差
    s1 = {1, 2, 3, 4}
    s2 = {3, 4, 5, 6}
    set_operation(s1, s2)

    # 调用带 *args **kwargs 的函数
    func_demo("LiSi", 20, "basketball", "game", city="Taiyuan", grade="大一")
