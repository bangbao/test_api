# coding: utf-8

from apps import notify as notify_app
from apps.notify import constants as notices


@notify_app.checker
def index(env):
    """地精科技页面
    """
    env.user.load_all()


@notify_app.checker
def master_up(env):
    """地精科技工匠点亮升级
    """
    master = int(env.req.get_argument('master'))

    user = env.user
    game_config = env.game_config
    env.user.load_all()

    game_app = env.import_app('game')
    goblin_app = env.import_app('goblin')
    expense = game_app.calc_expense_cost(user)
    master_up_key = game_app.constants.USER_EXPENSE_MASTER_UP

    if user.game.user['kcoin'] < expense[master_up_key]:
        return notices.KCOIN_NOT_ENOUGH

    masters = goblin_app.masters_get(env.user)
    max_level = max(game_config['goblin_master'])

    if masters[master] >= max_level:
        return notices.GOBLIN_MASTER_IS_MAX_LEVEL

    env.params['master'] = master


@notify_app.checker
def forge(env):
    """地精科技锻造
    """
    mode = int(env.req.get_argument('mode'))

    env.user.load_all()

    user = env.user

    goblin_app = env.import_app('goblin')
    constants = goblin_app.constants
    cost_effect = constants.GOBLIN_FORGE_MODES[mode]

    if user.game.user['gold'] < cost_effect['gold']:
        return notices.GOLD_NOT_ENOUGH

    if user.game.user['kcoin'] < cost_effect['kcoin']:
        return notices.KCOIN_NOT_ENOUGH

    if user.hero.data['forge'] >= goblin_app.get_forge_daily_top(user):
        return notices.GOBLIN_FORGE_ENOUGH_TIMES

    env.params['mode'] = mode


@notify_app.checker
def merge_index(env):
    """零件合成页面
    """
    user = env.user
    user.hero.load_goblins()
    user.load_all()


@notify_app.checker
def merge(env):
    """零件合成
    """
    goblin_id = env.req.get_argument('goblin_id')
    elements = env.req.get_arguments('elements')

    user = env.user
    user_hero = user.hero
    user.hero.load_goblins()
    user.load_all()

    game_config = env.game_config
    goblin_app = env.import_app('goblin')
    goblin_logics = goblin_app.logics
    used_goblin = goblin_app.get_used_goblin(user)

    dst = user_hero.goblins.get(goblin_id)

    if not dst:
        return notices.GOBLIN_NOT_EXISTS

    detail = goblin_logics.get_goblin_detail(dst, game_config)
    level, exp_type = dst['level'], detail['exp_type']
    base = game_config['goblin'][level]['detail'][exp_type]

    if not exp_type or not base['need']:
        return notices.GOBLIN_CAN_NOT_EATEN

    if dst['level'] >= max(game_config['goblin']):
        return notices.GOBLIN_IS_MAX_LEVEL

    if goblin_id in elements:
        return notices.GOBLIN_CAN_NOT_EATEN

    for element_id in elements:
        if element_id in used_goblin:
            return notices.GOBLIN_IS_USED

        obj = user_hero.goblins.get(element_id)

        if not obj:
            return notices.GOBLIN_NOT_EXISTS

        detail = goblin_logics.get_goblin_detail(obj, game_config)

        if not detail['exp_type']:
            return notices.GOBLIN_CAN_NOT_EATEN

    cost_gold = goblin_logics.calc_merge_cost(dst, elements, game_config)

    if user.game.user['gold'] < cost_gold:
        return notices.GOLD_NOT_ENOUGH

    env.params['goblin_id'] = goblin_id
    env.params['elements'] = elements


