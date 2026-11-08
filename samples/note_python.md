# Python 学习笔记

## 一、变量与类型

Python 是动态类型语言，变量不需要声明类型，赋值即创建。
常用基础类型有 int、float、str、bool。

## 二、f-string 格式化

推荐写法：`f"{name} 今年 {age} 岁"`。

相比 `%` 和 `str.format`，f-string 更直观，也更快。

## 三、列表推导式

把 for 循环压缩成一行：

```python
squares = [n * n for n in range(10)]
```

注意：推导式适合简单逻辑，超过两层嵌套就应该改回普通循环。
