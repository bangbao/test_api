# coding: utf-8

from lib.utils import sys_random as random
from apps.public import logics as publics
from apps.public.generator import salt_generator
from apps import battle as battle_app
from models import Hero

import time
import bisect
import itertools
import logics
import constants


def format_heros(user, hero_ids, filter_func=None):
    """格式化多个卡牌信息

    Args:
        user: 用户对象
        hero_ids: 卡牌id们
        filter_func: 过滤函数

    Returns:
        卡牌信息们
    """
    user_hero = user.hero
    game_config = user.env.game_config
    filter_func = filter_func or publics.lambda_func(default=True)
    heros = {}
    configs = {}

    for hero_id in itertools.ifilter(None, hero_ids):
        obj = user_hero.heros[hero_id]

        if filter_func(obj):
            #heros[hero_id] = obj
            #configs[obj['cfg_id']] = logics.filter_hero_info(obj, game_config)
            heros[hero_id] = obj #logics.hero_info(obj, game_config, hero_id=hero_id)

    return heros, configs


def hero2formation(user, hero_ids):
    """根据用户的阵容id队列, 生成相对应的战斗时的队列

    Args:
        user: 用户对象
        hero_ids: 用户阵容

    Returns:
        战斗队列
    """
    formations = [[], []]
    SEQ_GROUP = constants.HERO_TEAM_SEQ_GROUP

    fighter_list = heros2fighters(user, hero_ids)

    for idx, obj in enumerate(fighter_list):
        agent = None
        if obj:
            agent = battle_app.create_agent(obj['job'], **obj)

        group = bisect.bisect_left(SEQ_GROUP, idx)
        formations[group].append(agent)

    return formations


def monster2formation(env, monster_ids):
    """根据怪物id队列, 生成相对应的战斗时的队列

    Args:
        env: 运行环境
        monster_ids: 怪物id队列

    Returns:
        战斗队列
    """
    game_config = env.game_config
    formations = [[], []]
    SEQ_GROUP = constants.HERO_TEAM_SEQ_GROUP

    for idx, monster_id in enumerate(monster_ids):
        agent = None

        if monster_id:
            obj = logics.monster2fighter(monster_id, game_config)
            agent = battle_app.create_agent(obj['job'], **obj)

        group = bisect.bisect_left(SEQ_GROUP, idx)
        formations[group].append(agent)

    return formations


def hero_lined_up(user, hero_ids):
    """根据用户的阵容id队列, 生成相对应的战斗时的队列

    Args:
        user: 用户对象
        hero_ids: 用户阵容

    Returns:
        战斗队列
    """
    game_config = user.env.game_config
    fighter_list = heros2fighters(user, hero_ids)
    obj_list = []

    for hero_id, fighter in itertools.izip(hero_ids, fighter_list):
        obj = None
        if fighter:
            obj = logics.format_hero(fighter, game_config, hero_id=hero_id)

        obj_list.append(obj)

    return obj_list


def monster_lined_up(env, monster_ids):
    """根据怪物id队列, 生成相对应的战斗前显示的数据列表

    Args:
        env: 运行环境
        monster_ids: 怪物id队列

    Returns:
        战斗队列
    """
    game_config = env.game_config
    obj_list = []

    for monster_id in monster_ids:
        obj = None

        if monster_id:
            obj = logics.format_monster(monster_id, game_config)

        obj_list.append(obj)

    return obj_list


def team_put(user, team):
    """保存编队

    Args:
        user: 用户对象
        team: 要保存的编队
    """
    team = logics.rectify_team(team)

    user.game.user['team'] = publics.delimiter_str(team)


def birth_hero(user, hero_cfg_id, where=0, ext=0, **kwargs):
    """生成一个卡牌对象添加到用户数据中

    Args:
        user: 用户对象
        hero_cfg_id: 卡牌配置id
        where: 卡牌来源
        ext: 卡牌扩展标识
        kwargs: 动态卡牌参数

    Returns:
        卡牌hero_id 和 卡牌数据
    """
    game_config = user.env.game_config

    hero = logics.hero_birth(hero_cfg_id, game_config, **kwargs)

    return add_hero(user, hero, where, ext)


def add_hero(user, hero, where=0, ext=0):
    """添加一个新卡牌对象并保存到用户数据中

    Args:
        user: 用户对象
        hero: 卡牌数据对象
        where: 卡牌来源
        ext: 卡牌扩展标识
    """
    hero_id = '%s_%d_%d_%s_%d_%s' % (user.pk,
                                     int(time.time()),
                                     hero['cfg_id'],
                                     salt_generator(),
                                     where,
                                     ext)

    user.hero.heros.add(hero_id, **hero)

    return {
        'hero_id': hero_id,
        'hero': hero,
    }


