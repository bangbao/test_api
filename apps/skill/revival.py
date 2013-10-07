# coding: utf-8

from instantft.battle import skill as battle_skill

IS_ANGER_SKILL = True
SKILL_ATK_DISTANCE = battle_skill.atk_distance(10, 10)
SKILL_TOTAL_FRAME = 1
SKILL_ADD_ANGER = 10
SKILL_COST_ANGER = battle_skill.COST_ALL_ANGER
SKILL_TARGET = battle_skill.TEAMMATE

target_match = battle_skill.opp_match.dead_team_member
target_type = battle_skill.opp_match.dead_target
disaster = battle_skill.disaster.revival
hit_targets = battle_skill.effect_range.hit_daed_teammate
hit_range = battle_skill.effect_range.target_only

def skill(agent, target, be):
    """
    """

    from instantft.battle import skill as battle_skill

    return {
        battle_skill.REVIVAL_ATTACK: None,
    }
