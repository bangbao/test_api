# coding: utf-8

import itertools

from apps import notify as notify_app
from apps.notify import constants as notices


@notify_app.checker
def index(env):
    """进入竞技场首页
    """
    user = env.user
    user.game.load_arena()
    user.load_all()

    arena_app = env.import_app('arena')
    required_level = arena_app.constants.REQUIRED_LEVEL

    if user.game.user['level'] < required_level:
        return notices.ARENA_NOT_ENOUGH_LEVEL


@notify_app.checker
def rank(env):
    """排行榜
    """
    user = env.user
    user.game.load_arena()
    user.load_all()


@notify_app.checker
def rival(env):
    """查看竞技场对手
    """
    refresh = env.req.get_argument('refresh', '')

    user = env.user
    user.game.load_arena()
    user.load_all()

    arena_app = env.import_app('arena')
    refresh_price = arena_app.constants.RIVAL_REFRESH_PRICE

    if refresh and user.game.user['kcoin'] < refresh_price:
        return notices.KCOIN_NOT_ENOUGH

    env.params['refresh'] = refresh


@notify_app.checker
def pre_fight(env):
    """对比双方阵容详细
    """
    target_id = int(env.req.get_argument('target_id'))

    user = env.user
    user.load_fight()
    user.load_all()

    user_app = env.import_app('user')

    target_user = user_app.get_user(env, target_id)
    target_user.load_fight()

    env.params['target_user'] = target_user


@notify_app.checker
def fight(env):
    """挑战对手
    """
    members = env.req.get_arguments('members')
    target_id = int(env.req.get_argument('target_id'))

    user_app = env.import_app('user')
    hero_app = env.import_app('hero')
    members = hero_app.logics.rectify_team(members)

    user = env.user
    user.game.load_arena()
    user.load_fight(members=members)
    user.load_all()

    target_user = user_app.get_user(env, target_id, read_only=True)
    target_user.game.load_arena()
    target_user.load_fight()
    target_user.arena.load_data()
    target_user.arena.load(env)

    arena_app = env.import_app('arena')
    required_level = arena_app.constants.REQUIRED_LEVEL

    if user.game.user['level'] < required_level:
        return notices.ARENA_NOT_ENOUGH_LEVEL

    if arena_app.logics.calc_battle_delta(user.arena.data['battle_at']):
        return notices.ARENA_FIGHT_IN_CD_TIME

    if user.arena.data['battle'] - user.arena.data['buy_count'] >= \
            arena_app.get_battle_top(user):
        return notices.ARENA_TODAY_ENOUGH_BATTLE_TIMES

    member_not_exists = False

    for member in itertools.ifilter(None, members):
        if member not in user.hero.heros:
            member_not_exists = True
            break

    if any(members) and not member_not_exists:
        env.params['members'] = members
    else:
        env.params['members'] = hero_app.team_get(user)

    env.params['target_user'] = target_user


@notify_app.checker
def buy_battle_times(env):
    """购买竞技次数
    """
    user = env.user
    user.load_all()

    arena_app = env.import_app('arena')
    buy_price = arena_app.constants.BUY_BATTLE_TIMES_PRICE

    if user.game.user['kcoin'] < buy_price:
        return notices.KCOIN_NOT_ENOUGH


@notify_app.checker
def clear_battle_delta(env):
    """清空竞技场cd时间
    """
    user = env.user
    user.load_all()

    arena_app = env.import_app('arena')
    buy_price = arena_app.constants.CLEAR_BATTLE_DELTA_PRICE

    if user.game.user['kcoin'] < buy_price:
        return notices.KCOIN_NOT_ENOUGH


@notify_app.checker
def get_rank_award(env):
    """领取排名奖励
    """
    user = env.user
    user.game.load_award()
    user.load_all()

    arena_app = env.import_app('arena')

    if not arena_app.has_rank_award(user):
        return notices.ARENA_AWARD_HAS_BEEN_RECEIVE


@notify_app.checker
def get_log(env):
    """获取日志记录
    """
    user = env.user
    user.arena.load_logs()
    user.load_all()


