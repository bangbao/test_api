# coding: utf-8

import itertools

from . import destinys
from . import constants


def add_destiny_effect(user, formation):
    """添加编队命运点亮标识

    Args:
        user: 用户对象
        formation: 编队对象们
    """
    game_config = user.env.game_config
    hero_app = user.env.import_app('hero')
    hero_logics = hero_app.logics
    cmp_sort = cmp_destiny_sort(user, formation)

    for obj in itertools.ifilter(None, formation):
        detail = hero_logics.get_hero_detail(obj, game_config)
        hero_logics.subjoin_destiny_info(obj, detail, game_config,
                                         cmp_sort=cmp_sort)


def apply_destiny_effect(user, formation):
    """卡牌编队应用命运效果

    Args:
        user: 用户对象
        formation: 编队对象们
    """
    game_config = user.env.game_config
    destinys_conf = game_config['destinys']
    hero_app = user.env.import_app('hero')
    hero_logics = hero_app.logics
    cmp_sort = cmp_destiny_sort(user, formation)

    for obj in itertools.ifilter(None, formation):
        hero_detail = hero_logics.get_hero_detail(obj, game_config)

        for cfg_id in hero_detail['destiny']:
            detail = destinys_conf[cfg_id]

            if cmp_sort(detail):
                effect_apply(obj, detail, game_config)


def cmp_destiny_sort(user, formation):
    """判断命运是否生效

    需要前置处理用户编队，装备，零件数据， 使用闭包

    Args:
        user: 用户对象
        formation: 编队对象们

    Returns:
        判断命运是否生效的闭包
    """
    game_config = user.env.game_config
    hero_app = user.env.import_app('hero')
    equip_app = user.env.import_app('equip')
    goblin_app = user.env.import_app('goblin')
    hero_logics = hero_app.logics
    equip_logics = equip_app.logics

    equips = user.hero.equips
    goblins = user.hero.goblins
    used_equip = equip_app.get_used_equip(user)
    used_goblin = goblin_app.get_used_goblin(user)

    hero_type_set = set()
    party_type_set = set()
    equip_type_set = set()
    goblin_type_set = set()

    for obj in itertools.ifilter(None, formation):
        detail = hero_logics.get_hero_detail(obj, game_config)
        hero_type_set.add(detail['destiny_type'])
        party_type_set.add(detail['party'])

    for equip_id in used_equip:
        detail = equip_logics.get_equip_detail(equips[equip_id], game_config)
        equip_type_set.add(detail['destiny_type'])

    for goblin_id in used_goblin:
        goblin_type_set.add(goblins[goblin_id]['cfg_id'])

    own_sort_sets = {
        constants.DESTINY_SORT_HERO: hero_type_set,
        constants.DESTINY_SORT_EQUIP: equip_type_set,
        constants.DESTINY_SORT_GOBLIN: goblin_type_set,
        constants.DESTINY_SORT_PARTY: party_type_set,
    }

    def cmp_sort(detail):
        """判断命运是否生效 若需要条件是已有条件的子集，是为生效

        Args:
            detail: 命运配置

        Returns:
            命运是否生效的布尔值
        """
        target_set = set(detail['target'])
        own_set = own_sort_sets.get(detail['sort'], set())

        return target_set.issubset(own_set)

    return cmp_sort


def effect_apply(obj, detail, game_config):
    """应用命运效果

    Args:
        obj: 战斗对象
        detail: 该命运详细配置
        game_config: 游戏配置
    """
    effect_func_key = 'destiny_effect%d' % detail['effect_sort']
    effect_func = getattr(destinys, effect_func_key)

    effect_func(obj, detail, game_config)


