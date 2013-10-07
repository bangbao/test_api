# coding: utf-8

from instantft.battle import skill as battle_skill

IS_ANGER_SKILL = True
SKILL_ATK_DISTANCE = battle_skill.atk_distance(10, 10)
SKILL_TOTAL_FRAME = 9
SKILL_ADD_ANGER = 30
SKILL_COST_ANGER = battle_skill.COST_ALL_ANGER
SKILL_TARGET = battle_skill.OPPONENT
SKILL_SUMMON_HEROS = [6]
SKILL_SUMMONS = 1

summon_birth = battle_skill.disaster.kick_target
target_match = battle_skill.opp_match.shift_by_hate()
target_type = battle_skill.opp_match.agent_target
disaster = battle_skill.disaster.summon_bulle(7, 1, 30)
hit_targets = battle_skill.effect_range.hit_opponent
hit_range = battle_skill.effect_range.target_land_site(4, 4)

def skill(agent, target, be):
    """
    """

    from instantft.battle import skill as battle_skill

    return {
        battle_skill.MAGIC_ATTACK: [agent.mattack],
    }
