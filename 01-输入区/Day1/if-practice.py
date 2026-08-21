# 练习1：结合输入输出以及if条件判断的知识，完成一个模拟登录功能的实现（正确账号和密码为18888888888/666888）
# 1. 提示用户输入账号和密码
# 2. 判断账号和密码是否正确
# 3. 如果账号和密码有一个错误，则登录失败，提示错误信息。
import getpass
import pwinput
#
# account_setup = "18888888888"
# pass_setup = "666888"
#
# account_input = input("Please enter your account: ")
# pass_input = pwinput.pwinput("Please enter your password: ", mask='*')
#
# if account_input == account_setup and pass_input == pass_setup:
#     print("Login successful!")
# else:
#     print("Login failed!")

# 练习2:根据用户输入的年份，判断是闰年还是平年
# 1. 非整百年份，且能被4整除的年份是闰年
# 2. 整百年份（如1900年、2000年）必须能被400整除才是闰年
# year = int(input("Please enter a year: "))
# if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
#     print(f"{year} 是闰年！")
# else:
#     print(f"{year} 是平年！")

# 练习3:
# 1. 根据用户输入的数字，判断该数字是奇数还是偶数
print("根据用户输入的数字，判断该数字是奇数还是偶数")
num = int(input("Please enter a number: "))
if num % 2 == 0:
    print(f"{num} is even")
else:
    print(f"{num} is odd")
print("-----------------------------------------------------")

# 2. 根据用户输入的年龄判断用户是否成年（>=18表示成年否则未成年）
print("根据用户输入的年龄判断用户是否成年（>=18表示成年否则未成年）")
user_age = int(input("Please enter your age: "))
if user_age >= 18:
    print(f"{user_age} is adult")
else:
    print(f"{user_age} is teenager")
print("-----------------------------------------------------")

# 3. 根据用户输入的数字判断数字是正数还是负数（不考虑0）
print("根据用户输入的数字判断数字是正数还是负数（不考虑0）")
number = int(input("Please enter a number: "))
if number > 0:
    print(f"{number} is positive")
elif number < 0:
    print(f"{number} is negative")
else:
    print(f"{number} is zero")
print("-----------------------------------------------------")

# 4. 根据用户输入的分数判断分数是否及格（>=60表示及格）
print("根据用户输入的分数判断分数是否及格（>=60表示及格）")
score = int(input("Please enter your score: "))
if score >= 60:
    print(f"{score} is passed")
else:
    print(f"{score} is failed")
