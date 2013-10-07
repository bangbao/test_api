# coding: utf-8

import hashlib
import itertools
import constants


def rectify_team(team):
    """校验编队的完整性

    Args:
        team: 编队列表

    Returns:
        完整的编队
    """
    new_team = []

    for i, member in itertools.izip_longest(constants.HERO_TEAM_SEQ, team):
        new_team.append(constants.TEAM_MEMBER_DEFAULTS.get(member, member))

    return new_team


def hero_birth(hero_id, game_config, **kwargs):
    """生成一个开奖的数据对象

    根据卡牌id和游戏配置生成一个卡牌的数据对象

    Args:
       hero_id: 卡牌的配置id
       game_config: 游戏配置
       kwargs: 动态参数

    Returns:
        卡牌对象
    """
    hero = game_config['heros'][hero_id]

    obj = dict(cfg_id=hero_id, level=1, exp=0, level_up=0,
               lock=0, askill=1, nskill=1,
               cost=hero['cost'],
               job=hero['job'],
               **hero['init'])

    obj['sign'] = hero_sign(obj, game_config)
    level = kwargs.pop('level', 1)
    obj = hero_upgrade(obj, game_config)

    for i in xrange(1, level):
        obj['exp'] = obj['level_up']

        obj = hero_upgrade(obj, game_config)

    obj.update(kwargs)

    return obj


def hero_upgrade(obj, game_config, evolutions=None):
    """卡牌升级

    提升卡牌的等级，基础属性

    Args:
        obj: 卡牌对象
        game_config: 游戏配置
        evolution: 是否是进阶

    Returns:
        升级后的卡牌对象
    """
    obj_detail = get_hero_detail(obj, game_config)
    up_detail = game_config['hero']
    level = obj['level']
    level_config = up_detail.get(level)

    if not level_config:
        return obj

    if obj['level'] >= obj_detail['max_level']:
        obj['exp'] = 0

        return obj

    need_exp = level_config['detail'][obj_detail['type']]['need']

    while (obj['exp'] - need_exp >= 0):
        level += 1
        evolution = {}

        obj['exp'] -= need_exp
        obj['level'] = level

        for up_name, up_value in obj_detail['incr'].iteritems():
            evolution[up_name] = [obj[up_name], up_value]
            evolution['exp'] = need_exp
            evolution['level'] = level
            obj[up_name] += up_value

        if evolutions is not None:
            evolutions.append(evolution)

        if obj['level'] >= obj_detail['max_level']:
            obj['exp'] = 0
            break

        level_config = up_detail.get(level)

        if not level_config:
            obj['exp'] = 0
            break

        need_exp = level_config['detail'][obj_detail['type']]['need']

    obj['level_up'] = need_exp - obj['exp']

    return obj


def get_hero_detail(obj, game_config):
    """获取某个卡牌的配置信息

    Args:
        obj: 卡牌对象
        game_config: 游戏配置

    Returns:
        卡牌在配置中的信息
    """
    heros = game_config['heros']

    return heros[obj['cfg_id']]


def hero_info(obj, game_config, **kwargs):
    """把一个卡牌对象转换成前端需要显示的格式

    Args:
        obj: 卡牌对象
        game_config: 游戏配置 包括卡牌详细配置，技能配置，命运配置
        kwargs: 动态属性

    Returns:
        卡牌信息
    """
    hero_detail = get_hero_detail(obj, game_config)

    info = dict(obj, star=hero_detail['star'],
                type=hero_detail['type'],
                name=hero_detail['name'],
                level_top=hero_detail['max_level'],
                image=hero_detail['image'],
                icon=hero_detail['icon'],
                res=hero_detail['res'],
                story=hero_detail['story'])

    info = subjoin_skill_info(info, hero_detail, game_config)
    info = subjoin_destiny_info(info, hero_detail, game_config)
    info.update(kwargs)

    return info


def calc_merge_value(value, merge_type):
    """ 计算根据合成类型，所加成的数值

    Args:
       value: 初始数值
       merge_type: 合成类型

    Returns:
       应加的数值
    """
    return constants.HERO_MULTIPLE_MERGE_TYPE[merge_type] * value


