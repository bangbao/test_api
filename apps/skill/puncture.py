# coding: utf-8

from instantft.battle import skill as battle_skill

IS_ANGER_SKILL = True
SKILL_ATK_DISTANCE = battle_skill.atk_distance(10, 10)
SKILL_TOTAL_FRAME = 1
SKILL_ADD_ANGER = 10
SKILL_COST_ANGER = battle_skill.COST_ALL_ANGER
SKILL_TARGET = battle_skill.BOTH_TARGET

target_match = battle_skill.opp_match.shift_by_hate()
target_type = battle_skill.opp_match.lateral_target
disaster = battle_skill.disaster.hidetranshide(9, 1, 10)
hit_targets = battle_skill.effect_range.hit_all
hit_range = battle_skill.effect_range.offset_matrix

def skill(agent, target, be):
    """
    """

    from instantft.battle import skill as battle_skill

    if agent.teammate(target):
        return {
            battle_skill.CURE_ATTACK: [agent.mattack * 0.3],
        }
    else:
        return {
            battle_skill.MAGIC_ATTACK: [agent.mattack],
        }
