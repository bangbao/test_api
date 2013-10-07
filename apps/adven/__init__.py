# coding: utf-8

from models import Adven
from test import (world_map_config, chapter_map_config)

import itertools
import logics


def chapter_over(user, chapter, stage, select, win=False, grade=1):
    """关卡结算

    处理关卡的消耗和掉落

    Args:
        user: 用户对象
        chapter: 章节ID
        stage: 关卡ID
        select: 选择的战斗模式light 或者 dark
        win: 战斗结果，胜利为True, 失败为False
        grade: 战斗评级

    Returns:
        角色升级数据 和 掉落数据
    """
    evolutions = []
    loot_data = {'heros': [], 'exp': 0, 'gold': 0, 'evaluation': grade}

    game_config = user.env.game_config
    stage_config = game_config['stages'][stage]

    cost_energy = adven_cost(user, stage_config['cost'])

    if not win:
        return evolutions, loot_data

    base_exp = stage_config['loot']['exp']
    base_gold = stage_config['loot']['gold']
    fight_id = stage_config[select]['fight_id']
    score = stage_config[select]['side']
    monsters = game_config['map_fight'][fight_id]['monster']

    monster_loot = logics.monster_loot(monsters, game_config)
    evolutions, real_loot = adven_loot(user, monster_loot, stage,
                                       gold=base_gold, exp=base_exp)

    loot_data.update(real_loot)

    set_adven_record(user, chapter, stage, cost_energy, grade,
                     **{select: score, 'select': select})

    return evolutions, loot_data

def battle_evaluation(user, win, falls):
    """对战斗进行评级

    Args:
        user: 用户对象
        win: 战斗结果，胜利为True, 失败为False
        falls: 战斗死亡人数

    Returns:
        评级
    """
    return 1

def set_adven_record(user, chapter, stage, energy, grade,
                     light=0, dark=0, select=''):
    """记录用户冒险数据

    Args:
        user: 用户对象
        chapter: 关卡章节
        stage: 关卡id
        energy: 消耗的体力
        grade: 战斗评级
        light: 获得的光明点数
        dark: 获得的黑暗点数
        select: 所选择的阵营
    """

    set_adven_adven(user, chapter, stage)
    set_adven_readven(user, chapter,
                      stage=stage, select=select)
    set_adven_data(user, stage,
                   energy=energy, grade=grade, light=light, dark=dark)

def set_adven_adven(user, chapter, stage):
    """记录用户最高冒险记录

    Args:
        user: 用户对象
        chapter: 章节ID
        stage: 关卡ID
    """
    adven = user.adven.adven

    if chapter > adven['chapter']:
        adven['chapter'] = chapter
        adven['stage'] = stage

    elif chapter == adven['chapter'] and stage > adven['stage']:
        adven['stage'] = stage

def set_adven_readven(user, chapter, **obj):
    """记录用户冒险快照

    Args:
        user: 用户对象
        chapter: 章节ID
        obj: 修改的数据
    """
    readven = user.adven.readven

    if not chapter in readven:
        readven.add(chapter, **obj)
    else:
        readven.modify(chapter, **obj)

def set_adven_data(user, stage, **obj):
    """记录用户每个关卡数据

    Args:
        user: 用户对象
        stage: 关卡ID
        obj: 修改的数据
    """
    data = user.adven.data

    if not stage in data:
        data.add(stage, **obj)
    else:
        data.modify(stage, **obj)

def reset_adven(user, chapter):
    """用户重置章节

    Args:
        user: 用户对象
        chapter: 章节id
    """
    game_app = user.env.import_app('game')
    stages = user.env.game_config['chapter_stage']['chapter_stage'][chapter]

    data = user.adven.data
    light = dark = energy = 0
    filter_func = lambda x: x in data

    for stage in itertools.ifilter(filter_func, stages):
        stage_data = data[stage]
        light += stage_data['light']
        dark += stage_data['dark']
        energy += stage_data['energy']

        data.remove(stage)

    game_app.incr_user_attr(user,
                            light= -light,
                            dark= -dark,
                            energy=energy)

    user.adven.readven.modify(chapter,
                              reset=user.adven.readven[chapter]['reset'] + 1,
                              stage=stages[0],
                              select='')

def get_adven_record(user):
    """获取用户当前最高记录

    Args:
        user: 用户对象

    Returns:
        用户当前最高攻关记录
    """
    stages_config = user.env.game_config['stages']
    adven = user.adven.adven
    stage = adven['stage']

    return {
        'area': 2,
        'chapter': adven['chapter'],
        'stage': stage,
        'stage_name': stages_config.get(stage, {}).get('name')
    }

def adven_loot(user, loot, stage, **kwargs):
    """为用户发放过关奖励

    Args:
        user: 用户对象
        loot: 掉落数据 每个关卡的掉落数据集合
        stage: 关卡id
        kwargs: 动态参数

    Returns:
        升级数据和奖励数据
    """
    env = user.env
    exp = kwargs.get('exp', 0)
    gold = loot['gold'] + kwargs.get('gold', 0)
    evolutions = []

    game_app = env.import_app('game')
    hero_app = env.import_app('hero')
    equip_app = env.import_app('equip')
    game_config = user.env.game_config

    loot_heros = []
    for hero_cfg_id, level in loot['heros']:
        obj = hero_app.birth_hero(user, hero_cfg_id,
                                  where=hero_app.constants.HERO_FROM_STAGE,
                                  ext=stage,
                                  level=level)

        detail = hero_app.logics.format_hero(obj['hero'], game_config)
        loot_heros.append(detail)

    for equip_cfg_id, in loot['equips']:
        obj = equip_app.birth_equip(user, equip_cfg_id,
                                    where=equip_app.constants.EQUIP_FROM_STAGE,
                                    ext=stage)
        detail = equip_app.logics.get_equip_detail(obj['equip'], game_config)
        loot_heros.append(detail)

    game_app.incr_user_attr(user, gold=gold)
    game_app.add_exp(user, exp, evolutions)

    return evolutions, {
        'heros': loot_heros,
        'exp': exp,
        'gold': gold,
    }

def adven_cost(user, cost):
    """攻关时的消耗

    Args:
        user: 用户对象
        cost: 消耗配置
    """
    game_app = user.env.import_app('game')

    cost_energy = cost['energy']

    game_app.incr_user_attr(user, energy= -cost_energy)

    return cost_energy
