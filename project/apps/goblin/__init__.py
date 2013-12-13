# coding: utf-8

import time
import bisect
import datetime
import itertools

from lib.utils import get_it
from lib.utils import sys_random as random
from lib.db.expressions import Incr
from apps.public import logics as publics
from apps.public.generator import salt_generator
from . import logics
from . import constants


def forge_goods(user, cost_effect):
    """打造物品

    Args:
        user: 用户对象
        cost_effect: 选择的效果方式

    Returns:
        物品掉落数据
    """
    game_config = user.env.game_config
    forge_obj, next_obj = logics.get_forge_config(user.hero.data['forge_level'],
                                                  game_config)
    cfg_id = logics.goblin_loot(forge_obj['loot'])

    birth_goblin(user, cfg_id, where=constants.GOBLIN_FROM_FORGE)
    user.hero.data['forge_cycle'] = 0
    user.hero.data['forge_point'] = 0
    user.hero.data['forge_level'] = 0

    detail = game_config['goblins'][cfg_id]

    return [{'star': detail['star'], 'name': detail['name'],
             'image': detail['image'], 'level': 1}]


def forge_point(user, cost_effect):
    """打造点数

    Args:
        user: 用户对象
        cost_effect: 选择的效果方式

    Returns:
        效果触发数据
    """
    game_app = user.env.import_app('game')
    master_data = get_master_data(user)

    point = constants.GOBLIN_FORGE_POINT_MAX
    is_luck = get_it(master_data['luck'])
    if not is_luck:
        point = random.randint(constants.GOBLIN_FORGE_POINT_MIN,
                               constants.GOBLIN_FORGE_POINT_MAX)

    effect = master_data['effect']
    is_crt = get_it(master_data['crt'])
    if not is_crt:
        effect = constants.GOBLIN_FORGE_POINT_CRT_DEFAULT

    inspire = constants.GOBLIN_FORGE_POINT_INSPIRE_DEFAULT
    is_inspire = get_it(constants.GOBLIN_FORGE_POINT_INSPIRE_RATE)
    if is_inspire:
        inspire = random.choice(constants.GOBLIN_FORGE_POINT_INSPIRE_AREA)

    is_insight = get_it(constants.GOBLIN_FORGE_POINT_INSIGHT_RATE)
    if is_insight:
        insight = random.choice(constants.GOBLIN_FORGE_POINT_INSIGHT_AREA)
        master_up(user, insight)

    gain_point = int(cost_effect['effect'] * point * effect + master_data['point'])

    incr_goblin_attr(user,
                     forge_point=gain_point,
                     forge_cycle=1,
                     forge=1 - inspire)
    game_app.incr_user_attr(user,
                            gold= -cost_effect['gold'],
                            kcoin= -cost_effect['kcoin'])

    return {
        'is_luck': is_luck,
        'is_crt': is_crt,
        'is_inspire': is_inspire,
        'is_insight': is_insight,
        'gain_point': gain_point,
        'cost_effect': cost_effect,
    }


def buy_pos_goblin(user, pos, game_config):
    """购买零件装备占位

    Args:
        user: 用户对象
        pos: 编队位置
    """
    game_app = user.env.import_app('game')
    goblin_position = game_config['goblin_position']

    extend_idx = extend_pos_goblin(user, pos)

    if goblin_position['min_idx'] <= extend_idx <= goblin_position['max_idx']:
        cost_kcoin = goblin_position['open_ku'][extend_idx]
        game_app.incr_user_attr(user, kcoin= -cost_kcoin)


def get_master_data(user):
    """获取工匠们的效果数据

    Args:
        user: 用户对象

    Returns:
        工匠们的效果数据
    """
    masters = masters_get(user)

    goblin_master = user.env.game_config['goblin_master']
    TYPES = constants.GOBLIN_DEFAULT_MASTER_TYPES

    return dict((attr, goblin_master[level][attr])
                for level, attr in itertools.izip(masters, TYPES))


def get_goblin_data(user):
    """获取用户地精科技锻造当前数据

    Args:
        user: 用户对象

    Returns:
        用户当前显示锻造数据
    """
    game_config = user.env.game_config
    data = user.hero.data
    forge_obj, next_obj = logics.get_forge_config(data['forge_level'], game_config)

    return {
        'forge': data['forge_cycle'],
        'forge_left': get_forge_daily_top(user) - data['forge'],
        'forge_delta': constants.GOBLIN_FORGE_DELTA,
        'forge_level': data['forge_level'],
        'forge_point': data['forge_point'],
        'forge_point_top': next_obj['point'],
    }


