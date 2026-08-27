# 定义类
class Car:
    pass


# 创建对象
c1 = Car()
# 动态为对象添加属性 ----> 不推荐 降低代码可读性
c1.color = "red"
c1.brand = "BMW"
c1.name = "X5"
c1.price = 500000

print(c1)
print(c1.brand)
print(c1.__dict__)
