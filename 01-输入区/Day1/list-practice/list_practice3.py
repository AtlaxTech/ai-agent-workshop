# 练习三：生成1-20的平方列表
# 写法一：传统写法
result = []
for i in range(1, 21):
    result.append(i ** 2)
print(result)

# 写法二：列表推导式：按照一定的规则快速生成一个列表的方法
# 语法格式1：[插入的值 for i in 序列/列表]
result2 = [i ** 2 for i in range(1, 21)]
print(result2)
