# 函数嵌套调用采用栈结构后进先出
def function_a():
    print("a ... before")
    function_b()
    print("a ... after")


def function_b():
    print("b ... before")
    function_c()
    print("b ... after")


def function_c():
    print("c ...")


function_a()

print("函数调用完毕 ～")
