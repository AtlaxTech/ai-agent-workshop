class Car:
    def __init__(self, brand, name, price):
        self.brand = brand
        self.name = name
        self.price = price

    def running(self):
        print(f"{self.brand} {self.name} 正在高速行驶中")

    def __str__(self):  # 将当前对象转换成字符串 默认是输出地址
        return f"{self.brand} {self.name} {self.price}"

    def __eq__(self, other):
        return self.price == other.price and self.brand == other.brand and self.name == other.name

    def __lt__(self, other):
        return self.price < other.price


c1 = Car("BMW", "X5", 500000)
print(c1)
c2 = Car("BMW", "X5", 500000)
print(c2)

print(c1 == c2)
print(c1 < c2)
