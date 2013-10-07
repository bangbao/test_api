# coding:utf-8

from instantft.battle import skill as battle_skill

IS_ANGER_SKILL = True
SKILL_ATK_DISTANCE = battle_skill.atk_distance(6, 6)
SKILL_TOTAL_FRAME = 10
SKILL_ADD_ANGER = 30
SKILL_COST_ANGER = battle_skill.COST_ALL_ANGER
SKILL_TARGET = battle_skill.TEAMMATE

target_match = battle_skill.opp_match.min_hp_of_team
target_type = battle_skill.opp_match.agent_target
disaster = battle_skill.disaster.attack(5)
hit_targets = battle_skill.effect_range.hit_all
hit_range = battle_skill.effect_range.all_teammate

def skill(agent, target, be):
    """
    """

    from instantft.battle import skill as battle_skill

    return {
        battle_skill.CURE_ATTACK: [agent.mattack * 0.1],
    }
