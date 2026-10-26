def split_words(text):
    for mark in ",.!?;:\"'()":
        text = text.replace(mark, " ")
    words = text.lower().split()
    return words
def count_words(words):
    counter = {}
    for word in words:
        counter[word] = counter.get(word, 0) + 1
    return counter
def unique_count(words):
    unique = set(words)
    return len(unique)
def top_n(counter, n=3):
    pairs = []
    for word in counter:
        pairs.append((counter[word], word))
    pairs.sort(reverse=True)      # 元组排序：先比次数，次数相同比单词
    return pairs[:n]
def show_top(pairs):
    for rank, pair in enumerate(pairs, start=1):
        times = pair[0]
        word = pair[1]
        print(f"  第 {rank} 名  {word}  出现 {times} 次")
def main():
    text = (
        "Python is simple. Python is powerful. "
        "I like Python, and Python likes me. "
        "Simple is better than complex."
    )
    print("原文：")
    print(text)
    words = split_words(text)
    print("\n切出来的单词：")
    print(words)
    counter = count_words(words)
    print("\n每个单词出现的次数：")
    for word in counter:
        print(f"  {word}: {counter[word]}")
    print("\n总单词数：", len(words))
    print("不同单词数：", unique_count(words))
    print("\n出现最多的 3 个：")
    show_top(top_n(counter, 3))
if __name__ == "__main__":
    main()
