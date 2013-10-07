# coding: utf-8

from cheetahes.utils import rand_weight

import itertools


def monster_loot(monsters, game_config):
    """怪物的掉落数据

    Args:
        monsters: 怪物id们
        game_config: 所需配置：怪物配置，掉落配置

    Returns:
        怪物们的掉落数据
    """
    gold = 0
    heros = []
    equips = []

    for monster in itertools.ifilter(None, monsters):
        drop_id = game_config['monster'][monster]['drop']
        drop = game_config['monster_drop'][drop_id]

        goods_type, goods = rand_weight(**drop)

        if goods_type == 'hero':
            heros.append(goods)

        elif goods_type == 'gold':
            gold += goods[0]

        elif goods_type == 'equip':
            equips.append(goods)

    return {
        'gold': gold,
        'heros': heros,
        'equips': equips,
    }
