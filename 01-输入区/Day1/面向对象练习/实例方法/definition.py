class Car:
    def __init__(self, c_color, c_brand, c_name, c_price):
        self.color = c_color
        self.brand = c_brand
        self.name = c_name
        self.price = c_price
        print("Car 类型的对象初始化完毕，对象属性已经添加完毕")

    # 定义实例方法
    def running(self):
        print(f"{self.brand} {self.name} 正在高速行驶中")

    def total_cost(self, discount, rate):
        """
        计算提车的总费用
        :param discount: 折扣
        :param rate: 税率
        :return: 提车总费用
        """
        return self.price * discount + self.price * rate


c1 = Car("red", "BMW", "x5", 500000)
c1.running()
total = c1.total_cost(0.99, 0.2)
print("提车的总费用为：", total)
