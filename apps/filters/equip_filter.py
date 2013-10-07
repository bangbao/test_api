# coding: utf-8

from apps import notify as notify_app
from apps.notify import constants as notices
from apps.public import logics as publics


def team_equip(env):
    """查看编队装备
    """
    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(env.user)

    user.hero.load_equips()
    user.hero.load_heros(keys=team)
    user.load_all()


def load_equip(env):
    """编队位置装载装备
    """
    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(env.user)

    user_hero = user.hero
    user_hero.load_equips()
    user_hero.load_heros(keys=team)
    user.load_all()

    return check_load_equip(env)


def pre_strengthen_equip(env):
    """强化装备前页面
    """
    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(env.user)

    user_hero = user.hero
    user_hero.load_equips()
    user_hero.load_heros(keys=team)
    user.load_all()


def strengthen_equip(env):
    """强化装备
    """
    equip_id = env.req.get_argument('equip_id')

    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(env.user)

    user_hero = user.hero
    user_hero.load_equips()
    user_hero.load_heros(keys=team)
    user.load_all()

    env.params['equip_id'] = equip_id

    return check_strengthen_equip(env, equip_id, env.game_config)


def pre_resolve_equip(env):
    """分解装备前页面
    """
    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(user)

    user_hero = user.hero
    user_hero.load_equips()
    user_hero.load_heros(keys=team)
    user_hero.load_materials()
    user.load_all()


def resolve_equip(env):
    """分解装备
    """
    equip_id = env.req.get_argument('equip_id', '')
    auto = env.req.get_argument('auto', '')

    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(user)

    user_hero = user.hero
    user_hero.load_equips()
    user_hero.load_heros(keys=team)
    user_hero.load_materials()
    user.load_all()

    env.params['equip_id'] = equip_id
    env.params['auto'] = auto

    return check_resolve_equip(env, equip_id, env.game_config, auto)


def pre_merge_equip(env):
    """合成装备前页面
    """
    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(env.user)

    user_hero = user.hero
    user_hero.load_equips()
    user_hero.load_heros(keys=team)
    user.load_all()


def merge_equip(env):
    """合成装备
    """
    cfg_id = int(env.req.get_argument('cfg_id'))

    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(env.user)

    user_hero = user.hero
    user_hero.load_equips()
    user_hero.load_heros(keys=team)
    user.load_all()

    env.params['cfg_id'] = cfg_id

    return check_merge_equip(env, cfg_id, env.game_config)


def sell_equip(env):
    """装备卖出
    """
    elements = set(env.req.get_arguments('elements'))

    user = env.user
    user.game.load_equip()
    user.game.load(env)

    hero_app = env.import_app('hero')
    team = hero_app.team_get(env.user)

    user_hero = user.hero
    user_hero.load_equips()
    user_hero.load_heros(keys=team)
    user.load_all()

    env.params['elements'] = elements

    return check_sell_equip(env, elements, env.game_config)


def clear_equip(env):
    """清空装备cd时间
    """
    env.user.load_all()


def ratio_equip(env):
    """改变装备强化成功率
    """
    env.user.load_all()


@notify_app.checker
def check_load_equip(env):
    """检查装载装备
    """
    equips_set = set(env.user.hero.equips)
    equip_app = env.import_app('equip')

    data = {}
    for pos in equip_app.constants.EQUIP_TEAM_POS_KEYS:
        pos_set = set(env.req.get_arguments(pos))

        if not pos_set.issubset(equips_set):
            return notices.EQUIP_NOT_EXISTS

        data[pos] = pos_set

    env.params['data'] = data


@notify_app.checker
def check_strengthen_equip(env, equip_id, game_config):
    """检查装备是否可以强化
    """
    user_game = env.user.game
    user_hero = env.user.hero
    equip_app = env.import_app('equip')

    obj = user_hero.equips.get(equip_id)

    if not obj:
        return notices.EQUIP_NOT_EXISTS

    if obj['level'] >= user_game.user['level']:
        return notices.EQUIP_ST_MAX_LEVEL

    if user_hero.data['st_cd'] >= equip_app.constants.EQUIP_ST_CD_MAX_MINUTE:
        return notices.EQUIP_ST_IN_CD_TIME

    detail = equip_app.logics.get_equip_detail(obj, game_config)
    config = game_config['equip'][obj['level']]['detail']

    if user_game.user['gold'] < config[detail['star']]['need']:
        return notices.GOLD_NOT_ENOUGH


@notify_app.checker
def check_merge_equip(env, cfg_id, game_config):
    """检查合成装备
    """
    user_game = env.user.game
    equip_app = env.import_app('equip')

    quality = game_config['equip_quality'].get(cfg_id)

    if not quality:
        return notices.EQUIP_NOT_EXISTS

    if user_game.user['gold'] < quality['cost']['gold']:
        return notices.GOLD_NOT_ENOUGH

    elements = equip_app.select_merge_elements(env.user, quality['src'])

    if not elements:
        return notices.EQUIP_ELEMENTS_NOT_ENOUGH

    env.params['elements'] = elements


@notify_app.checker
def check_sell_equip(env, elements):
    """检查装备售卖
    """
    can_sells = []
    user_hero = env.user.hero
    equip_app = env.import_app('equip')
    used_equips = equip_app.get_used_equip(env.user)

    for element in elements:
        if element in used_equips:
            continue

        obj = user_hero.equips.get(element)
        if not obj:
            continue

        can_sells.append(element)

    if not can_sells:
        return notices.EQUIP_NOT_EXISTS

    env.params['elements'] = can_sells


@notify_app.checker
def check_resolve_equip(env, equip_id, game_config, auto):
    """检查分解装备
    """
    user = env.user

    if auto:
        return

    equip_app = env.import_app('equip')

    obj = user.hero.equips.get(equip_id)

    if not obj:
        return notices.EQUIP_NOT_EXISTS

    used_equips = equip_app.get_used_equip(user)

    if equip_id in used_equips:
        return notices.EQUIP_RESOLVE_IN_TEAM

