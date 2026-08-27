# 从给出的列表中提取出所有的偶数，并计算其平方，最后组成一个新的列表。
# 写法一：传统写法
num_list = [19, 23, 54, 64, 87, 20, 109, 232, 123, 43, 26, 55, 72]
result = []
for num in num_list:
    if num % 2 == 0:
        result.append(num ** 2)
print(result)

# 写法二：列表推导式：按照一定的规则快速生成一个列表的方法
# 语法格式2：[插入的值 for i in 序列/列表 + if 条件判断语句]
result2 = [num ** 2 for num in num_list if num % 2 == 0]
print(result2)
