# coding: utf-8

from cheetahes.utils import sys_random as random
from apps.public import logics as publics

import bisect
import itertools
import constants


def pet_birth(cfg_id, game_config, **kwargs):
    """由宠物配置ID生成一个能用的宠物对象

    Args:
        cfg_id: 配置ID
        game_config: 游戏配置
        kwargs: 动态参数

    Returns:
        宠物对象
    """

    obj = dict(constants.PET_BIRTH_INIT,
               cfg_id=cfg_id)

    level = kwargs.pop('level', 1)
    obj = pet_upgrade(obj, game_config)

    for _ in xrange(1, level):
        obj['exp'] = obj['level_up']

        obj = pet_upgrade(obj, game_config)

    obj.update(**kwargs)

    return obj

def pet_upgrade(obj, game_config):
    """宠物升级

    Args:
        obj: 宠物对象
        game_config: 游戏配置
    """


    up_detail = game_config['pet']
    detail = get_pet_detail(obj, game_config)
    level, star, clone = obj['level'], detail['star'], obj['clone']
    level_config = up_detail.get(level)

    if not level_config or not level_config[star][clone]:
        return obj

    need_exp = level_config[star][clone]

    while (obj['exp'] - need_exp >= 0):
        level += 1

        obj['exp'] -= need_exp
        obj['level'] = level

        level_config = up_detail.get(level)

        if not level_config or not level_config[star][clone]:
            obj['exp'] = 0
            break

        need_exp = level_config[star][clone]

    obj['level_up'] = need_exp - obj['exp']

    return obj

def get_pet_detail(obj, game_config):
    """获取某个宠物的配置信息

    Args:
        obj: 宠物对象
        game_config: 游戏配置

    Returns:
        在配置中的信息
    """

    pets = game_config['pets']

    return pets[obj['cfg_id']]

def get_pet_item(obj, game_config):
    """获取某个宠物对象的属性加成

    Args:
        obj: 宠物对象
        game_config: 游戏配置

    Returns:
        该宠物的对卡牌的属性加成
    """

    detail = get_pet_detail(obj, game_config)
    level, star = obj['level'], detail['star']

    return game_config['pet_item'][level]['detail'][star]

def item_info(obj, detail, **kwargs):
    """食物材料数据

    Args:
        obj: 食物对象
        detail: 游戏配置
        kwargs: 动态参数

    Returns:
        食物材料数据
    """

    return dict(num=obj['num'],
                name=detail['name'],
                stack_num=detail['stack_num'],
                food_type=detail['food_type'],
                icon=detail['icon'],
                **kwargs)

def pet_info(obj, game_config, **kwargs):
    """宠物数据背包信息

    Args:
        obj: 宠物对象
        game_config: 游戏配置
        kwargs: 动态参数

    Returns:
        宠物数据
    """

    detail = get_pet_detail(obj, game_config)
    pet_item = get_pet_item(obj, game_config)

    pet = dict(obj,
               full_top=detail['full'],
               name=detail['name'],
               image=detail['image'],
               icon=detail['icon'],
               **pet_item)

    pet = subjoin_skill_info(pet, detail, game_config)
    pet.update(kwargs)

    return pet

def subjoin_skill_info(obj, detail, game_config):
    """宠物添加天赋，普通技能信息

    Args:
        obj: 宠物数据
        detail: 宠物详细
        game_config: 游戏配置

    Returns:
        添加技能后的宠物数据
    """

    pet_skill = game_config['pet_skill']
    talent = detail['talent']
    skills = skill_get(obj)

    skills_list = []

    if talent:
        obj['talent'] = pet_skill[talent]

    for skill in skills:

        if skill in pet_skill:
            skills_list.append(pet_skill[skill])
        else:
            skills_list.append(skill)

    obj['skill'] = skills_list

    return obj

def rectify_skill(skill, clone, func=None):
    """校验宠物技能的完整性, 繁衍代数clone对应的技能数为clone+1

    Args:
        skill: 技能列表
        clone: 繁衍代数
        func: 对每个元素的处理函数

    Returns:
        完整的编队
    """

    skills = []
    fill = constants.PET_SKILL_UNOPENED
    length = len(constants.PET_SKILL_SEQ)
    func = func or (lambda x: x)

    for i, member in itertools.izip_longest(constants.PET_SKILL_SEQ,
                                            skill[:length]):
        if not member and i > clone:
            member = fill
        elif member == fill and i <= clone:
            member = None

        skills.append(func(member))

    return skills

def skill_get(obj):
    """
    """

    func = lambda x: int(x) if x and x.isdigit() else x
    skill = publics.delimiter_list(obj['skill']) if obj['skill'] else []

    return rectify_skill(skill, obj['clone'], func=func)

def skill_set(obj, skill):
    """
    """

    func = lambda x: str(x) if x else x
    skill = rectify_skill(skill, obj['clone'], func=func)

    obj['skill'] = publics.delimiter_str(skill)

def random_skill(skills, exclude=None):
    """随机选出一个技能

    Args:
        skills: 技能列表
        exclude: 排除列表

    Returns:
        不在排除列表中的一个技能
    """

    skill_sets = set(skills)
    exclude_sets = set(exclude or [])

    pool = list(skill_sets - exclude_sets)

    return random.choice(pool)

def apply_pet_base_effect(obj, pet_obj, ratio):
    """应用宠物的基本属性加成效果

    Args:
        obj: 卡牌战斗对象
        pet_obj: 宠物对象
        ratio: 饱食度的加成
    """

    for attr in constants.PET_EFFECT_ATTRS:
        obj[attr] += int(pet_obj[attr] * ratio)

def apply_pet_skill_effect(obj, skills, game_config):
    """应用宠物的技能加成效果

    Args:
        obj: 卡牌战斗对象
        skills: 宠物技能列表
        game_config: 游戏配置
    """

    pet_skill = game_config['pet_skill']

    filter_func = lambda x: x and x != constants.PET_SKILL_UNOPENED

    for skill_id in itertools.ifilter(filter_func, skills):
        skill_detail = pet_skill[skill_id]

        if cmp_sort(obj, skill_detail):
            apply_skill_effect(obj, skill_detail)

def calc_full_ratio(pet_obj, game_config):
    """计算饱食度对应用效果的影响

    Args:
        pet_obj: 宠物对象
        game_config: 游戏配置

    Returns:
        属性加成值
    """

    detail = get_pet_detail(pet_obj, game_config)
    full = float(pet_obj['full']) / detail['full']

    idx = bisect.bisect_left(constants.PET_FULL_EFFECT['full'], full)

    return constants.PET_FULL_EFFECT['effect'][idx]

def cmp_sort(obj, skill_detail):
    """判断技能是否对此卡牌生效

    宠物技能只对特定职业的卡牌生效

    Args:
        obj: 卡牌战斗对象
        skill_detail: 技能详细

    Returns:
        是否生效
    """

    return obj['job'] in skill_detail['effect_job']

def apply_skill_effect(obj, skill_detail):
    """应用单个宠物技能的效果

    Args:
        obj: 卡牌战斗对象
        skill_detail: 技能详细
    """

    for sort, value1, value2 in itertools.izip_longest(skill_detail['sort'],
                                                       skill_detail['value1'],
                                                       skill_detail['value2'],
                                                       fillvalue=0):
        attr = constants.PET_SKILL_SORT_MAP[sort]

        if attr in obj:
            obj[attr] += value1
            obj[attr] += int(obj[attr] * value2 / 100.0)
