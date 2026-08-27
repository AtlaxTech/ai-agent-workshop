print("Hello, World!")
###########################################
# python 的四种基本数据类型
# 整数（int）
age = 25
# 浮点数（float）
height = 1.75
# 字符串（str）
message = "This is a String!"
# 布尔值（bool）
is_student = True

print(message)
print(age)
print(height)
print(is_student)

print(type(age), type(height), type(message), type(is_student))
###########################################
# list 列表
# 定义一个列表变量
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "orange"]
# 输出：[1, 2, 3, 4, 5]
print(numbers)
# 输出：['apple', 'banana', 'orange']
print(fruits)

# 查看列表的类型
# 输出：<class 'list'>
print(type(numbers))

# 修改列表中的元素
fruits[0] = '李子'
# 输出：['李子', 'banana', 'orange']
print(fruits)

# 添加元素到列表中
fruits.append('peach')
# 输出：['李子', 'banana', 'orange', 'peach']
print(fruits)

###########################################
# tuple 元组
# 定义一个元组变量
fruits_tuple = ('apple', 'banana', 'orange')
# 输出：('apple', 'banana', 'orange')
print(fruits_tuple)
# 输出：<class 'tuple'>
print(type(fruits_tuple))
# 元组中的元素不能被修改
# 输出：'tuple' object does not support item assignment
# fruits_tuple[0] = '李子'
print(fruits_tuple)

###########################################
# for 循环
# 遍历列表/元组中的每个元素
for f in fruits:
    print(f)

# 遍历数字序列
# 常见搭配可以使用 range() 函数
# range从 0 开始计数
for i in range(5):
    print(i)

# 遍历数字序列+复杂操作
# 例如：计算 0 到 4 的平方
for i in range(5):
    print(i**2)