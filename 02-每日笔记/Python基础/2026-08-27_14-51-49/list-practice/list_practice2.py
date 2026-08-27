# 练习二：合并两个列表中的元素，并对合并的结果进行去重处理
num_list1 = [19, 23, 54, 64, 875, 20, 109, 232, 123, 54]
num_list2 = [55, 80, 72, 35, 60, 123, 54, 29, 91]
print("-----------------原始列表-------------------")
print(num_list1)
print(num_list2)

# 写法一：原始写法 两次遍历，先合并再去重
# merge list
# for num in num_list2:
#     if num not in num_list1:
#         num_list1.append(num)
#
# num_list_result = []
# for num in num_list1:
#     if num not in num_list_result:
#         num_list_result.append(num)

# 写法二：解包合并列表写法：
# 解包：将列表这一类容器解开成独立的元素
# 组包：将多个值合并到一个容器
# num_list = [*num_list1, *num_list2]

# 写法三：AI 推荐写法 直接使用 + 把两个列表直接合并
num_list_result = []
for num in num_list1 + num_list2:
    if num not in num_list_result:
        num_list_result.append(num)

print("-----------------合并后的列表-------------------")
print(f"合并后去重的列表结果：{num_list_result}")
