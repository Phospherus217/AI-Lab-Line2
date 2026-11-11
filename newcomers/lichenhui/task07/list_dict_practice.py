def task_list_and_dict():
    """
    练习内容：列表推导式与字典安全取值
    """
    # 1. 列表操作：生成1-10的平方数列表
    numbers = [x ** 2 for x in range(1, 11)]
    print(f"平方数列表: {numbers}")

    # 2. 切片操作：获取前3个元素
    top_3 = numbers[:3]
    print(f"前三个数: {top_3}")

    # 3. 字典操作：使用 get 方法防止报错
    student = {"name": "Alice", "age": 20}
    # 尝试获取不存在的 'score' 键，返回默认值 0
    score = student.get("score", 0)
    print(f"学生分数(默认值): {score}")


if __name__ == "__main__":
    task_list_and_dict()
