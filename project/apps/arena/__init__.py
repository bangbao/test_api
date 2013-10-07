# coding: utf-8

from cheetahes.utils import rand_weight
from cheetahes.db.expressions import Incr
from apps.public import logics as publics
from apps import config as config_app
from models import Arena

import time
import datetime
import itertools
import logics
import constants


def give_award(user, award):
    """发送排名奖励

    Args:
        user: 用户对象
        award: 奖励配置

    Returns:
        奖励详细
    """
    gold = award['round']['gold']
    score = award['round']['score']
    round_type = award['round_type']
    value = award['value']
    num = award['num']

    game_app = user.env.import_app('game')
    hero_app = user.env.import_app('hero')
    equip_app = user.env.import_app('equip')
    game_config = user.env.game_config

    incr_arena_attr(user, score=score)
    game_app.incr_user_attr(user, gold=gold)
    user.arena.data['award_at'] = time.strftime('%Y-%m-%d %H:%M:%S')

    loot = []
    if round_type == constants.ARENA_AWARD_ROUND_TYPE_HERO:
        goods_id = rand_weight(**value)
        for i in xrange(num):
            hero_app.birth_hero(user, goods_id,
                                where=hero_app.constants.HERO_FROM_ARENA,
                                ext=num)
        detail = game_config['heros'][goods_id]
        loot.append({'name': detail['name'], 'num': num})

    elif round_type == constants.ARENA_AWARD_ROUND_TYPE_EQUIP:
        goods_id = rand_weight(**value)
        for i in xrange(num):
            equip_app.birth_equip(user, goods_id,
                                  where=equip_app.constants.EQUIP_FROM_ARENA,
                                  ext=num)
        detail = game_config['equips'][goods_id]
        loot.append({'name': detail['name'], 'num': num})

    elif round_type == constants.ARENA_AWARD_ROUND_TYPE_ITEM:
        goods_id = rand_weight(**value)
        hero_app.incr_item(user, goods_id, num)
        detail = game_config['item'][goods_id]
        loot.append({'name': detail['name'], 'num': num})

    return {
        'gold': gold,
        'score': score,
        'loot': loot,
    }


def has_rank_award(user):
    """ 判断是否可领取排名奖励

    Args:
        user: 用户对象

    Returns:
        排名奖励
    """
    game_config = user.env.game_config
    award_arena = get_award_arena(user)

    start_time = get_arena_start_time(user.env)
    award_at = user.arena.data['award_at']

    if award_at and \
            datetime.datetime.strptime(award_at, '%Y-%m-%d %H:%M:%S') > start_time:
        return False

    return logics.get_award_detail(award_arena.rank, game_config)

def get_per_award(user):
    """查看时间奖励

    Args:
        user: 用户对象

    Returns:
        时间奖励数据
    """
    game_config = user.env.game_config
    rank = user.arena.data['rank']

    config = logics.get_award_detail(rank, game_config)
    remainder = timed_per_award(user)

    return {
        'score': config['per']['score'],
        'delta': constants.DEFAULT_PER_DELTA_SECONDS - remainder,
    }


def incr_arena_attr(user, **kwargs):
    """修改用户竞技场相关属性值

    Args:
        user: 用户对象
        kwargs: 属性键值对
    """
    field = user.arena.data

    for attr, value in kwargs.iteritems():
        field[attr] = Incr(attr, value, field)


def rivals_get(user):
    """获取固定的对手ID

    Args:
        user: 用户对象

    Returns:
        对手ID们
    """
    rivals_str = user.arena.data['rivals']
    rivals = publics.delimiter_list(rivals_str) if rivals_str else []

    return map(int, rivals)


def rivals_put(user, rivals):
    """保存对手ID

    Args:
        user: 用户对象
        rivals: 对手ID列表
    """
    rivals = itertools.imap(str, rivals)

    user.arena.data['rivals'] = publics.delimiter_str(rivals)


def get_users_info(env, uids):
    """根据用户排名数据返回用户们详细信息

    Args:
        env: 运行环境
        uids: 用户uids

    Returns:
        list
    """
    return [user_rank_info(env, user_id) for user_id in uids]


def get_arena_data(user):
    """获取用户竞技数据
    """
    arena_data = user.arena.data

    return {
        'rank': arena_data['rank'],
        'score': arena_data['score'],
        'battle': arena_data['battle'],
        'battle_top': get_battle_top(user),
        'battle_delta': logics.calc_battle_delta(arena_data['battle_at']),
    }


def get_battle_top(user):
    """获取竞技次数上限

    Args:
        user: 用户对象

    TODO:
        vip功能添加时完善
    """
    return constants.DEFAULT_BATTLE_TIMES


