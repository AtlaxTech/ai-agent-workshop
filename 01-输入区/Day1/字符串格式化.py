name = "张三"
age = 18
project = "Applied AI Engineering"
hobby = "Playing Sports"

# 正常字符串拼接
print("大家好，我是" + name + "，今年" + str(age) + "岁，学习的专业是 " + project + "，爱好是 " + hobby)

# 字符串格式化拼接 -- 方式一
print("大家好，我是 %s ，今年 %s 岁，学习的专业是 %s，爱好是 %s" %(name, age, project, hobby))

# 字符串格式化拼接 -- 方式二（推荐方式，更简洁）
print(f"大家好，我是{name}，今年{age}岁，学习的专业是 {project}，爱好是 {hobby}")