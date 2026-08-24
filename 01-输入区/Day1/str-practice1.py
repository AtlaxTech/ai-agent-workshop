# 邮箱格式验证：用户输入一个邮箱，验证邮箱格式是否正确（包含一个 `@` 和至少一个 `.`），如果输入正确，输出“邮箱格式正确”，否则输出“邮箱格式错误”
user_input_email = input("Please enter your email address: ")
if user_input_email.count('@') == 1 and user_input_email.count('.') != 0:
    print("邮箱格式正确")
else:
    print("邮箱格式错误")