def get_free_refresh(user):
    """获取免费刷新对手次数

    Args:
        user: 用户对象

    TODO:
        vip功能添加时完善
    """
    return constants.DEFAULT_REFRESH_TIMES

def refresh_rival(user, refresh):
    """刷新对手们

    Args:
        user: 用户对象
        refresh: 是否手动刷新

    Returns:
        对手uid们
    """
    uids = rivals_get(user)

    # if not refresh and len(uids) >= constants.DEFAULT_RIVAL_LENGTH:
    if not refresh and uids:
        return uids

    arena = get_or_init_arena(user)
    see_ranks = logics.nearby_rank(user.arena.data['rank'])
    ranks = arena.pick_out(see_ranks)
    uids = map(int, ranks.itervalues())
    rivals_put(user, uids)

    if refresh:
        if user.arena.data['refresh'] >= get_free_refresh(user):
            game_app = user.env.import_app('game')
            game_app.incr_user_attr(user, kcoin= -constants.RIVAL_REFRESH_PRICE)

        incr_arena_attr(user, refresh=1)

    return uids


def get_rival_users(user, refresh=False):
    """获取用户排名周围用户数据

    Args:
        user: 用户对象
        refresh: 是否刷新对手

    Returns:
        用户信息们
    """
    uids = refresh_rival(user, refresh)

    return get_users_info(user.env, uids)


def format_rank_award(user):
    """格式化用户当前排名奖励信息，默认为最后一名奖励

    Args:
        user: 用户对象

    Returns:
        当前排名奖励信息
    """
    game_config = user.env.game_config
    config = logics.get_award_detail(user.arena.data['rank'], game_config)

    now = datetime.datetime.now()
    end_time = get_arena_end_time(user.env)
    cd_delta = (end_time - now).seconds if end_time > now else 0

    return {
        'gold': config['round']['gold'],
        'score': config['round']['score'],
        'loot': logics.format_award_loot(config, game_config),
        'cd_delta': cd_delta,
    }


def user_rank_info(env, uid, **kwargs):
    """格式化用户排名基础信息

    Args:
        env: 运行环境
        uid: 用户uid
        kwargs: 动态参数

    Returns:
        用户排名基础信息
    """
    user_app = env.import_app('user')
    user = user_app.get_user(env, uid, read_only=True)

    user.load_base()
    user.game.load_arena()
    user.load_all()

    if not user.arena.data['rank']:
        get_or_init_arena(user)

    data = {
        'uid': user.pk,
        'username': user.game.info['username'],
        'role': user.game.info['role'],
        'level': user.game.user['level'],
        'rank': user.arena.data['rank'],
    }

    data.update(kwargs)

    return data


def get_or_init_arena(user):
    """获取用户竞技场对象

    竞技场排名默认是按进入先后顺序排列，其后战斗角逐

    Args:
        user: 用户对象

    Returns:
        竞技场对象
    """
    arena = user.game.arena

    if arena.rank is None:
        arena.zadd(constants.DEFAULT_MAX_SCORE - time.time())

    if user.arena.data['rank'] != arena.rank:
        user.arena.data['rank'] = arena.rank
        user.arena.data['rank_score'] = str(arena.score)

    return arena


def get_award_arena(user):
    """获取竞技场快照对象, 用于结算用

    Args:
        user: 用户对象

    Returns:
        竞技场快照对象
    """
    award = user.game.award

    return award


def snapshot_arena(env):
    """竞技排名快照
    """
    user = env.user

    user.game.load_arena()
    user.game.load_award()
    user.game.load(env)

    arena = get_or_init_arena(user)
    award = get_award_arena(user)

    arena.snapshot_to(award.key)


def arena_over(user, target, win=False):
    """战斗结算， 处理排名数据

    Args:
        user: 用户对象
        target: 目标用户对象
        win: 是否胜利
    """
    user_arena = get_or_init_arena(user)
    target_arena = get_or_init_arena(target)

    ts = int(time.time())
    change_rank = 0
    user_score = user_arena.score
    target_score = target_arena.score

    if user_arena.rank > target_arena.rank and win:
        change_rank = 1
        user_arena.zadd(target_score)
        target_arena.zadd(user_score)
        user.arena.data['rank'] = user_arena.rank
        target.arena.data['rank'] = target_arena.rank

    set_cont_win(user, win, ts)
    record_log(user, target, user_arena.rank, target_arena.rank,
               win, change_rank, ts)