def calc_merge_cost(dst, goods):
    """ 计算合成所需要的花费

    Args:
       dest: 目标卡牌对象
       goods: 材料列表

    Returns:
       所需要花费的金币
    """
    return dst['level'] * constants.HERO_MERGE_COST * len(goods)


def calc_merge_exp(src, dst, game_config):
    """计算合成获取的经验

    相同职业提供经验有加成

    Args:
        src: 材料卡牌对象
        dst: 目标卡牌对象
        game_config: 游戏配置

    Returns:
        提供的经验
    """
    src_detail = get_hero_detail(src, game_config)
    dst_detail = get_hero_detail(dst, game_config)

    hero_up_config = game_config['hero']
    exp_config = hero_up_config[src['level']]['detail']
    add_exp = exp_config[src_detail['type']]['eaten']

    if src_detail['job'] == dst_detail['job']:
        add_exp *= constants.HERO_MERGE_SAME_JOB_EXP_ADDITION

    return add_exp


def hero_merge(dst, merges, game_config, merge_type):
    """根据材料卡牌计算合成后卡牌的数据

    合成主要是卡牌等级，成长，技能等相关数据

    Args:
        dest: 目标卡牌
        merges: 要合成的材料
        game_config: 游戏配置
        merge_type: 合成成功类型

    Returns:
        合成后的数据信息
        {
           'hero' // 卡牌数据
           'evolutions' // 演化过程数据，包括基础数据的更改
           'type' // 合成的类型
        }
    """
    obj = dict(dst)
    add_exp = 0
    evolutions = []

    for good in merges:
        add_exp += calc_merge_exp(good, obj, game_config)

    obj['exp'] += calc_merge_value(add_exp, merge_type)

    obj = hero_upgrade(obj, game_config, evolutions)

    return {
        'hero': obj,
        'evolutions': evolutions,
        'type': merge_type,
    }


def hero2fighter(obj, game_config):
    """把一个卡牌对象转换成战斗所需的战斗对象

    Args:
        obj: 卡牌对象
        game_config: 游戏配置

    Returns:
        战斗所需的战斗对象
    """
    if not obj:
        return None

    detail = get_hero_detail(obj, game_config)

    return format_fighter(obj, detail, game_config)


def monster2fighter(monster_id, game_config):
    """根据monster_id转换成战斗时所需的战斗对象

    Args:
        monster_id: 关卡怪物id
        game_config: 游戏配置

    Returns:
        战斗所需的战斗对象
    """
    if not monster_id:
        return None

    obj = detail = game_config['monster'][monster_id]
    obj['cfg_id'] = monster_id

    return format_fighter(obj, detail, game_config)


def format_fighter(obj, detail, game_config):
    """统一格式化战斗对象信息, 生成战斗成员用

    Args:
        obj: 卡牌对象或怪物配置
        detail: 卡牌配置或取物配置
        game_config: 游戏配置

    Returns:
        战斗使用的数据格式
    """
    skill_data = game_config['skill_data']

    fighter = {
        'cfg_id': obj['cfg_id'],
        'level': obj['level'],
        'hp': obj['hp'],
        'natk': obj['natk'],
        'ndef': obj['ndef'],
        'matk': obj['matk'],
        'mdef': obj['mdef'],
        'job': detail['job'],
        'ai': detail['ai'],
        'hit': detail['hit'],
        'dodge': detail['dodge'],
        'storm_hit': detail['storm_hit'],
        'holdout_storm': detail['holdout_storm'],
        'atk_cd': detail['atk_cd'],
        'speed': detail['speed'][0],
        'speed_round': detail['speed'][1],
        'width': detail['size'][0],
        'high': detail['size'][1],
        'res': detail['res'],
        'rage': 0,
        'release_anger': detail['release_anger'],
        'enmity': game_config['battle_enmity'],
        'normal_skill': skill_data.get(detail['skill']['normal']),
        'anger_skill': skill_data.get(detail['skill']['rage']),
        'destiny_skill': None,
        'bf_init': format_data(obj, detail, game_config),
    }

    return fighter


def format_hero(obj, game_config, **kwargs):
    """根据heros配置转换成战斗前所需的战斗信息

    Args:
        obj: 卡牌对象
        game_config: 游戏配置
        kwargs: 动态参数

    Returns:
        战斗所需的战斗对象
    """
    detail = get_hero_detail(obj, game_config)

    data = format_data(obj, detail, game_config)
    data = subjoin_skill_info(data, detail, game_config)
    data.update(kwargs)

    return data


