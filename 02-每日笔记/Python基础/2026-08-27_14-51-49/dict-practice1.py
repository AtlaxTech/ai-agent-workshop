# 开发一个购物车管理系统，实现商品信息的增删改查操作。系统使用字典结构存储商品数据，通过控制台菜单与用户交互。
# 具体功能如下：
# 1. 添加购物车：用户根据提示录入商品名称、以及商品的价格、数量，保存该商品到购物车
# 2. 修改购物车：要求用户输入要修改的购物车商品名称，然后再提示输入该商品的价格、数量，输入完成后修改该商品信息
# 3. 删除购物车：要求用户输入要删除的商品名称，根据名称删除购物车中的商品
# 4. 查询购物车：将购物车中的商品信息展示出来，格式为：“商品名称：xxx，商品价格：xxx，商品数量：xxx”
# 5. 退出购物车

# 数据结构设计 shopping_cart = {product_name1:{price:xxx, number:xxx}, product_name2:{price:xxx, number:xxx}, ...}
shopping_cart = {}
menu = """
######### 购物车系统 #########
#       1. 添加购物车        #
#       2. 修改购物车        #
#       3. 删除购物车        #
#       4. 查询购物车        #
#       5. 退出购物车        #
############################
"""

# 步骤一：制作菜单
print("欢迎使用购物车系统 ~")
while True:
    print(menu)
    choice = input("请选择要执行的操作（1～5）: ")
    match choice:
        case "1":  # 添加购物车
            product_name = input("Please enter the product name : ")
            if product_name in shopping_cart:
                print("该商品已存在，请重新选择 ～")
            else:
                product_price = float(input("Please enter the product price : "))
                product_number = int(input("Please enter the product number : "))
                shopping_cart[product_name] = {"product_price": product_price, "product_number": product_number}
                print("商品添加成功 ～")
        case "2":  # 修改购物车
            modify_name = input("Please enter the product name you want to modify : ")
            if modify_name not in shopping_cart:
                print("该商品不存在，请重新选择 ～")
            else:
                modify_number = int(input("Please enter the new number you want to modify : "))
                modify_price = float(input("Please enter the new price you want to modify : "))
                shopping_cart[modify_name] = {"product_price": modify_price, "product_number": modify_number}
                print("商品修改成功 ～")
        case "3":  # 删除购物车
            remove_name = input("Please enter the product name you want to remove : ")
            if remove_name not in shopping_cart:
                print("该商品不存在，请重新选择 ～")
            else:
                del shopping_cart[remove_name]
                print("商品删除成功 ～")
        case "4":  # 查询购物车
            for product_name in shopping_cart:
                product_info = shopping_cart[product_name]
                print(
                    f"商品名称：{product_name}，商品价格：{product_info["product_price"]}，商品数量：{product_info["product_number"]}")
        case "5":  # 退出购物车
            print("Bye Bye ~")
            break
        case _:  # 匹配其他所有情况
            print("非法操作，不支持！！！请使用 1～5 进行操作。")