def set_cont_win(user, win, ts):
    """设置连胜记录

    Args:
        user: 用户对象
        win: 是否胜利
        ts: 战斗发生时间戳
    """
    if win:
        incr_arena_attr(user, cont_win=1, battle=1)
        user.arena.data['battle_at'] = 0
    else:
        incr_arena_attr(user, battle=1)
        user.arena.data['cont_win'] = 0
        user.arena.data['battle_at'] = ts


def record_log(user, target, user_rank, target_rank, win, change_rank, ts):
    """记录交战双方日志

    Args:
        user: 用户对象
        target: 对手用户对象
        user_rank: 用户排名
        target_rank: 对手排名
        win: 是否胜利
        chang_rank: 排名是否改变
        ts: 战斗发生时间
    """
    user_log = {
        'ts': ts,
        'type': constants.ARENA_LOG_TYPE_ATK,
        'win': win,
        'target_id': target.pk,
        'target_name': target.game.info['username'],
        'change_rank': change_rank and user_rank or 0,
    }

    target_log = {
        'ts': ts,
        'type': constants.ARENA_LOG_TYPE_DEF,
        'win': not win,
        'target_id': user.pk,
        'target_name': user.game.info['username'],
        'change_rank': change_rank and target_rank or 0,
    }

    add_log(user, user_log)
    add_log(target, target_log)


def add_log(user, log):
    """添加日志记录, 并删除过时的记录

    Args:
        user: 用户对象
        log: 数据对象
    """
    log_id = '%d_%s_%s_%s_%d' % (user.pk,
                                 log['ts'],
                                 log['type'],
                                 log['target_id'],
                                 log['win'],
                                )

    user.arena.logs.add(log_id, **log)

    log_ids = sorted(user.arena.logs.iterkeys(), reverse=True)

    for del_id in log_ids[constants.ARENA_LOG_RECORD_NUM:]:
        user.arena.logs.remove(del_id)


def pre_use_arena(env):
    """调用数据前需处理的数据
    """
    user_arena = env.user.arena
    today = time.strftime('%Y-%m-%d')

    if user_arena.data['last_date'] != today:
        user_arena.data['last_date'] = today
        user_arena.data['battle'] = 0
        user_arena.data['battle_at'] = 0
        user_arena.data['viral'] = ''
        user_arena.data['refresh'] = 0

    if not user_arena.data['per_at']:
        user_arena.data['per_at'] = int(time.time())

    timed_per_award(env.user)


def timed_per_award(user):
    """ 定时增加用户竞技奖励

    Args:
       user: 用户对象

    Returns:
        返回到下次奖励时间差
    """
    current_time = int(time.time())
    game_config = user.env.game_config
    user_arena = user.arena

    config = logics.get_award_detail(user_arena.data['rank'], game_config)

    differ = current_time - user.arena.data['per_at']
    quotient, remainder = divmod(differ, constants.DEFAULT_PER_DELTA_SECONDS)

    if quotient > 0:
        score = user_arena.data['score'] + quotient * config['per']['score']
        gold = user.game.user['gold'] + quotient * config['per']['gold']

        user.game.user['gold'] = gold
        user_arena.data['score'] = score
        user_arena.data['per_at'] = current_time - remainder

    return remainder


def get_arena_start_time(env):
    """获取竞技场开始时间

    Args:
        env: 运行环境

    Returns:
        datetime时间对象
    """
    start_time = env.game_config[constants.ARENA_START_TIME_NAME]

    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()

    differ = (now - start_time).days
    quotient, _ = divmod(differ, constants.ARENA_CRYCLE_DAYS)

    return start_time + datetime.timedelta(days=constants.ARENA_CRYCLE_DAYS * quotient)


def get_arena_end_time(env):
    """获取竞技场结束时间

    Args:
        env: 运行环境

    Returns:
        datetime时间对象
    """
    start_time = get_arena_start_time(env)

    end_date = start_time + datetime.timedelta(days=constants.ARENA_CRYCLE_DAYS - 1)
    timedelta = datetime.datetime.strptime(constants.ARENA_END_TIME, '%H:%M:%S') - \
                datetime.datetime.strptime(constants.ARENA_START_TIME, '%H:%M:%S')

    return end_date + timedelta


def set_arena_start_time(env, date=None):
    """设置竞技场开始时间

    Args:
        env: 运行环境
        date: 日期字符串，不传默认为今天

    Returns:
        时间字符串
    """
    if not date:
        date = time.strftime('%Y-%m-%d')

    start_time = '%s %s' % (date, constants.ARENA_START_TIME)
    config_app.set_config(env, constants.ARENA_START_TIME_NAME, start_time)

    return start_time

