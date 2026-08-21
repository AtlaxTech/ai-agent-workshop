# 获取键盘上输入的数据
# name = input("Please enter your name: ")
# print(f"Hello, {name}!")

# age = input("Please enter you age: ")
# print(f"your age is {age}")

# practice
# 银行卡中有10000元，现在到ATM进行取钱操作，请根据输入的金额执行取钱操作，取钱完毕后展示银行卡余额
# 步骤
# 1. 输入密码
# 2. 输入取款金额
# 3. 计算余额并输出
balence = 10000
password = "123456"
password = input("Please enter your password: ")
if password != "123456":
    print("Password is incorrect!")
    exit()
else:
    print(f"Password is correct! Your balance is {balence}")
    amount = int(input("Please enter the amount you want to withdraw: "))
    print(f"Your balance is {balence-amount}")
    print("Thank you for using our ATM!")