def get_forge_daily_top(user):
    """获取用户每天锻造次数，vip用户有加成

    Args:
        user: 用户对象

    Returns:
        每天锻造次数
    """
    return constants.GOBLIN_FORGE_DAILY_TIMES


def master_reset(user, today):
    """每天检查重置用户工匠等级

    Args:
        user: 用户对象
    """
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    start_time = user.env.game_config['arena_start_time']
    start_time = datetime.datetime.strptime(start_time, DATETIME_FORMAT)
    today = datetime.datetime.strptime(today, '%Y-%m-%d')

    cycle_days = constants.GOBLIN_MASTER_UP_CYCLE_DAYS
    differ = (today - start_time).days
    quotient, remainder = divmod(differ, cycle_days)
    start_time += datetime.timedelta(days=cycle_days * quotient)

    master_at = user.hero.data['master_at']
    masters = user.hero.data['masters']
    if not masters or not master_at or \
        datetime.datetime.strptime(master_at, DATETIME_FORMAT) < start_time:

        user.hero.data['master_at'] = start_time.strftime(DATETIME_FORMAT)
        user.hero.data['masters'] = constants.GOBLIN_DEFAULT_MASTERS

    user.hero.data['master_up'] = 0


def master_up(user, master):
    """工匠升级

    Args:
        user: 用户对象
        master: 工匠位置

    Returns:
        工匠数据
    """
    masters = masters_get(user)
    goblin_master = user.env.game_config['goblin_master']
    level = masters[master]
    max_level = max(goblin_master)

    masters[master] = min(level + 1, max_level)
    masters_put(user, masters)

    return masters


def masters_get(user):
    """获取工匠数据

    Args:
        user: 用户对象
    """
    masters = publics.delimiter_list(user.hero.data['masters'])

    return map(int, masters)


def masters_put(user, masters):
    """保存工匠数据

    Args:
        user: 用户对象
        masters: 工匠级别列表
    """
    masters = itertools.imap(str, masters)

    user.hero.data['masters'] = publics.delimiter_str(masters)


def incr_goblin_attr(user, **kwargs):
    """修改用户零件相关属性值

    Args:
        user: 用户对象
        kwargs: 属性键值对
    """
    field = user.hero.data

    forge_point = kwargs.pop('forge_point', 0)
    add_forge_point(user, forge_point)

    for attr, value in kwargs.iteritems():
        field[attr] = Incr(attr, value, field)


def add_forge_point(user, forge_point):
    """锻造点数增加时触发升级

    Args:
        user: 用户对象
        forge_point: 增加的锻造点数
    """
    if not forge_point:
        return

    game_config = user.env.game_config
    level = user.hero.data['forge_level']
    point = user.hero.data['forge_point']

    forge_obj, next_obj = logics.get_forge_config(level, game_config)
    new_point = point + forge_point

    while new_point - next_obj['point'] >= 0:
        level = next_obj['level']
        new_point -= next_obj['point']

        forge_obj, next_obj = logics.get_forge_config(level, game_config)

    user.hero.data['forge_level'] = level
    user.hero.data['forge_point'] = new_point


def birth_goblin(user, cfg_id, where=0, ext=0, **kwargs):
    """生成一个零件对象添加到用户数据中

    Args:
        user: 用户对象
        cfg_id: 配置id
        where: 来源
        ext: 扩展标识
        kwargs: 动态参数

    Returns:
        零件数据
    """
    game_config = user.env.game_config
    goblin = logics.goblin_birth(cfg_id, game_config, **kwargs)

    return add_goblin(user, goblin, where, ext)


def add_goblin(user, goblin, where=0, ext=0):
    """添加一个新零件对象并保存到用户数据中

    Args:
        user: 用户对象
        goblin: 零件数据对象
        where: 来源
        ext: 扩展标识
    """
    obj_id = '%s_%d%s_%d_%d%d' % (user.pk,
                                  int(time.time()),
                                  goblin['cfg_id'],
                                  salt_generator(),
                                  where,
                                  ext)
    user.hero.goblins.add(obj_id, **goblin)

    return {
        'goblin_id': obj_id,
        'goblin': goblin,
    }


