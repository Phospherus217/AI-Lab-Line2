def task_set_and_tuple():
    """
    练习内容：集合去重与元组操作
    """
    # 1. 集合操作：列表去重
    raw_data = [1, 2, 2, 3, 4, 4, 5]
    unique_data = list(set(raw_data))
    print(f"去重后的数据: {unique_data}")

    # 2. 集合运算：求交集 (共同拥有的元素)
    set_a = {1, 2, 3}
    set_b = {2, 3, 4}
    common = set_a & set_b
    print(f"A和B的交集: {common}")

    # 3. 元组操作：解包赋值
    coordinates = (10, 20)
    x, y = coordinates
    print(f"坐标 X: {x}, Y: {y}")


if __name__ == "__main__":
    task_set_and_tuple()
