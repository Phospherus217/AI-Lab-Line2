def task_function_design():
    """
    练习内容：函数定义与不定长参数
    """

    # 定义一个计算总分的函数
    def calculate_score(name, *args, **kwargs):
        """
        name: 学生姓名
        *args: 接收所有分数 (例如: 90, 80)
        **kwargs: 接收其他信息 (例如: subject="Math")
        """
        total = sum(args)
        extra_info = kwargs.get("subject", "综合")
        return f"{extra_info}科目 - {name} 的总分是: {total}"

    # 调用函数
    result = calculate_score("Bob", 85, 90, 95, subject="数学")
    print(result)


if __name__ == "__main__":
    task_function_design()