def get_used_goblin(user):
    """获取使用中的零件id

    Args:
        user: 用户对象

    Returns:
        零件id集合
    """
    used_goblin = {}
    filter_func = lambda x: x and x != constants.GOBLIN_POS_HOLE_UNOPENED

    for pos in constants.GOBLIN_TEAM_POS_KEYS:
        goblin_list = get_pos_goblin(user, pos)

        for goblin_id in itertools.ifilter(filter_func, goblin_list):
            used_goblin[goblin_id] = pos

    return used_goblin


def get_team_goblin(user):
    """获取编队零件

    Args:
        user: 用户对象

    Returns:
        编队零件
    """
    return dict((pos, get_pos_goblin(user, pos))
                 for pos in constants.GOBLIN_TEAM_POS_KEYS)


def get_pos_goblin(user, pos):
    """获取一个位置的零件

    Args:
        user: 用户对象
        pos: 零件编队位置

    Returns:
        零件
    """
    value = user.game.goblin[pos]
    holes = publics.delimiter_list(value) if value else []

    return logics.rectify_hole(holes)


def set_pos_goblin(user, pos, pos_goblin, idx=None):
    """设定一个位置的零件

    Args:
        user: 用户对象
        pos: 编队位置
        pos_goblin: 此位置零件
        idx: 开启的位置
    """
    if idx is not None:
        pos_goblin[idx] = None

    holes = logics.rectify_hole(pos_goblin)
    user.game.goblin[pos] = publics.delimiter_str(holes)


def extend_pos_goblin(user, pos):
    """开启下个零件占位

    Args:
        user: 用户对象
        pos: 开启的编队位置

    Returns:
        开启的位置 或者 None
    """
    pos_goblin = get_pos_goblin(user, pos)
    upopened_key = constants.GOBLIN_POS_HOLE_UNOPENED

    if upopened_key in pos_goblin:
        extend_idx = pos_goblin.index(upopened_key)
        set_pos_goblin(user, pos, pos_goblin, extend_idx)

        return extend_idx


def check_pos_gobllin(user):
    """用户升级时检查零件位置是否需要自动开启

    Args:
        user: 用户对象
    """
    upopened_key = constants.GOBLIN_POS_HOLE_UNOPENED
    level = user.game.user['level']
    config = user.env.game_config['goblin_position']
    open_idx = bisect.bisect_right(config['open_level'], level)
    team_goblin = get_team_goblin(user)

    for pos, pos_goblin in team_goblin.iteritems():
        opened = False

        for idx, goblin_id in enumerate(pos_goblin[:open_idx]):
            if goblin_id == upopened_key:
                pos_goblin[idx] = None
                opened = True

        if opened:
            set_pos_goblin(user, pos, pos_goblin)


def format_goblins(user, goblin_ids, filter_func=None):
    """格式化多个零件信息

    Args:
        user: 用户对象
        goblin_ids: 零件id们
        filter_func: 过滤函数

    Returns:
        零件信息们
    """
    user_hero = user.hero
    game_config = user.env.game_config
    used_goblin = get_used_goblin(user)
    filter_func = filter_func or (lambda x: True)
    goblins = {}

    for goblin_id in itertools.ifilter(None, goblin_ids):
        obj = user_hero.goblins[goblin_id]

        if filter_func(obj):
            used = goblin_id in used_goblin
            goblins[goblin_id] = logics.goblin_info(obj, game_config,
                                                    used=used)

    return goblins


def del_goblins(user, goblin_ids):
    """删除多个零件

    删除零件， 若零件在使用中，不删除

    Args:
        user: 用户对象
        goblin_ids: 要删除的零件id们
    """
    goblins = user.hero.goblins
    used_goblin = get_used_goblin(user)

    for goblin_id in goblin_ids:
        if goblin_id not in used_goblin:
            goblins.remove(goblin_id)


def apply_goblin_effect(user, formation):
    """卡牌编队应用装备效果

    Args:
        user: 用户对象
        formation: 编队对象列表

    Returns:
        应用效果后编队对象列表
    """
    game_config = user.env.game_config
    goblins = user.hero.goblins

    for pos, obj in itertools.izip(constants.GOBLIN_TEAM_POS_KEYS, formation):

        if obj:
            pos_goblin = get_pos_goblin(user, pos)
            pos_goblins = (logics.goblin_info(goblins[goblin_id], game_config)
                           for goblin_id in pos_goblin
                               if goblin_id in goblins)
            logics.apply_goblin_effect(obj, pos_goblins)


