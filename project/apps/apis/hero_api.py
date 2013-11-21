# coding: utf-8

from lib.db.expressions import Incr


def heros(env):
    """卡牌背包

    Returns:
        背包信息

    TODO:
        检查函数要放在更合理的地方
    """
    user = env.user
    hero_app = env.import_app('hero')

    hero_app.hero_check(user)
    user.save_all()

    hero_objs, hero_configs = hero_app.format_heros(user, user.hero.heros.iterkeys())

    return {
        'team': hero_app.team_get(user),
        'heros': hero_objs,
        #'heros': hero_app.format_heros(user, user.hero.heros.iterkeys()),
        'configs': {
            'heros': hero_configs,
        }
    }


def team_arrange(env):
    """阵容编队

    Args:
        members: 编队成员

    Returns:
        新的编队
    """
    user = env.user
    new_team = env.params['members']
    hero_app = env.import_app('hero')

    hero_app.team_put(user, new_team)
    user.save_all()

    return {
        'team': new_team,
    }


def pre_evolution(env):
    """卡牌进阶界面

    Args:
      hero_id: 要进阶的卡牌

    Returns:
        界面信息
    """
    user = env.user
    game_config = env.game_config
    hero_id = env.params['hero_id']
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    return {
        'game': game_app.get_game_data(user),
        'hero_id': hero_id,
        'team': hero_app.team_get(user),
        'heros': hero_app.format_heros(user, user.hero.heros.iterkeys()),
        'configs': {
            'hero': game_config['hero'],
            'heros': game_config['heros'],
            'hero_evolution': game_config['hero_evolution'],
        },
    }


def evolution(env):
    """卡牌进阶

    Args:
      hero_id: 要进阶的卡牌
      elements: 要使用的材料卡牌

    Returns:
        界面信息
    """
    user = env.user
    game_config = env.game_config
    hero_id = env.params['hero_id']
    elements = env.params['elements']
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    team = hero_app.team_get(user)
    hero = user.hero.heros[hero_id]
    cost_gold = game_config['hero_evolution'][hero['cfg_id']]['cost']['gold']

    game_app.incr_user_attr(user, gold= -cost_gold)
    hero_app.del_heros(user, itertools.chain((hero_id,), elements))

    obj = hero_app.logics.hero_evolution(hero['cfg_id'], game_config, lock=hero['lock'])

    obj_new = hero_app.add_hero(user, obj,
                                where=hero_app.constants.HERO_FROM_EVOLUTION,
                                ext=hero['cfg_id'])

    if hero_id in team:
        idx = team.index(hero_id)
        team[idx] = obj_new['hero_id']
        hero_app.team_put(user, team)

    user.save_all()

    return pre_evolution(env)


def pre_merge(env):
    """卡牌合并界面

    Args:
       hero_id: 目标卡牌

    Returns:
        界面信息
    """
    user = env.user
    game_config = env.game_config
    hero_id = env.params['hero_id']
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    return {
        'game': game_app.get_game_data(user),
        'hero_id': hero_id,
        'team': hero_app.team_get(user),
        'heros': hero_app.format_heros(user, user.hero.heros.iterkeys()),
        'configs': {
            'hero': game_config['hero'],
            'heros': game_config['heros'],
        },
    }


def merge(env):
    """卡牌合并

    Args:
       hero_id: 目标卡牌
       elements: 材料卡牌们

    Returns:
        合并后的卡牌数据
    """
    user = env.user
    game_config = env.game_config
    hero_id = env.params['hero_id']
    elements = env.params['elements']
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    dst = user.hero.heros[hero_id]
    merges = hero_app.format_heros(user, elements).values()
    merge_type = hero_app.get_merge_type(user)
    cost_gold = hero_app.logics.calc_merge_cost(dst, merges)
    merge_data = hero_app.logics.hero_merge(dst, merges, game_config, merge_type)

    game_app.incr_user_attr(user, gold= -cost_gold)
    user.hero.heros.modify(hero_id, **merge_data['hero'])

    user.save_all()

    return pre_merge(env)


def pre_resolve(env):
    """卡牌分解界面

    Returns:
        界面信息
    """
    user = env.user
    game_config = env.game_config
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    filter_func = lambda obj: obj['star'] > 1
    heros = hero_app.format_heros(user, user.hero.heros.iterkeys(), filter_func=filter_func)

    return {
        'game': game_app.get_game_data(user),
        'resolve': user.hero.data,
        'team': hero_app.team_get(user),
        'heros': heros,
        'configs': {
            'hero': game_config['hero'],
            'hero_resolve': game_config['hero_resolve'],
        },
    }


def resolve(env):
    """卡牌分解

    Args:
       hero_id: 目标卡牌

    Returns:
        界面信息
    """
    user = env.user
    game_config = env.game_config
    hero_id = env.params['hero_id']
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    obj = user.hero.heros[hero_id]
    detail = hero_app.logics.get_hero_detail(obj, game_config)
    level, tp, star = obj['level'], detail['type'], detail['star']
    config = game_config['hero_resolve'][star]
    sell_gold = game_config['hero'][level]['detail'][tp]['sell']

    if user.hero.data['resolve'] >= 1:
        user.hero.data['resolve'] = Incr('resolve', -1,
                                         user.hero.data)
    game_app.incr_user_attr(user, gold=sell_gold)
    game_app.incr_info_attr(user, hero=config['gain']['hero'])
    hero_app.del_heros(user, [hero_id])

    user.save_all()

    return pre_resolve(env)


def sell(env):
    """卡牌卖出

    Args:
        elements: 卡牌hero_id们

    Returns:
        卡牌背包
    """
    user = env.user
    game_config = env.game_config
    elements = env.params['elements']
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    gold = 0
    for element in elements:
        obj = user.hero.heros[element]
        detail = hero_app.logics.get_hero_detail(obj, game_config)
        level, tp = obj['level'], detail['type']

        gold += game_config['hero'][level]['detail'][tp]['sell']

    game_app.incr_user_attr(user, gold=gold)
    hero_app.del_heros(user, elements)

    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'elements': elements,
        'team': hero_app.team_get(user),
        'heros': hero_app.format_heros(user, user.hero.heros.iterkeys()),
        'configs': {
            'hero': game_config['hero'],
        },
    }


def pre_trans_job(env):
    """转职页面
    """
    user = env.user
    game_config = env.game_config
    hero_app = env.import_app('hero')

    filter_func = hero_app.logics.filter_trans_job(game_config)

    return {
        'heros': hero_app.format_heros(user, user.hero.heros.iterkeys(),
                                       filter_func=filter_func),
        'items': user.hero.items,
        'configs': {
            'class_evolution': game_config['class_evolution'],
            'class_sort': game_config['class_sort'],
            'item': game_config['item'],
        },
    }


def trans_job(env):
    """转职
    """
    user = env.user
    game_config = env.game_config
    hero_id = env.params['hero_id']
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')

    obj = user.hero.heros[hero_id]
    config = game_config['class_evolution'][obj['job']]

    user.hero.heros.modify(hero_id, job=config['dest'])
    hero_app.del_items(env.user, config['src'])
    game_app.incr_user_attr(env.user, gold= -config['cost']['gold'])

    env.user.save_all()

    return pre_trans_job(env)


def buy_items(env):
    """购买转职材料

    TODO:
        消耗酷币
    """
    user = env.user
    item_id = env.params['item_id']
    num = env.params['num']
    hero_app = env.import_app('hero')

    hero_app.incr_item(user, item_id, num)

    user.save_all()

    return pre_trans_job(env)

