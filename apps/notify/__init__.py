# coding: utf-8

from cheetahes.core.environ import RUNTIME_INFO


def notify(env, errno):
    """错误提示接口

    当 filters 检查出请求不符合条件时， 设置env的报错信息, 返回True, 中断请求

    Args:
        env: 运行环境
        errno: 错误代号

    Returns:
        True
    """
    text = env.game_config['text']

    env.errno = RUNTIME_INFO
    env.msg = text[errno]['text']

    return True

def checker(func):
    """错误提示装饰器

    Args:
        func: 检查函数

    Returns:
        错误提示函数
    """
    def decorator(env, *args, **kwargs):
        """错误提示函数

        Args:
            env: 运行环境

        Returns:
            是否需要错误提示
        """
        errno = func(env, *args, **kwargs)

        if errno:
            return notify(env, errno)

    return decorator
