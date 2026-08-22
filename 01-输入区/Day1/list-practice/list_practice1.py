# 练习一：将用户输入的十个数字，存储到一个列表中，并将列表中的数字进行排序，输出其中的最小值、最大值和平均值
user_input_list = []
user_input_sum = 0
for i in range(10):
    user_input = int(input("Please enter a number: "))
    user_input_list.append(user_input)
    user_input_sum += user_input

print("-------------排序前列表---------------")
print(user_input_list)
print("-------------AI建议写法与结果---------------")
# print("用户输入的最小值：" + min(user_input_list))
# print("用户输入的最大值：" + max(user_input_list))
# print("用户输入的平均值：" + sum(user_input_list) / len(user_input_list))
user_input_min_ai = min(user_input_list)
user_input_max_ai = max(user_input_list)
user_input_average_AI = sum(user_input_list) / len(user_input_list)
print(f"用户输入的最小值：{user_input_min_ai}")
print(f"用户输入的最大值：{user_input_max_ai}")
print(f"用户输入的平均值：{user_input_average_AI}")

user_input_list.sort()
user_input_min = user_input_list[0]
user_input_max = user_input_list[-1]
user_input_average = user_input_sum / len(user_input_list)

print("-------------排序后列表---------------")
print(user_input_list)
print("-------------最终结果---------------")
print(f"用户输入的最小值：{user_input_min}")
print(f"用户输入的最大值：{user_input_max}")
print(f"用户输入的平均值：{user_input_average}")
