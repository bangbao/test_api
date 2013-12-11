# coding: utf-8

import itertools

from apps import notify as notify_app
from apps.notify import constants as notices
from apps.public import logics as publics


@notify_app.checker
def heros(env):
    """卡牌背包
    """
    user = env.user
    user.hero.load_heros()
    user.load_all()


@notify_app.checker
def team_arrange(env):
    """阵容编队
    """
    members = env.req.get_arguments('members')

    user = env.user
    user.game.load(env)

    hero_app = env.import_app('hero')
    members = hero_app.logics.rectify_team(members)
    team = hero_app.team_get(env.user)

    user_hero = user.hero
    user_hero.load_heros(keys=set(members + team))
    user.load_all()

    member_not_exists = False

    for member in itertools.ifilter(None, members):
        if member not in user_hero.heros:
            member_not_exists = True
            break

    if any(members) and not member_not_exists:
        env.params['members'] = members
    else:
        env.params['members'] = team

    env.params['user_team'] = team


@notify_app.checker
def pre_evolution(env):
    """卡牌进阶界面
    """
    hero_id = env.req.get_argument('hero_id', '')

    user = env.user
    user.hero.load_heros()
    user.load_all()

    env.params['hero_id'] = hero_id


@notify_app.checker
def evolution(env):
    """卡牌进阶
    """
    hero_id = env.req.get_argument('hero_id')
    elements = set(env.req.get_arguments('elements'))

    user = env.user
    user.hero.load_heros()
    user.load_all()

    user_game = user.game
    user_hero = user.hero
    game_config = env.game_config

    hero_app = env.import_app('hero')
    team = hero_app.team_get(user)
    hero = user_hero.heros.get(hero_id)

    if not hero:
        return notices.HERO_NOT_EXISTS

    detail = game_config['heros'][hero['cfg_id']]
    config = game_config['hero_evolution'].get(hero['cfg_id'])

    if not config:
        return notices.HERO_CAN_NOT_EVOLUTION

    if hero['level'] < detail['max_level']:
        return notices.HERO_NOT_MAX_LEVEL

    if user_game.user['gold'] < config['cost']['gold']:
        return notices.GOLD_NOT_ENOUGH

    src_elements = list(config['src'])

    for element_id in elements:
        if element_id in team:
            return notices.HERO_MERGE_IN_TEAM

        obj = user_hero.heros.get(element_id)

        if not obj:
            return notices.HERO_NOT_EXISTS

        if obj['lock']:
            return notices.HERO_MERGE_IS_LOCKING

        try:
            src_elements.remove(obj['cfg_id'])
        except ValueError:
            return notices.HERO_ELEMENTS_NOT_ENOUGH

    if src_elements:
        return notices.HERO_ELEMENTS_NOT_ENOUGH

    env.params['hero_id'] = hero_id
    env.params['elements'] = elements


@notify_app.checker
def pre_merge(env):
    """卡牌合并前信息
    """
    hero_id = env.req.get_argument('hero_id', '')

    user = env.user
    user.hero.load_heros()
    user.load_all()

    env.params['hero_id'] = hero_id


@notify_app.checker
def merge(env):
    """卡牌合并
    """
    hero_id = env.req.get_argument('hero_id')
    elements = set(env.req.get_arguments('elements'))

    user = env.user
    user.hero.load_heros()
    user.load_all()

    user_game = user.game
    user_hero = user.hero
    game_config = env.game_config
    hero_app = env.import_app('hero')
    team = hero_app.team_get(env.user)
    hero = user_hero.heros.get(hero_id)

    if not hero:
        return notices.HERO_NOT_EXISTS

    detail = game_config['heros'][hero['cfg_id']]

    if hero['level'] >= detail['max_level']:
        return notices.HERO_IS_MAX_LEVEL

    if hero_id in elements:
        return notices.HERO_CAN_NOT_EATEN_SELL

    for element_id in elements:
        if element_id in team:
            return notices.HERO_MERGE_IN_TEAM

        obj = user_hero.heros.get(element_id)

        if not obj:
            return notices.HERO_NOT_EXISTS

        if obj['lock']:
            return notices.HERO_MERGE_IS_LOCKING

        detail = hero_app.logics.get_hero_detail(obj, game_config)

        if not detail['can_eaten']:
            return notices.HERO_CAN_NOT_EATEN_SELL

    if user_game.user['gold'] < hero_app.logics.calc_merge_cost(hero, elements):
        return notices.GOLD_NOT_ENOUGH


    env.params['hero_id'] = hero_id
    env.params['elements'] = elements


