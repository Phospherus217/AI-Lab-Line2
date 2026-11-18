"""练习1：List 列表操作"""

def list_demo():
    # 初始化列表
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("原始列表：", nums)

    # 增
    nums.append(10)
    print("append后：", nums)
    # 改
    nums[0] = 99
    print("修改第一个元素：", nums)
    # 删
    nums.pop()
    print("pop删除末尾：", nums)
    # 切片 [start:end:step]
    slice_part = nums[1:5]
    print("切片 1:5：", slice_part)
    # 列表推导式：筛选偶数
    even_list = [x for x in nums if x % 2 == 0]
    print("推导式筛选偶数：", even_list)


if __name__ == "__main__":
    list_demo()
