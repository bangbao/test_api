# coding: utf-8

import time
import hashlib
import itertools
from collections import defaultdict

from . import constants


def calc_delta_second(at, cd):
    """计算时间差额

    Args:
        at: 旧时间
        cd: 间隔cd, 单位分钟

    Returns:
        时间差额
    """
    delta = at + cd * constants.EQUIP_ST_CD_SECOND - int(time.time())

    if delta < 0:
        delta = 0

    return delta


def equip_birth(cfg_id, game_config, **kwargs):
    """由装备配置ID生成一个能用的装备对象

    Args:
        cfg_id: 配置ID
        game_config: 游戏配置,包括装备配置
        kwargs: 动态参数

    Returns:
        装备对象
    """
    detail = game_config['equips'][cfg_id]

    obj = dict(constants.EQUIP_BIRTH_INIT, cfg_id=cfg_id,)
    obj['sign'] = equip_sign(obj, game_config)

    for tp, tp_data in detail['data'].iteritems():
        if tp_data['ability'] != constants.EQUIP_ABILITY_NONE:
            attr = constants.EQUIP_ABILITY_DATA[tp_data['ability']]
            obj[attr] += tp_data['value']

    level = kwargs.pop('level', 1)

    for i in xrange(1, level):
        obj = equip_upgrade(obj, game_config)

    obj.update(kwargs)

    return obj


def equip_upgrade(obj, game_config):
    """装备升级

    Args:
        obj: 装备对象
        game_config: 游戏配置,包括装备配置
    """
    detail = get_equip_detail(obj, game_config)
    obj['level'] += 1

    for tp, tp_data in detail['data'].iteritems():
        if tp_data['ability'] != constants.EQUIP_ABILITY_NONE:
            attr = constants.EQUIP_ABILITY_DATA[tp_data['ability']]
            obj[attr] += tp_data['level_add']

    return obj


def get_equip_detail(obj, game_config):
    """获取某个装备的配置信息

    Args:
        obj: 装备对象
        game_config: 游戏配置,包括装备配置

    Returns:
        卡牌在配置中的信息
    """
    equips = game_config['equips']

    return equips[obj['cfg_id']]


def equip_info(obj, game_config, **kwargs):
    """把一个装备对象转换成前端需要显示的格式

    Args:
        obj: 装备对象
        game_config: 游戏配置 包括装备配置
        kwargs: 动态属性

    Returns:
        装备信息
    """
    detail = get_equip_detail(obj, game_config)

    return dict(obj,
                sort=detail['sort'],
                star=detail['star'],
                name=detail['name'],
                image=detail['image'],
                icon=detail['icon'],
                can_resolve=detail['can_resolve'],
                **kwargs)


def apply_equip_effect(obj, pos_equips):
    """应用装备效果

    Args:
        obj: 卡牌对象
        pos_equips: 编队位置装备们

    Returns:
        应用效果后的卡牌对象
    """
    for equip in itertools.ifilter(None, pos_equips):

        for attr in constants.EQUIP_ABILITY_ATTRS:
            obj[attr] += equip[attr]

    return obj


def get_equip_incr(detail):
    """获取装备强化属性增长数据

    Args:
        detail: 装备配置

    Returns:
        增长数据
    """
    return {'data': detail['data']}


def equip_sign(obj, game_config, sign_key="%(level_add)s.%(ability)s.%(value)s"):
    """创建生长签名

    根据生长类型, 初始数值创建签名，当配置更改时可以自动更新

    Args:
       obj: 装备详细
       game_config: 游戏配置
       sign_key: 签名key

    Returns:
       装备数值签名
    """
    detail = get_equip_detail(obj, game_config)

    obj = hashlib.md5()
    for tp, data in detail['data'].iteritems():
        obj.update(sign_key % data)

    return obj.hexdigest()


def equip_reborn(obj, game_config):
    """装备重生

    Args:
       obj: 装备对象
       game_config: 游戏全局配置

    Returns:
       装备数据
    """
    kwargs = {
        'level': obj['level'],
        'gold': obj['gold'],
    }

    return equip_birth(obj['cfg_id'], game_config, **kwargs)


def apply_job_effect(obj, detail):
    """卡牌应用职业的附加效果

    Args:
        obj: 卡牌对象
        detail: 职业的配置详细
    """
    bf_init = obj['bf_init']

    obj['hp'] += int(bf_init['hp'] * (detail['hp'] - 1))
    obj['natk'] += int(bf_init['natk'] * (detail['natk'] - 1))
    obj['ndef'] += int(bf_init['ndef'] * (detail['ndef'] - 1))
    obj['matk'] += int(bf_init['matk'] * (detail['matk'] - 1))
    obj['mdef'] += int(bf_init['mdef'] * (detail['mdef'] - 1))

    obj['hit'] += detail['hit']
    obj['dodge'] += detail['dodge']
    obj['storm_hit'] += detail['storm_hit']
    obj['holdout_storm'] += detail['holdout_storm']


def filter_trans_job(game_config):
    """过滤掉不能转职的卡牌

    Args:
        game_config: 游戏全局配置

    Returns:
        是否能转职的过滤函数
    """
    class_evolution = game_config['class_evolution']

    def wrapper(obj):
        """判断卡牌对象是否可转职

        Args:
            obj: 卡牌对象

        Returns:
            是否能转职
        """
        return obj['job'] in class_evolution

    return wrapper


def filter_merge_equip(game_config):
    """过滤掉不能合成的装备配置

    Args:
        game_config: 游戏配置

    Returns:
        能合成的装备详细配置，装备分类配置
    """
    equips_config = game_config['equips']
    equip_quality = game_config['equip_quality']
    same_cfg_set = set(equips_config) & set(equip_quality)

    new_equips = defaultdict(list)
    new_equip_merge = defaultdict(list)

    for cfg_id in same_cfg_set:
        detail = equips_config[cfg_id]
        where = constants.EQUIP_SORT_WHERES[detail['sort']]
        new_equips[where].append(cfg_id)
        new_equip_merge[detail['destiny_type']].append(cfg_id)

    return new_equips, new_equip_merge


