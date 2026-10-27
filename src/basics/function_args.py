


def calc_sum(a, b, c=0):
    """普通函数 + 默认参数"""
    return a + b + c


def args_demo(*args):
    """可变位置参数，打包成元组"""
    total = 0
    for num in args:
        total += num
    return total


def kwargs_demo(**kwargs):
    """可变关键字参数，打包成字典"""
    for k, v in kwargs.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    print(calc_sum(1, 2))
    print(calc_sum(1, 2, 3))
    print(args_demo(1, 2, 3, 4, 5))
    kwargs_demo(name="Tom", age=18, city="Taiyuan")