"""
# 定义类
class 类名:
    # 初始化方法行参第一个值必须是 self 相当于 java 中的 this，表示当前创建的实例对象
    def __init__(self, 参数列表): # 初始化方法，对象创建后自动调用，主要用于设置对象的厨师状态（设置对象属性）
        self.属性名 = 参数值
        self.属性名 = 参数值

# 创建对象
对象名 = 类名(参数列表)
"""


# 说明：定义在类的外面称为函数，定义在类中的函数称为方法
class Car:
    def __init__(self, c_brand, c_name, c_price):
        self.brand = c_brand
        self.name = c_name
        self.price = c_price


c1 = Car("BMW", "X5", 500000)
print(c1.__dict__)
