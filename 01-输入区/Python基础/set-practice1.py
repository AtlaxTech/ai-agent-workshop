# 根据提供的班级学生的选课情况，完成如下需求：
# 1. 找出同时选修了法语和艺术的学生
# 2. 找出同时选修了所有四门课的学生
# 3. 找出选修了足球，但是没有选修篮球的学生
# 4. 统计每一个学生选修的课程数量

# 选修足球学生的名单
football_set = {"王林", "曾牛", "徐立国", "遁天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"}
# 选修篮球学生名单
basketball_set = {"张铁", "墨居仁", "王林", "姜老道", "曾牛", "王蝉", "韩立", "天运子", "李化元", "厉飞雨", "云露"}
# 选修法语学生名单
french_set = {"许木", "王卓", "十三", "虎咆", "姜老道", "天运子", "红蝶", "厉飞雨", "韩立", "曾牛"}
# 选修艺术学生名单
art_set = {"遁天", "天运子", "韩立", "虎咆", "姜老道", "紫灵"}

# 1. 找出同时选修了法语和艺术的学生
# 方式1：
r1 = french_set.intersection(art_set)
print(f"同时选修了法语和艺术的学生（方式一）：{r1}")
# 方式2: & -- > 交集
fa_set = french_set & art_set
print(f"同时选修了法语和艺术的学生（方式二）：{fa_set}")

# 2. 找出同时选修了所有四门课的学生
r2 = football_set.intersection(basketball_set, french_set, art_set)
print(f"同时选修了所有四门课的学生（方式一）：{r2}")
# 方式2: & -- > 交集
all_set = french_set & art_set & football_set & basketball_set
print(f"同时选修了所有四门课的学生（方式一）：{all_set}")

# 3. 找出选修了足球，但是没有选修篮球的学生
# 方式一：差集 s.difference(b)
r3 = football_set.difference(basketball_set)
print(f"选修了足球，但是没有选修篮球的学生（方式一）：{r3}")
# 方式二：- --> 差集
fb_set = football_set - basketball_set
print(f"选修了足球，但是没有选修篮球的学生（方式二）：{fb_set}")
# 方式三：集合推导式
# 快速构建集合，语法：{要往集合中添加的数据 for s in set1 if 条件}
fb_set3 = {s for s in football_set if s not in basketball_set}
print(f"选修了足球，但是没有选修篮球的学生（方式三）：{fb_set3}")

# 4. 统计每一个学生选修的课程数量
print("----------------------统计每一个学生选修的课程数量--------------------------")
# 4.1 获取学生名单（并集会自动去重）
# 方式一：并集
all_union_set1 = football_set.union(basketball_set).union(french_set).union(art_set)
# 方式二：并集运算符 |
all_union_set2 = football_set | basketball_set | french_set | art_set

# 4.2 获取每个学生选择的课程数量
# 解包放到列表中
all_list = [*football_set, *basketball_set, *french_set, *art_set]
for s in all_union_set2:
    print(f"{s} 选修了 {all_list.count(s)} 课程")
