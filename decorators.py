from functools import wraps
from flask import g, redirect

# 装饰器本质是还是一个函数，只是函数调用函数，避免多次重复代码的复制粘贴，提高复用性
def login_requested(func):
    # 保留func的信息，保留调用的函数的信息，然后调用过来的函数可以继续运行下去
    @wraps(func)

    # 传入万能参数 *args是位置参数，**kwargs是可以传入变量的。
    def inner(*args, **kwargs):

        # hasattr 是判断是否有这个属性，判断有没有值
        # if hasattr(g, "user"):
        if g.user:

            # 这里需要返回原来的函数
            return func(*args, **kwargs)

        else:
            return redirect("/auth/login")

    return inner

