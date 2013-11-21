# coding: utf-8

import bisect
import random

sys_random = random.SystemRandom()


def get_it(probability, weight=100):
    """ 判断概率是否命中

    随机0-weight断当前指定的概率是否符合要求
    
    Args:
       probability: 指定概率
       weight: 最高权重

    Returns:
       是否命中
    """
    return sys_random.randint(0, weight) <= probability


def rand_weight(weight, weights, goods):
    """随机一个值

    Args:
       weight: max（weights）
       weights：从小到大 的权重列表
       goods: 跟weights对应的列表

    Returns:
       随机出的值
    """
    w = sys_random.randint(0, weight)
    idx = bisect.bisect_left(weights, w)

    return goods[idx]
