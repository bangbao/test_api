# coding: utf-8

from cheetahes.utils import sys_random as random

import time
import bisect
import constants


def nearby_rank(rank):
    """按规则取出一个名次附近的名次们

    Args:
        rank: 名次， 从1开始

    Returns:
        名次们
    """
    idx = bisect.bisect_left(constants.ARENA_NEAR_RANKS, rank)
    near_area = constants.ARENA_NEAR_AREAS[idx]
    ranks = []

    for a, b, n in near_area:
        before = max(rank + a, 1)
        behind = max(rank + b, 1)
        xranks = xrange(before, behind)
        sample = random.sample(xranks, n)

        ranks.extend(sample)

    return sorted(ranks)


def get_award_detail(rank, game_config):
    """根据排名获取奖励详细

    Args:
        rank: 排名，从1开始
        game_config: 游戏配置

    Returns:
        奖励详细
    """
    arena_award = game_config['arena_award']

    idx = bisect.bisect_left(arena_award['ranks'], rank)
    cur_idx = min(idx, arena_award['max_idx'])

    return arena_award['configs'][cur_idx]


def format_award_loot(award, game_config):
    """根据排名获取奖励详细

    Args:
        award: 奖励详细
        game_config: 游戏配置

    Returns:
        掉落详细
    """
    round_type = award['round_type']
    value = award['value']
    num = award['num']
    loot = []

    if not all((round_type, value, num)):
        return loot

    config_key = constants.ARENA_AWARD_ROUND_TYPE_CONFIG_KEY_MAP[round_type]
    config = game_config[config_key]

    for goods_id in value['goods']:
        detail = config[goods_id]

        loot.append({
                'name': detail['name'],
                'num': num,
            })

    return loot


def calc_battle_delta(battle_at):
    """计算战斗cd时间

    Args:
        battle_at: 上次战斗时间戳

    Returns:
        离下次战斗时间
    """
    battle_delta = 0

    if battle_at:
        delta_time = constants.DEFAULT_ARENA_DELTA_SECONDS + battle_at - int(time.time())
        battle_delta = max(delta_time, battle_delta)

    return battle_delta
