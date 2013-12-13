# coding: utf-8

import time
import bisect
import itertools
from collections import defaultdict

from lib.utils import sys_random as random
from lib.utils import rand_weight
from apps.public import logics as publics
from apps.public.generator import salt_generator
from . import constants
from . import logics


def only_resolve_equip(env, equip_id, game_config):
    """分解装备

    Args:
        env: 运行环境
        equip_id: 装备ID
        game_config: 游戏配置，包括装备配置

    Returns:
        获得的物品
    """
    user = env.user
    user_hero = user.hero
    equip_config = game_config['equip']
    resolve_config = game_config['equip_resolve']
    game_app = env.import_app('game')

    obj = user_hero.equips[equip_id]
    detail = logics.get_equip_detail(obj, game_config)

    gain_gold = equip_config[obj['level']]['detail'][detail['star']]['sell']
    loot = resolve_config[detail['star']][detail['sort']]

    game_app.incr_user_attr(user, gold=gain_gold)
    loot_material = resolve_loot(user, loot)
    del_equips(user, [equip_id])

    return {
        'gold': gain_gold,
        'material': loot_material,
    }


def auto_resolve_equip(env, game_config):
    """自动分解装备，把2星以下的装备全部分解

    Args:
        env: 运行环境
        equip_id: 装备ID
        game_config: 游戏配置

    Returns:
        获得的物品
    """
    user = env.user
    user_hero = user.hero
    equip_config = game_config['equip']
    resolve_config = game_config['equip_resolve']
    game_app = env.import_app('game')
    used_equip = get_used_equip(user)

    gain_gold = 0
    loot_material = []
    elements = set()

    for equip_id, obj in user_hero.equips.iteritems():
        detail = logics.get_equip_detail(obj, game_config)

        if equip_id not in used_equip and detail['star'] < 2:
            elements.add(equip_id)
            gain_gold += equip_config[obj['level']]['detail'][detail['star']]['sell']

            loot_cfg = resolve_config[detail['star']][detail['sort']]
            loot_data = resolve_loot(user, loot_cfg)
            loot_material.extend(loot_data)

    game_app.incr_user_attr(user, gold=gain_gold)
    del_equips(user, elements)

    return {
        'gold': gain_gold,
        'material': loot_material,
    }


def pre_merge_equip(env):
    """合成装备前页面
    """
    user = env.user
    game_config = env.game_config
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    equips_cfg, equip_merge_cfg = logics.filter_merge_equip(game_config)

    return {
        'game': game_app.get_game_data(user),
        'team': hero_app.team_get(user),
        'team_equip': get_team_equip(user),
        'equips': format_equips(user, user.hero.equips.iterkeys()),
        'configs': {
            'equips': game_config['equips'],
            'equips_merge': equips_cfg,
            'equip_merge': equip_merge_cfg,
            'equip_quality': game_config['equip_quality'],
            'equip_ability_map': constants.EQUIP_ABILITY_DATA,
        },
    }


def merge_equip(env):
    """合成装备
    """
    user = env.user
    cfg_id = env.params['cfg_id']
    elements = env.params['elements']
    game_config = env.game_config
    game_app = env.import_app('game')
    quality = game_config['equip_quality'][cfg_id]

    rebate_gold = calc_merge_rebate(user, elements)
    cost_gold = rebate_gold - quality['cost']['gold']

    game_app.incr_user_attr(user, gold=cost_gold)
    del_equips(user, elements)
    birth_equip(user, quality['dest'], where=constants.EQUIP_FROM_MERGE)

    env.user.save_all()

    return pre_merge_equip(env)


def sell_equip(env):
    """售卖装备

    Args:
        elements: 装备ID们

    Returns:
        背包
    """
    elements = env.params['elements']
    game_config = env.game_config

    user = env.user
    user_hero = user.hero
    equip_config = game_config['equip']
    game_app = env.import_app('game')
    gold = 0

    for element in elements:
        obj = user_hero.equips[element]
        detail = logics.get_equip_detail(obj, game_config)
        level, star = obj['level'], detail['star']

        gold += obj['gold'] + equip_config[level]['detail'][star]['sell']

    game_app.incr_user_attr(user, gold=gold)
    del_equips(user, elements)

    env.user.save_all()

    data = team_equip(env)
    data['elements'] = elements
    data['configs'] = {
        'hero': game_config['hero'],
    }

    return data


def clear_equip(env):
    """清空装备cd时间
    """
    user = env.user
    game_app = env.import_app('game')

    set_st_data(user, -user.hero.data['st_cd'])

    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'st_data': get_st_data(user),
    }