@notify_app.checker
def pre_resolve(env):
    """卡牌分解界面
    """
    user = env.user
    user.hero.load_heros()
    user.load_all()


@notify_app.checker
def resolve(env):
    """卡牌分解
    """
    hero_id = env.req.get_argument('hero_id')

    user = env.user
    user.hero.load_heros()
    user.load_all()


    hero_app = env.import_app('hero')
    team = hero_app.team_get(user)

    if hero_id in team:
        return notices.HERO_RESOLVE_IN_TEAM

    hero = user.hero.heros.get(hero_id)

    if not hero:
        return notices.HERO_NOT_EXISTS

    if hero['lock']:
        return notices.HERO_RESOLVE_IS_LOCKING

    if user.hero.data['resolve'] <= 0:
        return notices.HERO_RESOLVE_NO_FREE_TIMES

    env.params['hero_id'] = hero_id


@notify_app.checker
def sell(env):
    """卡牌卖出
    """
    elements = set(env.req.get_arguments('elements'))

    user = env.user
    user.hero.load_heros()
    user.load_all()

    user_hero = user.hero
    game_config = env.game_config

    hero_app = env.import_app('hero')
    team = hero_app.team_get(user)

    can_sells = []
    include_not_sell = False

    for element in elements:

        if element in team:
            continue

        obj = user_hero.heros.get(element)

        if not obj or obj['lock']:
            continue

        detail = hero_app.logics.get_hero_detail(obj, game_config)
 
        if not detail['can_sell']:
            include_not_sell = True
            continue

        can_sells.append(element)

    if not can_sells:
        if include_not_sell:
            return notices.HERO_CAN_NOT_EATEN_SELL

        return notices.HERO_NOT_EXISTS

    env.params['elements'] = can_sells


@notify_app.checker
def pre_trans_job(env):
    """转职页面
    """
    user = env.user
    user.hero.load_heros()
    user.hero.load_items()
    user.load_all()


@notify_app.checker
def trans_job(env):
    """转职
    """
    hero_id = env.req.get_argument('hero_id')
    game_config = env.game_config

    user = env.user
    user.hero.load_heros()
    user.hero.load_items()
    user.load_all()

    user_game = user.game
    user_hero = user.hero

    obj = user_hero.heros.get(hero_id)

    if not obj:
        return notices.HERO_NOT_EXISTS

    config = game_config['class_evolution'].get(obj['job'])

    if not config:
        return notices.HERO_JOB_CAN_NOT_EVOLUTION

    counts = publics.count(config['src'])

    for item_id, num in counts.iteritems():
        data = user_hero.items.get(item_id)

        if not data or data['num'] < num:
            return notices.HERO_JOB_ELEMENTS_NOT_ENOUGH

    if user_game.user['gold'] < config['cost']['gold']:
        return notices.GOLD_NOT_ENOUGH

    env.params['hero_id'] = hero_id


@notify_app.checker
def buy_items(env):
    """购买转职材料
    """
    item_id = int(env.req.get_argument('item_id', 0))
    num = int(env.req.get_argument('num', 1))

    user = env.user
    user.hero.load_heros()
    user.hero.load_items()
    user.load_all()

    # TODO check kcoin
    env.params['item_id'] = item_id
    env.params['num'] = num


