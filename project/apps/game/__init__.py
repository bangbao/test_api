# coding: utf-8

import time

from lib.db.expressions import Incr
from . import constants
from .models import Game


def add_exp(user, exp, evolutions=None):
    """增加经验值

    Args:
        user: 用户对象
        exp: 增加的经验值
        evolutions: 记录升级时的烟花数据
    """
    user_config = user.env.game_config['user']
    game = user.game
    old_level = game.user['level']

    exp_config = user_config.get(old_level)
    level_up = game.user['level'] + 1
    level_up_config = user_config.get(level_up)

    if not level_up_config:
        return False

    game.user['exp'] += exp

    while (game.user['exp'] - exp_config['exp']) >= 0:
        game.user['level'] = level_up
        game.user['exp'] -= exp_config['exp']
        level_up += 1

        exp_config = user_config.get(game.user['level'])
        level_up_config = user_config.get(level_up)

        if not level_up_config:  # max level
            game.user['exp'] = 0
            return False

        game.info['energy'] = exp_config['energy']
        game.info['cost'] = exp_config['cost_top']
        game.info['friend'] = exp_config['friend_top']
        game.info['exp'] = exp_config['exp']
        game.user['energy'] = Incr('energy', exp_config['energy_resume'],
                                   game.user)

        evolution = {}
        evolution['level'] = game.user['level']
        evolution['hero_top'] = exp_config['friend_top']
        evolution['cost_top'] = exp_config['cost_top']

        if evolutions is not None:
            evolutions.append(evolution)

    return True


def incr_user_attr(user, **kwargs):
    """修改用户game_user表相关属性值

    Args:
        user: 用户对象
        kwargs: 属性键值对
    """
    field = user.game.user

    for attr, value in kwargs.iteritems():
        field[attr] = Incr(attr, value, field)


def incr_info_attr(user, **kwargs):
    """修改用户game_info表相关属性值

    Args:
        user: 用户对象
        kwargs: 属性键值对
    """
    field = user.game.info

    for attr, value in kwargs.iteritems():
        field[attr] = Incr(attr, value, field)


def get_game_data(user):
    """获取用户game数据
    """
    player_config = user.env.game_config['player']
    game_info = user.game.info
    game_user = user.game.user

    return {
        'info': game_info,
        'user': game_user,
        'side': which_side(game_user['light'], game_user['dark']),
        'res': player_config[game_info['role']]['res'],
    }


def pre_use_game(env):
    """加载该模块时需要预先处理一部分数据

    Args:
        env: 运行环境
    """
    current_time = int(time.time())

    timed_fill_energy(env.user, current_time)


def get_energy_heal_time(user):
    """获取体力恢复的时间间隔
    """
    return constants.ENERGY_HEAL_TIME


def timed_fill_energy(user, current_time):
    """ 定时补充用户体力

    Args:
       user: 用户对象
       current_time: 当前时间
    """
    game = user.game
    differ = current_time - game.info['energy_fill_at']
    quotient, remainder = divmod(differ, get_energy_heal_time(user))

    if quotient > 0:
        energy = min(game.user['energy'] + (quotient * constants.ENERGY_HEAL_UNIT),
                     game.info['energy'])
        game.user['energy'] = energy
        game.info['energy_fill_at'] = current_time - remainder

    if game.user['energy'] < 0:
        game.user['energy'] = 0


def calc_expense_cost(user):
    """计算用户消费产品

    Args:
       user: 用户对象

    Returns:
       每项要花费的酷币
    """
    game_config = user.env.game_config
    obj = {}

    master_up_key = constants.USER_EXPENSE_MASTER_UP
    master_up_idx = constants.USER_EXPENSE_INDEX[master_up_key]

    expense = game_config['expense'][master_up_idx]['expense']
    counter = min(user.hero.data[master_up_key], len(expense) - 1)

    obj[master_up_key] = expense[counter]

    return obj


def which_side(light, dark):
    """由光暗点数判断属于哪个阵营

    Args:
        side_point: 光暗点数

    Returns:
        阵营

    TODO:
        判断规则以后添加
    """
    return 1

