# coding: utf-8

from lib.utils import sys_random as random
from lib.utils import rand_weight
from . import constants

import itertools


def rectify_hole(pos_hole):
    """校验零件占位的完整性

    Args:
        pos_hole: 编队列表

    Returns:
        完整的编队
    """
    new_holes = []
    fill = constants.GOBLIN_POS_HOLE_UNOPENED
    DEFAULTS = constants.GOBLIN_POS_HOLE_DEFAULTS

    for i, member in itertools.izip_longest(constants.GOBLIN_POS_HOLE_DEQ,
                                            pos_hole, fillvalue=fill):
        new_holes.append(DEFAULTS.get(member, member))

    return new_holes


def goblin_birth(cfg_id, game_config, **kwargs):
    """由配置ID生成一个能用的零件对象

    Args:
        cfg_id: 配置ID
        game_config: 游戏配置
        kwargs: 动态参数

    Returns:
        零件对象
    """
    obj = dict(cfg_id=cfg_id, level=1, exp=0, level_up=0)

    level = kwargs.pop('level', 1)
    obj = goblin_upgrade(obj, game_config)

    for i in xrange(1, level):
        obj['exp'] = obj['level_up']

        obj = goblin_upgrade(obj, game_config)

    obj.update(kwargs)

    return obj


def goblin_upgrade(obj, game_config):
    """零件升级

    Args:
        obj: 零件对象
        game_config: 游戏配置

    Returns:
        升级后的对象
    """
    exp_type = game_config['goblins'][obj['cfg_id']]['exp_type']
    up_detail = game_config['goblin']
    level = obj['level']
    level_config = up_detail.get(level)

    if not level_config or exp_type not in level_config['detail']:
        return obj

    need_exp = level_config['detail'][exp_type]['need']

    while (need_exp and obj['exp'] - need_exp >= 0):
        level += 1
        obj['exp'] -= need_exp
        obj['level'] = level

        level_config = up_detail.get(level)
        if not level_config:
            obj['exp'] = 0
            break

        need_exp = level_config['detail'][exp_type]['need']

    obj['level_up'] = need_exp - obj['exp']

    return obj


def get_goblin_detail(obj, game_config):
    """获取某个零件的配置信息

    Args:
        obj: 零件对象
        game_config: 游戏配置

    Returns:
        配置中的信息
    """
    goblins = game_config['goblins']

    return goblins[obj['cfg_id']]


def get_forge_config(forge_level, game_config):
    """根据锻造等级获取当前锻造等级配置和下个锻造等级配置

    Args:
        forge_level: 用户锻造等级
        game_config: 游戏配置

    Returns:
        当前锻造等级配置, 下个锻造等级配置
    """
    goblin_get = game_config['goblin_get']

    max_level = max(goblin_get)
    next_level = min(forge_level + 1, max_level)

    return goblin_get[forge_level], goblin_get[next_level]


def goblin_loot(loot):
    """锻造掉落零件

    Args:
        loot: 零件掉落配置

    Returns:
        掉落配置中的一个零件
    """
    good_type, goods = rand_weight(**loot)

    return random.choice(goods)


def goblin_info(obj, game_config, **kwargs):
    """一个零件信息
    """
    detail = get_goblin_detail(obj, game_config)
    base_config = game_config['goblin']
    level, exp_type = obj['level'], detail['exp_type']

    data = {
        'cfg_id': obj['cfg_id'],
        'level': level,
        'exp': obj['exp'],
        'level_up': obj['level_up'],
        'effect_sort': detail['effect_sort'],
        'value': detail['value'] + detail['level_add'] * (level - 1),
        'base': base_config[level]['detail'][exp_type],
        'can_eaten': bool(exp_type),
    }

    data.update(kwargs)

    return data


def calc_merge_cost(dst, merges, game_config):
    """ 计算合成所需要的花费

    Args:
       dst: 目标对象
       merges: 材料列表

    Returns:
       所需要花费的金币
    """
    info = goblin_info(dst, game_config)

    return info['base']['cost'] * len(merges)


def goblin_merge(dst, merges, game_config):
    """零件合成
    """
    add_exp = sum(obj['base']['eaten'] for obj in merges)

    dst['exp'] += add_exp

    return goblin_upgrade(dst, game_config)


def apply_goblin_effect(obj, pos_goblins):
    """应用零件效果

    Args:
        obj: 卡牌对象
        pos_goblins: 编队位置零件们

    Returns:
        应用效果后的卡牌对象
    """
    for goblin in itertools.ifilter(None, pos_goblins):
        attr = constants.GOBLIN_EFFECT_SORT_MAP[goblin['effect_sort']]

        if attr in obj:
            obj[attr] += goblin['value']

    return obj


def filter_goblin_merge(game_config):
    """过滤不能合成的零件

    Args:
        game_config: 游戏配置

    Returns:
        是否能合成的过滤函数
    """
    goblins = game_config['goblins']
    exp_type = constants.GOBLIN_EXP_TYPE_NOT_MERGE

    def wrapper(obj):
        """判断零件是否可合成，或当材料

        Args:
            obj: 零件对象

        Returns:
            是否可合成
        """
        return goblins[obj['cfg_id']]['exp_type'] != exp_type

    return wrapper

