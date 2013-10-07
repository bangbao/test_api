# coding: utf-8

from apps import battle as battle_app

import itertools


def index(env):
    """进入竞技场首页
    """
    user = env.user
    game_app = env.import_app('game')
    arena_app = env.import_app('arena')

    arena_app.get_or_init_arena(user)
    incr = arena_app.get_per_award(user)

    user.save_all()

    return {
        'game': game_app.get_game_data(user),
        'arena': arena_app.get_arena_data(user),
        'rank_award': arena_app.format_rank_award(user),
        'incr': incr,
    }


def rank(env):
    """排行榜
    """
    user = env.user
    arena_app = env.import_app('arena')
    constants = arena_app.constants
    arena = arena_app.get_or_init_arena(user)

    ranks = arena.zrevrange(constants.DEFAULT_START_RANK,
                            constants.DEFAULT_END_RANK)
    uids = itertools.imap(int, ranks)

    user.save_all()

    return {
        'users': arena_app.get_users_info(env, uids),
        'arena': arena_app.get_arena_data(user),
    }


def rival(env):
    """查看竞技场对手
    """
    user = env.user
    refresh = env.params['refresh']
    arena_app = env.import_app('arena')
    rival_users = arena_app.get_rival_users(user, refresh=refresh)

    user.save_all()

    return {
        'users': rival_users,
        'arena': arena_app.get_arena_data(user),
    }


def pre_fight(env):
    """对比双方阵容详细
    """
    user = env.user
    hero_app = env.import_app('hero')

    team = hero_app.team_get(user)
    target_user = env.params['target_user']
    target_team = hero_app.team_get(target_user)

    attacker = hero_app.hero_lined_up(user, team)
    defender = hero_app.hero_lined_up(target_user, target_team)

    return {
        'attacker': attacker,
        'defender': defender,
        'map': {
            'icon': '1.png',
            'area': 1,
            'stage': 1,
            'chapter': 1,
            'name': '',
            'loot': {
                'heros': [],
                'exp': 0,
                'gold': 0,
            },
        },
    }


def fight(env):
    """挑战对手
    """
    game_config = env.game_config
    game_app = env.import_app('game')
    hero_app = env.import_app('hero')
    arena_app = env.import_app('arena')

    user = env.user
    team = env.params['members']
    target_user = env.params['target_user']
    target_team = hero_app.team_get(target_user)

    attacker = hero_app.hero2formation(user, team)
    defender = hero_app.hero2formation(target_user, target_team)

    battle_ai = battle_app.battle(env, game_config['map_info'][1], attacker, defender)
    battle_data = battle_ai.record()

    arena_app.arena_over(user, target_user, win=battle_data['fight']['win'])

    hero_app.team_put(user, team)
    user.save_all()
    target_user.save_all()

    return {
        'battle': battle_data,
        'opening': battle_ai.opening,
        'takeabow': battle_ai.takeabow,
        'arena': arena_app.get_arena_data(user),
        'loot': {'exp': 0, 'gold': 0, 'heros': [], 'evaluation': 1},
        'levelup': [],
        'area': 1,
        'stage': 1,
        'chapter': 1,
        'game': game_app.get_game_data(user),
    }


def buy_battle_times(env):
    """购买竞技次数
    """
    user = env.user
    game_app = env.import_app('game')
    arena_app = env.import_app('arena')
    constants = arena_app.constants

    arena_app.incr_arena_attr(user, buy_count=1)
    game_app.incr_user_attr(user, kcoin= -constants.BUY_BATTLE_TIMES_PRICE)

    user.save_all()

    return {
        'arena': arena_app.get_arena_data(user),
        'game': game_app.get_game_data(user),
    }


def clear_battle_delta(env):
    """清空竞技CD时间
    """
    user = env.user
    game_app = env.import_app('game')
    arena_app = env.import_app('arena')
    constants = arena_app.constants

    user.arena.data['battle_at'] = 0
    game_app.incr_user_attr(user, kcoin= -constants.CLEAR_BATTLE_DELTA_PRICE)
    rival_users = arena_app.get_rival_users(user)

    user.save_all()

    return {
        'users': rival_users,
        'arena': arena_app.get_arena_data(user),
        'game': game_app.get_game_data(user),
    }

def get_log(env):
    """获取日志记录
    """
    user = env.user
    arena_app = env.import_app('arena')
    constants = arena_app.constants

    latest_logs = sorted(user.arena.logs.itervalues(), key=lambda x: x['ts'],
                         reverse=True)

    user.save_all()

    return {
        'logs': latest_logs[:constants.ARENA_LOG_RECORD_NUM]
    }


def get_rank_award(env):
    """领取排名奖励
    """
    user = env.user
    arena_app = env.import_app('arena')

    award_config = arena_app.has_rank_award(user)
    loot = {}

    if award_config:
        loot = arena_app.give_award(user, award_config)

    user.save_all()

    return {'rank_award': loot}

