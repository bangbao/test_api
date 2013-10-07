# coding: utf-8

from collections import defaultdict

import itertools


def delimiter_list(value, delimiter=','):
    """转换字符串到列表，空值转为None

    Args:
        value:  逗号分隔的字符串
        delimiter: 分割符

    Returns:
        转换后的列表
    """
    trans = {'': None}
    temp = value.split(delimiter)

    return [trans.get(key, key) for key in temp]

def delimiter_str(value, delimiter=','):
    """转换列表到字符串, None值转为空值

    Args:
        value: 列表
        delimiter: 分割符

    Returns:
        转换后的字符串
    """
    trans = {None: ''}
    temp = map(str, (trans.get(key, key) for key in value))

    return delimiter.join(temp)


def count(src_list):
    """计算列表元素的数量

    Args:
        src_list: 列表元素们

    Returns:
        元素数量字典
    """
    counts = defaultdict(int)

    for src in src_list:
        counts[src] += 1

    return counts


def lambda_func(default=False):
    """默认的lambda函数

    Args:
        default: 默认返回值

    Returns:
        真正的处理函数
    """
    def func(*args):
        """处理函数

        Args:
            args: 变量们

        Returns:
            返回默认的值
        """
        return default

    return func