def ratio_equip(env):
    """改变装备强化成功率
    """

    user = env.user
    game_app = env.import_app('game')

    # TODO vip功能添加时完善
    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'success_ratio': get_equip_ratio(user),
    }


def birth_equip(user, cfg_id, where=0, ext=0, **kwargs):
    """生成一个装备对象添加到用户数据中

    Args:
        user: 用户对象
        cfg_id: 配置id
        where: 来源
        ext: 扩展标识
        kwargs: 动态参数

    Returns:
        装备数据
    """
    game_config = user.env.game_config

    equip = logics.equip_birth(cfg_id, game_config, **kwargs)

    return add_equip(user, equip, where, ext)


def add_equip(user, equip, where=0, ext=0):
    """添加一个新装备对象并保存到用户数据中

    Args:
        user: 用户对象
        equip: 数据对象
        where: 来源
        ext: 扩展标识

    Returns:
        装备数据
    """
    obj_id = '%s_%d%s_%d_%d%s' % (user.pk,
                                  int(time.time()),
                                  salt_generator(),
                                  equip['cfg_id'],
                                  where,
                                  ext)
    user.hero.equips.add(obj_id, **equip)

    return {
        'equip_id': obj_id,
        'equip': equip,
    }


def del_equips(user, equip_ids):
    """删除多个装备

    删除装备， 若装备在使用中，不删除

    Args:
        user: 用户对象
        equip_ids: 要删除的装备id们
    """
    user_hero = user.hero
    used_equip = get_used_equip(user)

    for equip_id in equip_ids:
        if equip_id not in used_equip:
            user_hero.equips.remove(equip_id)


def get_used_equip(user):
    """获取使用中的装备id

    Args:
        user: 用户对象

    Returns:
        装备id集合
    """
    used_equip = {}

    for pos in constants.EQUIP_TEAM_POS_KEYS:
        equip_data = get_pos_equip(user, pos)

        for equip_id in itertools.ifilter(None, equip_data.itervalues()):
            used_equip[equip_id] = pos

    return used_equip


def get_team_equip(user):
    """获取编队装备

    Args:
        user: 用户对象

    Returns:
        编队装备
    """
    return dict((pos, get_pos_equip(user, pos))
                 for pos in constants.EQUIP_TEAM_POS_KEYS)


def get_pos_equip(user, pos):
    """获取一个位置的装备

    Args:
        user: 用户对象
        pos: 装备编队位置
        value: 存储的装备格式字符串

    Returns:
        装备字典
    """
    value = user.game.equip[pos]
    pos_list = publics.delimiter_list(value)

    return dict(itertools.izip_longest(constants.EQUIP_TEAM_WHERE_KEYS,
                                       pos_list))


def set_pos_equip(user, pos, pos_equip):
    """设定一个位置的装备

    Args:
        user: 用户对象
        pos: 编队位置
        pos_equip: 此编队的装备
    """
    equips = (pos_equip.get(where)
              for where in constants.EQUIP_TEAM_WHERE_KEYS)

    user.game.equip[pos] = publics.delimiter_str(equips)


def format_equips(user, equip_ids, filter_func=None):
    """获取装备背包数据

    Args:
        user: 用户对象
        equip_ids: id们
        filter_func: 过滤函数

    Returns:
        装备背包数据
    """
    user_hero = user.hero
    game_config = user.env.game_config
    equips = defaultdict(dict)

    if not callable(filter_func):
        filter_func = publics.lambda_func(default=True)

    for equip_id in itertools.ifilter(None, equip_ids):
        obj = user_hero.equips[equip_id]

        if filter_func(obj):
            info = logics.equip_info(obj, game_config, equip_id=equip_id)
            sort_key = constants.EQUIP_SORT_WHERES[info['sort']]
            equips[sort_key][equip_id] = info

    return equips


def apply_equip_effect(user, formation):
    """卡牌编队应用装备效果

    Args:
        user: 用户对象
        formation: 编队对象列表

    Returns:
        应用效果后编队对象列表
    """
    equips = user.hero.equips

    for pos, obj in itertools.izip(constants.EQUIP_TEAM_POS_KEYS, formation):
        if obj:
            pos_equip = get_pos_equip(user, pos)
            pos_equips = (equips.get(equip_id)
                          for equip_id in pos_equip.itervalues())
            logics.apply_equip_effect(obj, pos_equips)


def get_equip_incr(user, game_config):
    """获取装备强化增长数据

    Args:
        env: 运行环境
        game_config: 游戏配置，包括装备配置

    Returns:
        增长数据
    """
    equip_incr = {}

    for obj in user.hero.equips.itervalues():

        if obj['cfg_id'] not in equip_incr:
            detail = logics.get_equip_detail(obj, game_config)
            equip_incr[obj['cfg_id']] = logics.get_equip_incr(detail)

    return equip_incr


