# coding: utf-8

import time
import itertools
from collections import defaultdict

from lib.utils import sys_random as random
from apps.public.generator import salt_generator
from . import logics
from . import constants


def add_food_effect(pet_obj, pet_detail, food_detail):
    """添加食物的食用效果

    Args:
        pet_obj: 宠物对象
        pet_detail: 宠物详细
        food_detail: 食物详细

    Returns:
        食用效果
    """
    if pet_detail['food_like'] == food_detail['food_type']:
        exp_mul, attr_mul, full_mul = constants.PET_FOOD_TYPE_MAP['like']
    elif pet_detail['food_wary'] == food_detail['food_type']:
        exp_mul, attr_mul, full_mul = constants.PET_FOOD_TYPE_MAP['wary']
    else:
        exp_mul, attr_mul, full_mul = constants.PET_FOOD_TYPE_MAP['common']

    add = food_detail['add']
    effect_data = defaultdict(int)
    effect_data['exp'] = int(add['exp'] * exp_mul)

    add_full_top = int(pet_detail['full'] * full_mul)
    full_delta = max(add_full_top - pet_obj['full'], 0)
    effect_data['full'] = min(full_delta, add['full'])

    #for ability in add['ability']:
    #    attr = constants.PET_FOOD_ABiLITY_MAP[ability]
    #    value = random_value(add['value'], attr_mul)
    #
    #    if attr in pet_obj:
    #        effect_data[attr] += value

    for attr, value in effect_data.iteritems():
        pet_obj[attr] += value

    return dict(effect_data)


def birth_pet(user, cfg_id, where=0, ext=0, **kwargs):
    """生成一个宠物对象添加到用户数据中

    Args:
        user: 用户对象
        cfg_id: 配置id
        where: 来源
        ext: 扩展标识
        kwargs: 动态参数

    Returns:
        宠物数据
    """
    game_config = user.env.game_config

    pet = logics.pet_birth(cfg_id, game_config, **kwargs)

    return add_pet(user, pet, where, ext)


def add_pet(user, pet, where=0, ext=0):
    """添加一个新宠物对象并保存到用户数据中

    Args:
        user: 用户对象
        pet: 宠物数据对象
        where: 来源
        ext: 扩展标识
    """
    pet_id = '%s_%d_%d_%s_%d_%s' % (user.pk,
                                    int(time.time()),
                                    pet['cfg_id'],
                                    salt_generator(),
                                    where,
                                    ext)
    user.hero.pets.add(pet_id, **pet)

    return {
        'pet_id': pet_id,
        'pet': pet,
    }

def format_pets(user, pet_ids, filter_func=any):
    """格式化多个宠物信息

    Args:
        user: 用户对象
        pet_ids: 宠物id们
        filter_func: 过滤函数

    Returns:
        宠物信息们
    """
    game_config = user.env.game_config
    hero_pets = user.hero.pets
    used_pet = get_played_pet(user)
    pets = {}

    for pet_id in itertools.ifilter(None, pet_ids):
        obj = hero_pets[pet_id]

        if filter_func(obj):
            used = pet_id in used_pet
            pets[pet_id] = logics.pet_info(obj, game_config,
                                           used=used)

    return pets


def format_items(user):
    """获取食物材料数据

    Args:
        user: 用户对象

    Returns:
        食物材料背包
    """
    game_config = user.env.game_config
    item_config = game_config['item']

    return dict((cfg_id, logics.item_info(obj, item_config[cfg_id]))
                for cfg_id, obj in user.hero.items.iteritems())


def del_pets(user, pet_ids):
    """删除多个宠物 若宠物在使用中，不删除

    Args:
        user: 用户对象
        pet_ids: 要删除的宠物id们
    """
    pets = user.hero.pets
    used_pet = get_played_pet(user)

    for pet_id in pet_ids:
        if pet_id != used_pet:
            pets.remove(pet_id)


def get_played_pet(user):
    """获取出战的宠物
    """
    return user.game.user['pet']


def set_played_pet(user, pet_id):
    """设定出战的宠物
    """
    user.game.user['pet'] = pet_id


def apply_pet_effect(user, formation):
    """卡牌编队应用宠物效果

    Args:
        user: 用户对象
        formation: 编队对象列表

    Returns:
        应用效果后编队对象列表
    """
    game_config = user.env.game_config
    pet_id = get_played_pet(user)
    pet_obj = user.hero.pets.get(pet_id)

    if not pet_obj:
        return

    pet_item = logics.get_pet_item(pet_obj, game_config)
    ratio = logics.calc_full_ratio(pet_obj, game_config)
    skills = logics.skill_get(pet_obj)

    for obj in itertools.ifilter(None, formation):
        logics.apply_pet_base_effect(obj, pet_item, ratio)
        logics.apply_pet_skill_effect(obj, skills, game_config)


def check_pet_full(user):
    """修正宠物当前饱食度

    宠物的饱食度每3分钟下降1%

    Args:
        user: 用户对象
    """
    game_config = user.env.game_config
    current_time = int(time.time())
    pet_at = user.hero.data['pet_at']

    quotient, remainder = divmod(current_time - pet_at,
                                 constants.PET_FULL_REDUCE_CYCLE_SECENDS)

    if quotient <= 0:
        return

    for pet_id, obj in user.hero.pets.iteritems():
        detail = logics.get_pet_detail(obj, game_config)
        delta = int(quotient * detail['full'] * constants.PET_FULL_REDUCE_RATIO)

        if delta and obj['full']:
            new_full = max(obj['full'] - delta, 0)
            user.hero.pets.modify(pet_id, full=new_full)

    user.hero.data['pet_at'] = current_time - remainder


def random_value(value, attr_mul=1):
    """
    """
    if len(value) == 1:
        return int(value[0] * attr_mul)

    return int(random.randint(*value) * attr_mul)

