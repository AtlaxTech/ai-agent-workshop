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
year = int(input("Please enter a year: "))
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} 是闰年！")
else:
    print(f"{year} 是平年！")
