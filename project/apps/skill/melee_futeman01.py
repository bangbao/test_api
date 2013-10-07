# coding: utf-8 from instantft.battle import skill as battle_skill
IS_ANGER_SKILL = True
SKILL_ATK_DISTANCE = battle_skill.atk_distance(2, 2)
SKILL_TOTAL_FRAME = 6
SKILL_ADD_ANGER = 18
SKILL_COST_ANGER = battle_skill.COST_ALL_ANGER

target_match = battle_skill.opp_match.shift_by_hate()target_type = battle_skill.opp_match.agent_targetdisaster = battle_skill.disaster.attack(4)hit_targets = battle_skill.effect_range.hit_allhit_range = battle_skill.effect_range.target_only
def skill(agent, target, be):    from instantft.battle import skill as battle_skill     return {         battle_skill.NORMAL_ATTACK: [agent.nattack*1.2],    }
