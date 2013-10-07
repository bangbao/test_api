# coding: utf-8


def team_equip(env):
    """查看阵容装备

    Returns:
        背包
    """
    user = env.user
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')
    equip_app = env.import_app('equip')
    destiny_app = env.import_app('destiny')

    equip_app.equip_check(user)
    team = hero_app.team_get(user)
    heros = hero_app.format_heros(user, team)

    formation = [heros.get(hero_id) for hero_id in team]
    destiny_app.add_destiny_effect(user, formation)

    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'team': team,
        'heros': heros,
        'team_equip': equip_app.get_team_equip(user),
        'equips': equip_app.format_equips(user, user.hero.equips.iterkeys()),
    }


def load_equip(env):
    """编队位置装载装备

    Args:
        data: 新的编队位置装备

    Returns:
        同team_equip接口
    """
    user = env.user
    data = env.params['data']
    game_config = env.game_config
    equip_app = env.import_app('equip')
    logics = equip_app.logics
    constants = equip_app.constants
    equips = user.hero.equips
    used_equip = set()

    for pos, equip_ids in data.iteritems():
        pos_equip = {}

        for equip_id in equip_ids:
            detail = logics.get_equip_detail(equips[equip_id], game_config)
            where = constants.EQUIP_SORT_WHERES[detail['sort']]

            if equip_id not in used_equip:
                pos_equip[where] = equip_id
                used_equip.add(equip_id)

        equip_app.set_pos_equip(user, pos, pos_equip)

    env.user.save_all()

    return team_equip(env)


def pre_strengthen_equip(env):
    """强化装备页面
    """
    user = env.user
    game_config = env.game_config
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')
    equip_app = env.import_app('equip')
    team = hero_app.team_get(user)

    return {
        'game': game_app.get_game_data(user),
        'team': team,
        'heros': hero_app.format_heros(user, team),
        'team_equip': equip_app.get_team_equip(user),
        'equips': equip_app.format_equips(user, user.hero.equips.iterkeys()),
        'success_ratio': equip_app.get_equip_ratio(env),
        'st_data': equip_app.get_st_data(user),
        'configs': {
            'equip_incr': equip_app.get_equip_incr(user, game_config),
            'equip': game_config['equip'],
            'equip_ability_map': equip_app.constants.EQUIP_ABILITY_DATA,
            }
        }


def strengthen_equip(env):
    """强化装备

    Args:
        equip_id: 装备ID

    Returns:
        同pre_strengthen_equip接口
    """
    user = env.user
    game_config = env.game_config
    equip_id = env.params['equip_id']
    game_app = env.import_app('game')
    equip_app = env.import_app('equip')
    logics = equip_app.logics
    user_hero = user.hero
    equip_config = game_config['equip']

    obj = user_hero.equips[equip_id]
    detail = logics.get_equip_detail(obj, game_config)

    cost_gold = equip_config[obj['level']]['detail'][detail['star']]['need']

    new_obj = logics.equip_upgrade(obj, game_config)
    new_obj['gold'] += cost_gold

    equip_app.set_st_data(user, cd=1)
    game_app.incr_user_attr(user, gold= -cost_gold)
    user_hero.equips.modify(equip_id, **new_obj)

    env.user.save_all()

    return pre_strengthen_equip(env)


def pre_resolve_equip(env):
    """分解装备页面
    """
    user = env.user
    game_config = env.game_config
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')
    equip_app = env.import_app('equip')

    return {
        'game': game_app.get_game_data(user),
        'team': hero_app.team_get(user),
        'team_equip': equip_app.get_team_equip(user),
        'equips': equip_app.format_equips(user, user.hero.equips.iterkeys()),
        'resolve': env.user.hero.data,
        'configs': {
            'equip': game_config['equip'],
        }
    }


def resolve_equip(env):
    """分解装备

    Args:
        equip_id: 装备ID

    Returns:
        同pre_resolve_equip接口
    """
    auto = env.params['auto']
    equip_id = env.params['equip_id']
    game_config = env.game_config
    equip_app = env.import_app('equip')

    if auto:
        loot = equip_app.auto_resolve_equip(env, game_config)
    else:
        loot = equip_app.only_resolve_equip(env, equip_id, game_config)

    env.user.save_all()

    data = pre_resolve_equip(env)
    data['type'] = 1
    data['loot'] = loot

    return data

