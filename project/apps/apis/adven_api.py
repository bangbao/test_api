# coding: utf-8

from apps import battle as battle_app


def area_map(env):
    """获取某个区域地图信息，包含这个区域各个章节的信息

    Args:
        area: 区域id

    Returns:
        地图信息
    """
    area = env.params['area']

    user = env.user
    game_app = env.import_app('game')
    adven_app = env.import_app('adven')

    return {
        'map': adven_app.chapter_map_config[area],
        'world_map': adven_app.world_map_config,
        'adven': adven_app.get_adven_record(user),
        'game': game_app.get_game_data(user),
        'area': area,
    }


def chapter_map(env):
    """获取某个章节地图信息，包含这个章节各个关卡的信息

    Args:
        area: 区域id
        chapter: 章节id

    Returns:
        地图信息
    """
    area = env.params['area']
    chapter = env.params['chapter']
    stage_map_config = env.game_config['stage_map']

    game_app = env.import_app('game')
    adven_app = env.import_app('adven')

    return {
        'map': stage_map_config[chapter],
        'area': area,
        'chapter': chapter,
        'adven': adven_app.get_adven_record(env.user),
        'game': game_app.get_game_data(env.user),
    }


def stage(env):
    """处理攻打关卡前的双方战斗阵容，地图数据

    Args:
       chapter: 攻打关卡所在的章节
       stage: 攻打的关卡id

    Returns:
        战斗阵容及地图数据
    """
    area = env.params['area']
    chapter = env.params['chapter']
    stage_id = env.params['stage']
    select = env.params['select']
    game_config = env.game_config

    hero_app = env.import_app('hero')
    team = env.params['user_team']
    stage_config = game_config['stages'][stage_id]
    fight_id = stage_config[select]['fight_id']
    monsters = game_config['map_fight'][fight_id]['monster']

    attacker = hero_app.hero_lined_up(env.user, team)
    defender = hero_app.monster_lined_up(env, monsters)

    return {
        'attacker': attacker,
        'defender': defender,
        'map': {
            'icon': '1.png',
            'area': area,
            'stage': stage_id,
            'chapter': chapter,
            'name': stage_config['name'],
            'loot': {
                'heros': [],
                'exp': stage_config['loot']['exp'],
                'gold': stage_config['loot']['gold'],
            },
        },
    }


def fight(env):
    """攻打关卡的战斗过程数据，掉落数据

    Args:
       chapter: 攻打关卡所在的章节
       stage: 攻打的关卡id
       members: 当前编队

    Returns:
        战斗数据及掉落数据
    """
    user = env.user
    area = env.params['area']
    chapter = env.params['chapter']
    stage_id = env.params['stage']
    select = env.params['select']
    team = env.params['members']
    game_config = env.game_config

    stage_detail = game_config['stages'][stage_id]
    fight_id = stage_detail[select]['fight_id']
    monsters = game_config['map_fight'][fight_id]['monster']
    map_id = game_config['map_fight'][fight_id]['map_id']
    map_detail = game_config['map_info'][map_id]

    game_app = env.import_app('game')
    hero_app = env.import_app('hero')
    adven_app = env.import_app('adven')

    attacker = hero_app.hero2formation(user, team)
    defender = hero_app.monster2formation(env, monsters)

    chapter_data = user.adven.readven.get(chapter)
    if stage_detail['script'] and not (chapter_data and chapter_data['select']):
        battle_ai = battle_app.battle(env, map_detail, attacker, defender,
                                      pot_name=stage_detail['script'])
    else:
        battle_ai = battle_app.battle(env, map_detail, attacker, defender)

    battle_data = battle_ai.record()

    battle_grade = adven_app.battle_evaluation(user, battle_data['fight']['win'],
                                               battle_data['fight']['falls'])
    evolutions, loot_data = adven_app.chapter_over(user, chapter, stage_id, select,
                                                   win=battle_data['fight']['win'],
                                                   grade=battle_grade)

    hero_app.team_put(user, team)
    env.user.save_all()

    return {
        'battle': battle_data,
        'opening': battle_ai.opening,
        'takeabow': battle_ai.takeabow,
        'loot': loot_data,
        'levelup': evolutions,
        'area': area,
        'stage': stage_id,
        'chapter': chapter,
        'game': game_app.get_game_data(user),
        #'fighter_info': {
        #    'attacker_list': env.attacker_list,
        #    'defender_list': env.defender_list,
        #}
    }

