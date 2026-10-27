


def list_compre():
    # 筛选1~20里面的偶数
    even = [i for i in range(1, 21) if i % 2 == 0]
    print("偶数列表：", even)


def dict_compre():
    words = ["apple", "banana", "orange"]
    # key:单词，value:单词长度
    word_len = {w: len(w) for w in words}
    print("单词长度字典：", word_len)


if __name__ == "__main__":
    list_compre()
    dict_compre()