def get_merge_type(user):
    """获取用户合并的成功类型

    Args:
        user: 用户对象

    Returns:
        成功类型的标志
        0 普通     经验值正常
        1 大成功   经验值*1.3
        2 超成功   经验值*1.5
    """
    acciden_limit = constants.HERO_MERGE_ACCIDENT_LIMIT

    merge_type = constants.HERO_MERGE_TYPE_NORMAL
    rand = random.randint(*constants.HERO_MERGE_ACCIDENT)

    if rand < acciden_limit:
        if rand < (acciden_limit * constants.HERO_MERGE_BIG_WEIGHT):
            merge_type = constants.HERO_MERGE_TYPE_BIG
        else:
            merge_type = constants.HERO_MERGE_TYPE_SUPER

    return merge_type


def team_get(user):
    """获取游戏编队

    Args:
        user: 用户对象

    Returns:
        编队列表
    """
    team = publics.delimiter_list(user.game.user['team'])

    return logics.rectify_team(team)


def del_heros(user, hero_ids):
    """删除多个卡牌

    删除卡牌， 若卡牌在编队中，则同步处理

    Args:
        user: 用户对象
        hero_ids: 要删除的卡牌id们
    """
    team = team_get(user)
    team_set = set(team)

    for hero_id in hero_ids:
        user.hero.heros.remove(hero_id)
        team_set.discard(hero_id)

    for i, hero_id in enumerate(team):
        if hero_id not in team_set:
            team[i] = None

    team_put(user, team)


def summon_hero(env):
    """ 召唤英雄小弟

    当战斗中有英雄使用召唤类技能时，会根据指定的配置生成小弟

    Args:
       env: 运行环境
    """
    game_config = env.game_config

    def wrapper(hero_id, level):
        """ 生成一个指定的卡牌数据

        Args:
           hero_id: 卡牌id
           level: 卡牌等级

        Returns:
           卡牌对象
        """
        obj = logics.hero_birth(hero_id, game_config, level=level)
        fighter = logics.hero2fighter(obj, game_config)

        return battle_app.create_agent(fighter['job'], **fighter)

    return wrapper


def heros2fighters(user, hero_ids):
    """统一编队转换为战斗对象

    Args:
        user: 用户对象
        hero_ids: 编队

    Returns:
        战斗对象们
    """
    equip_app = user.env.import_app('equip')
    goblin_app = user.env.import_app('goblin')
    destiny_app = user.env.import_app('destiny')
    pet_app = user.env.import_app('pet')
    game_config = user.env.game_config
    heros = user.hero.heros

    formation = [logics.hero2fighter(heros.get(hero_id), game_config)
                 for hero_id in hero_ids]

    apply_job_effect(user, formation)
    equip_app.apply_equip_effect(user, formation)
    destiny_app.apply_destiny_effect(user, formation)
    goblin_app.apply_goblin_effect(user, formation)
    pet_app.apply_pet_effect(user, formation)

    return formation


def apply_job_effect(user, formation):
    """应用卡牌职业效果

    Args:
        user: 用户对象
        formation: 卡牌编队们
    """
    game_config = user.env.game_config
    job_config = game_config['class_sort']

    for obj in itertools.ifilter(None, formation):
        detail = logics.get_hero_detail(obj, game_config)
        config = job_config.get(obj['job'])

        if config and obj['job'] != detail['job']:
            logics.apply_job_effect(obj, config)


def del_items(user, item_ids):
    """批量删除转职材料

    Args:
        user: 用户对象
        item_ids: 材料id们
    """
    counts = publics.count(item_ids)

    for item_id, num in counts.iteritems():
        incr_item(user, item_id, -num)


def incr_item(user, item_id, num, modify=False):
    """修改卡牌转职材料数量，有则改， 没则加

    Args:
        user: 用户对象
        item_id: 材料配置id
        num: 数量
        modify: 是否为修改
    """
    items = user.hero.items

    if item_id not in items:
        items.add(item_id, num=num)
        return

    if modify:
        new_num = num
    else:
        new_num = items[item_id]['num'] + num

    if new_num > 0:
        items.modify(item_id, num=new_num)
    else:
        items.remove(item_id)


def hero_check(user):
    """检查用户卡牌数值是否有变动

    当配置数据更改后,卡牌对应的数值当发生改变

    Args:
        user: 用户对象

    Returns:
        是否有更新
    """
    heros = user.hero.heros
    game_config = user.env.game_config
    need_save = False
    cache = {}

    for obj_id, obj in heros.iteritems():
        sign = cache.setdefault(obj['cfg_id'], logics.hero_sign(obj, game_config))

        if obj['sign'] != sign:
            obj_new = logics.hero_reborn(obj, game_config)

            heros.modify(obj_id, **obj_new)
            need_save = True

    return need_save


def pre_use_hero(env):
    """加载该模块时需要预先处理一部分数据
    """
    goblin_app = env.import_app('goblin')
    user_hero = env.user.hero
    today = time.strftime('%Y-%m-%d')

    if user_hero.data['last_date'] != today:
        user_hero.data['last_date'] = today
        user_hero.data['resolve'] = constants.HERO_RESOLVE_DAILY_TOP
        user_hero.data['forge'] = 0

        goblin_app.master_reset(env.user, today)