def get_equip_ratio(user):
    """获取强化成功率

    Args:
        user: 用户对象

    Returns:
        强化成功率

    TODO:
        以后完善
    """
    return random.randint(75, 100)


def select_merge_elements(user, element_ids):
    """筛选出用户装备背包中做为材料装备

    材料优先最低等级，不能使用中

    Args:
        user: 用户对象
        element_ids: 材料配置id们

    Returns:
        若条件满足返回材料id们, 否则返回空
    """
    equips = user.hero.equips
    used_equip = get_used_equip(user)

    elements_tree = set(element_ids)
    sorted_data = defaultdict(list)
    limits = defaultdict(int)

    for cfg_id in element_ids:
        limits[cfg_id] += 1

    filter_func = lambda (x, y): (x not in used_equip and \
                  y['cfg_id'] in elements_tree)

    get_element = lambda x: x[1]

    for equip_id, obj in itertools.ifilter(filter_func, equips.iteritems()):
        bisect.insort_left(sorted_data[obj['cfg_id']], (obj['level'], equip_id))

    elements = []

    for cfg_id, sort_list in sorted_data.iteritems():
        limit = limits[cfg_id]
        sort_ids = itertools.imap(get_element, sort_list[:limit])
        elements.extend(sort_ids)

    if len(elements) == len(element_ids):
        return elements


def calc_merge_rebate(user, elements):
    """计算装备合成时材料们强化消耗的金钱

    Args:
        objs: 材料对象们

    Returns:
        返还的钱
    """
    equips = user.hero.equips

    return sum(equips[equip_id]['gold'] for equip_id in elements)


def resolve_loot(user, loot):
    """分解后掉落的材料，放在材料背包中

    Args:
        user: 用户对象
        loot: 掉落配置

    Returns:
        获得的材料数据
    """
    game_config = user.env.game_config
    material = game_config['material']
    equip_material = game_config['equip_material']
    gain_data = defaultdict(int)
    gain = []

    for idx, data in loot.iteritems():
        goods_type, goods = rand_weight(**data)

        if goods_type == 'material':
            star, sort, max_num = goods
            cfg_id = random.choice(material[star][sort])
            num = random.randint(1, max_num)

            gain_data[cfg_id] += num

    for cfg_id, num in gain_data.iteritems():
        detail = equip_material[cfg_id]

        gain.append({
            'cfg_id': cfg_id,
            'num': num,
            'name': detail['name'],
            'icon': detail['icon'],
            })

        incr_material(user, cfg_id, num)

    return gain


def incr_material(user, cfg_id, num, modify=False):
    """修改装备材料数量，有则改， 没则加

    Args:
        user: 用户对象
        cfg_id: 材料配置id
        num: 数量
        modify: 是否为修改
    """
    materials = user.hero.materials

    if cfg_id not in materials:
        materials.add(cfg_id, num=num)
        return

    if modify:
        new_num = num
    else:
        new_num = materials[cfg_id]['num'] + num

    if new_num > 0:
        materials.modify(cfg_id, num=new_num)
    else:
        materials.remove(cfg_id)


def get_st_data(user):
    """获取装备强化时间

    Args:
        user: 用户对象

    Returns:
        强化时间数据
    """
    st_cd = user.hero.data['st_cd']
    st_at = user.hero.data['st_at']

    return {
        'st_cd': st_cd,
        'st_at': st_at,
        'st_delta': logics.calc_delta_second(st_at, st_cd),
    }


def set_st_data(user, cd=1):
    """设置装备强化时间

    Args:
        user: 用户对象
        cd: cd次数
    """
    new_cd = user.hero.data['st_cd'] + cd

    user.hero.data['st_at'] = int(time.time())
    user.hero.data['st_cd'] = min(new_cd, constants.EQUIP_ST_CD_MAX_MINUTE)


def equip_check(user):
    """检查用户装备数值是否有变动

    当配置数据更改后,装备对应的数值当发生改变

    Args:
        user: 用户对象

    Returns:
        是否有改变
    """
    hero_equips = user.hero.equips
    game_config = user.env.game_config
    need_save = False
    cache = {}

    for obj_id, obj in hero_equips.iteritems():
        sign = cache.setdefault(obj['cfg_id'], logics.equip_sign(obj, game_config))

        if obj['sign'] != sign:
            obj_new = logics.equip_reborn(obj, game_config)

            hero_equips.modify(obj_id, **obj_new)
            need_save = True

    return need_save


