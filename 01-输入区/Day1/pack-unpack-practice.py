# 练习一：两个变量值交换
a = 10
b = 20

a, b = b, a  # 前半部分是解包操作，后半部分是元组组包操作

print(a)
print(b)

# 练习2: 三个变量值交换，分别将a，b，c的值赋值给c，a，b
a = 100
b = 200
c = 300

c, a, b = a, b, c
# a,b,c = c,a,b
print(a)
print(b)
print(c)
