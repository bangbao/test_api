# coding: utf-8 from instantft.battle import skill as battle_skill
IS_ANGER_SKILL = False
SKILL_ATK_DISTANCE = SKILL_ATK_DISTANCE = battle_skill.atk_distance(10, 10)
SKILL_TOTAL_FRAME = [12,12]
SKILL_ADD_ANGER = 12
SKILL_COST_ANGER = battle_skill.COST_ALL_ANGER
SKILL_ACTIONS = [0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
target_match = battle_skill.opp_match.shift_by_hate()target_type = battle_skill.opp_match.agent_targetdisaster = battle_skill.disaster.bulle(9, 1)hit_targets = battle_skill.effect_range.hit_allhit_range = battle_skill.effect_range.target_only
def skill(agent, target, be):    from instantft.battle import skill as battle_skill     return {         battle_skill.MAGIC_ATTACK: [agent.nattack*1.3],    }
