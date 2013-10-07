# coding: utf-8


def index(env):
    """地精科技页面
    """
    user = env.user
    game_app = env.import_app('game')
    goblin_app = env.import_app('goblin')

    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'masters': goblin_app.masters_get(user),
        'expense': game_app.calc_expense_cost(user),
        'data': goblin_app.get_goblin_data(user),
    }


def master_up(env):
    """地精科技工匠点亮升级
    """
    user = env.user
    master = env.params['master']
    game_app = env.import_app('game')
    goblin_app = env.import_app('goblin')

    expense = game_app.calc_expense_cost(user)
    master_up_key = game_app.constants.USER_EXPENSE_MASTER_UP

    game_app.incr_user_attr(user, kcoin= -expense[master_up_key])
    goblin_app.incr_goblin_attr(user, master_up=1)
    masters = master_up(user, master)

    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'masters': masters,
        'expense': game_app.calc_expense_cost(user),
    }


def forge(env):
    """地精科技锻造
    """
    user = env.user
    mode = env.params['mode']
    game_app = env.import_app('game')
    goblin_app = env.import_app('goblin')

    constants = goblin_app.constants
    cost_effect = constants.GOBLIN_FORGE_MODES[mode]
    loot_goods = []
    loot_points = {}

    if user.hero.data['forge_cycle'] == constants.GOBLIN_FORGE_DELTA:
        loot_goods = goblin_app.forge_goods(user, cost_effect)
    else:
        loot_points = goblin_app.forge_point(user, cost_effect)

    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'masters': goblin_app.masters_get(user),
        'data': goblin_app.get_goblin_data(user),
        'loot': {
            'goblin': loot_goods,
            'points': loot_points,
        },
    }


def merge_index(env):
    """零件合成页面
    """
    user = env.user
    game_config = env.game_config
    game_app = env.import_app('game')
    goblin_app = env.import_app('goblin')
    filter_func = goblin_app.logics.filter_goblin_merge(game_config)

    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'goblins': goblin_app.format_goblins(user, user.hero.goblins.iterkeys(),
                                             filter_func=filter_func),
        'configs': {
            'goblins': game_config['goblins'],
            'effect_sort_map': goblin_app.constants.GOBLIN_EFFECT_SORT_MAP,
        }
    }


def merge(env):
    """零件合成
    """
    user = env.user
    game_config = env.game_config
    goblin_id = env.params['goblin_id']
    elements = env.params['elements']
    game_app = env.import_app('game')
    goblin_app = env.import_app('goblin')

    dst = user.hero.goblins[goblin_id]
    merges = goblin_app.format_goblins(user, elements).values()
    cost_gold = goblin_app.logics.calc_merge_cost(dst, elements, game_config)
    new_obj = goblin_app.logics.goblin_merge(dst, merges, game_config)

    game_app.incr_user_attr(user, gold= -cost_gold)
    user.hero.goblins.modify(goblin_id, **new_obj)
    goblin_app.del_goblins(user, elements)

    user.save_all()

    return merge_index(env)

