# coding: utf-8
from instantft.battle import skill as battle_skill

IS_ANGER_SKILL = True
SKILL_ATK_DISTANCE = battle_skill.atk_distance(3, 3)
SKILL_TOTAL_FRAME = 8
SKILL_ADD_ANGER = 20
SKILL_COST_ANGER = battle_skill.COST_ALL_ANGER
SKILL_TARGET = battle_skill.BOTH_TARGET

target_match = battle_skill.opp_match.shift_by_hate()
target_type = battle_skill.opp_match.agent_target
hit_targets = battle_skill.effect_range.hit_opponent
hit_range = battle_skill.effect_range.target_land_site(3, 3)
disaster = battle_skill.disaster.attack(4)

def skill(agent, target, skill_config):
    """
    """

    from instantft.battle import skill as battle_skill

    return {
        battle_skill.MAGIC_ATTACK: [agent.mattack * 1.1],
    }