def format_monster(monster_id, game_config, **kwargs):
    """根据monster配置转换成战斗前所需的战斗对象

    Args:
        monster_id: 关卡怪物id
        game_config: 游戏配置

    Returns:
        战斗所需的战斗对象
    """
    obj = detail = game_config['monster'][monster_id]
    obj['cfg_id'] = monster_id

    data = format_data(obj, detail, game_config)
    data = subjoin_skill_info(data, detail, game_config)
    data.update(kwargs)

    return data


def format_data(obj, detail, game_config):
    """统一格式化卡牌或怪物信息

    Args:
        obj: 卡牌对象或怪物对象
        detail: 卡牌配置或怪物配置
        game_config: 游戏配置

    Returns:
        格式化后的信息
    """
    data = {
        'cfg_id': obj['cfg_id'],
        'hp': obj['hp'],
        'level': obj['level'],
        'natk': obj['natk'],
        'ndef': obj['ndef'],
        'matk': obj['matk'],
        'mdef': obj['mdef'],
        'name': detail['name'],
        'icon': detail['icon'],
        'image': detail['image'],
      }

    return data


def subjoin_skill_info(obj, detail, game_config):
    """在卡牌对象或怪物对象中添加技能信息的展示

    Args:
        obj: 卡牌对象或怪物对象
        detail: 对象的详细配置
        game_config: 游戏配置，包含技能配置

    Returns:
        添加技能信息后的对象
    """
    skill_data = game_config['skill_data']
    obj['skill'] = {}

    for skill_type, skill_id in detail['skill'].iteritems():
        if skill_id:
            skill_config = skill_data[skill_id]

            obj['skill'][skill_type] = {
                    'cfg_id': skill_id,
                    'icon': skill_config['icon'],
                    'name': skill_config['name'],
                    'story': skill_config['desc'],
                }

    return obj


def subjoin_destiny_info(obj, detail, game_config, cmp_sort=False):
    """在卡牌对象中添加命运信息的展示

    Args:
        obj: 卡牌对象
        detail: 对象的详细配置
        game_config: 游戏配置，包含命运配置

    Returns:
        添加命运信息后的对象
    """
    destinys = game_config['destinys']
    obj['destiny'] = []

    for destiny_id in detail['destiny']:
        if destiny_id:
            config = destinys[destiny_id]
            obj['destiny'].append({
                    'cfg_id': destiny_id,
                    'name': config['name'],
                    'story': config['story'],
                    'icon': config['icon'],
                    'effect': cmp_sort and cmp_sort(config),
                    })
        else:
            obj['destiny'].append(None)

    return obj


def hero_evolution(hero_cfg_id, game_config, **kwargs):
    """卡牌进化

    生成卡牌进化后的卡牌对象

    Args:
       hero_cfg_id: 卡牌配置id
       game_config: 游戏配置
       kwargs: 动态参数

    Returns:
       卡牌对象
    """
    evolution = game_config['hero_evolution'][hero_cfg_id]

    obj = hero_birth(evolution['dest'], game_config, **kwargs)

    return obj


def hero_sign(obj, game_config, sign_key="%(hp)s.%(natk)s.%(ndef)s.%(matk)s.%(mdef)s"):
    """创建生长签名

    根据生长类型, 初始数值创建签名，当配置更改时可以自动更新

    Args:
       obj: 卡牌信息
       game_config: 游戏全局配置
       sign_key: 签名数据格式key

    Returns:
       卡牌数值签名
    """
    detail = get_hero_detail(obj, game_config)

    obj = hashlib.md5()
    obj.update(sign_key % detail['init'])
    obj.update(sign_key % detail['incr'])

    return obj.hexdigest()


def hero_reborn(obj, game_config):
    """卡牌重生

    Args:
       obj: 卡牌对象
       game_config: 游戏全局配置

    Returns:
       卡牌数据
    """
    kwargs = {
        'level_up': obj['level_up'],
        'level': obj['level'],
        'lock': obj['lock'],
        'exp': obj['exp'],
    }

    return hero_birth(obj['cfg_id'], game_config, **kwargs)


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

