# coding:utf-8
# ������

from instantft.battle import skill as battle_skill

IS_ANGER_SKILL = False
SKILL_ATK_DISTANCE = battle_skill.atk_distance(8, 8)
SKILL_TOTAL_FRAME = [11, 11]
SKILL_ADD_ANGER = 18
SKILL_COST_ANGER = battle_skill.COST_ALL_ANGER
SKILL_TARGET = battle_skill.TEAMMATE
SKILL_ACTIONS = [0, 1, 0, 1, 0, 1, 0, 1]

target_match = battle_skill.opp_match.min_hp_of_team
target_type = battle_skill.opp_match.agent_target
disaster = battle_skill.disaster.attack(2)
hit_targets = battle_skill.effect_range.hit_all
hit_range = battle_skill.effect_range.target_only

def skill(agent, target, be):
    """
    """

    from instantft.battle import skill as battle_skill

    return {
        battle_skill.CURE_ATTACK: [agent.mattack * 0.2],
    }
