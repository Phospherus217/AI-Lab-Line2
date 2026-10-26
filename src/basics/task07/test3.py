chinese = ["张三", "李四", "王五", "赵六"]
math    = ["李四", "王五", "钱七"]
english = ["王五", "赵六", "钱七", "孙八"]
print(f"至少选一门课:{len(set(chinese)|set(math)|set(english))}人 "
      f"{list(set(chinese)|set(math)|set(english))}")
print(f"三门都选:{len(set(chinese)&set(math)&set(english))}人 "
      f"{list(set(chinese)&set(math)&set(english))}")
print(f"只选了语文:{len(set(chinese)-(set(math)|set(english)))}人 "
      f"{list(set(chinese)-(set(math)|set(english)))}")
print(f"只选了一门:{len(set(chinese)-(set(math)|set(english))|set(math)-(set(chinese)|set(english))|set(english)-(set(math)|set(chinese)))}人 "
      f"{list(set(chinese)-(set(math)|set(english))|set(math)-(set(chinese)|set(english))|set(english)-(set(math)|set(chinese)))}")
