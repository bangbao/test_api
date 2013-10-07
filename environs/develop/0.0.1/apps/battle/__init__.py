# coding: utf-8

from instantft.ai import AI
from instantft.battle.field import BattleField
from instantft.battle.agent import Agent
from apps import skill as skill_app
from apps import battle as battle_app

skill_data = {1: {'name': u'\u706b\u7403\u672f', 'effective': 'fireball', 'effect': 'bomb', 'icon': 'skill_1.jpg', 'desc': u'\u55f7\u55f7\u7684\u706b\u7403\uff0c\u98da\u4f60\u4e00\u8138\uff0c\u9020\u6210100%\u7684\u6cd5\u672f\u4f24\u5bb3'}, 2: {'name': u'\u5927\u706b\u7403\u672f', 'effective': 'bfireball', 'effect': '', 'icon': 'skill_2.jpg', 'desc': u'\u55f7\u55f7\u7684\u5927\u706b\u7403\uff0c\u5e05\u5446\u4e86\uff01\u9020\u6210110%\u7684\u6cd5\u672f\u4f24\u5bb3\uff0c\u8fd8\u7ed9\u5168\u4f53\u52a0\u4e2anb buff'}, 3: {'name': u'\u5288\u780d', 'effective': 'hackchop', 'effect': 'null', 'icon': 'skill_3.jpg', 'desc': u'\u5f53\u5934\u4e00\u5200\uff0c\u6740\u50f5\u5c38\u6548\u679c\u6700\u597d\uff01\u9020\u6210100%\u7684\u7269\u7406\u4f24\u5bb3\uff0c\u8fd8\u7ed9\u81ea\u5df1\u52a0\u66b4\u51fb\u5462\uff01'}, 4: {'name': u'\u7a7f\u523a', 'effective': 'puncture', 'effect': '', 'icon': 'skill_4.jpg', 'desc': u'\u4e00\u4e2a\u7a7f\u523a\u5237\u5237\u7684\u98d9\u8840\uff0c\u5168\u8dea\uff01\u7ed9\u81ea\u5df1\u52a0\u8840\u7ed9\u654c\u65b9\u51cf\u8840\uff0c\u7279\u522b\u597d\u7528'}}

mapinfo = {'defend': [11194, 15534, 19834, 22734, 25594, 29934, 34234], 'focus': {'attack': {'y': 0, 'x': 0}, 'defend': {'y': 0, 'x': 480}}, 'attack': [10984, 15284, 19624, 22484, 25384, 29684, 34024], 'max_pos': 36863, 'pixel': 5, 'size': (288, 128)}

#mapinfo = {'defend': [57, 88, 117, 148, 177, 208, 237], 'focus': {'attack': {'y': 0, 'x': 0}, 'defend': {'y': 0, 'x': 15}}, 'attack': [32, 61, 92, 121, 152, 211, 242], 'max_pos': 599, 'pixel': 32, 'size': (30, 20)}

attacker = [battle_app.create_agent(battle_app.WarriorAgent,
                                    hp=801, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[3], 
                                    anger_skill=skill_data[4],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5),
            battle_app.create_agent(battle_app.WarriorAgent,
                                    hp=802, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[3], 
                                    anger_skill=skill_data[4],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5),
            battle_app.create_agent(battle_app.WarriorAgent,
                                    hp=803, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[3], 
                                    anger_skill=skill_data[4],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5),
            battle_app.create_agent(battle_app.MageAgent,
                                    hp=804, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[1], 
                                    anger_skill=skill_data[2],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5),
            battle_app.create_agent(battle_app.MageAgent,
                                    hp=805, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[1], 
                                    anger_skill=skill_data[2],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5)
]

defender = [battle_app.create_agent(battle_app.WarriorAgent,
                                    hp=801, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[3], 
                                    anger_skill=skill_data[4],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5),
            battle_app.create_agent(battle_app.WarriorAgent,
                                    hp=802, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[3], 
                                    anger_skill=skill_data[4],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5),
            battle_app.create_agent(battle_app.WarriorAgent,
                                    hp=803, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[3], 
                                    anger_skill=skill_data[4],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5),
            battle_app.create_agent(battle_app.MageAgent,
                                    hp=804, atk_range=3, atk_cd=[3, 10],
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[1], 
                                    anger_skill=skill_data[2],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5),
            battle_app.create_agent(battle_app.MageAgent,
                                    hp=805, atk_range=3, atk_cd=[3, 10], 
                                    normal_atk=100, magic_atk=10,
                                    normal_defend=10, magic_defend=1,
                                    normal_skill=skill_data[1], 
                                    anger_skill=skill_data[2],
                                    storm_hit=30, speed=11, speed_round=15,
                                    width=5, high=5)
]

def battle(env):
    """

    """

    bf = BattleField(mapinfo, attacker, defender)
    ai = AI(bf, skill_app)

    while not ai.over():
        ai.frame()

    return ai.record()
