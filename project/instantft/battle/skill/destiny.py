# coding: utf-8
import numpy

ATK_TIMES = 2
UNATK_TIMES = 3
HP_LT = 4
RAGE_LT = 5
TEAMMATE_DEAD_GT = 6
TEAMMATE_DEAD_LT = 7
STRENGTH_DEAD_GT = 8
STRENGTH_DEAD_LT = 9
OPPONENT_DEAD_GT = 10
OPPONENT_DEAD_LT = 11
OPPONENT_EXISTS_JOB = 12
SELF_ATTR_GT = 13 
SELF_ATTR_LT = 14
STORM_TIMES = 15
DODGE_TIMES = 16
UNSTORM_TIMES = 17

# 2.每攻击N下
# 3.被攻击N
# 4.血量少于%
# 5.怒气高于N
# 6.本队死亡数量大于N
# 7.本队死亡数量小于N
# 8.本队与敌方死亡数量大于N
# 9.本队与敌方死亡数量小于N
# 10.敌方死亡数量大于N
# 11.敌方死亡数量小于N
# 12.敌方存在X职业
# 13.自身X属性高于N
# 14.自身X属性小于N

# 15.暴击N次
# 16.闪避N次
# 17.被暴击N次

def cycle_atk_trigger(agent, be, value):
    """
    """

    return not be.counters[agent.id][ATK_TIMES] % value

def cycle_unatk_trigger(agent, be, value):
    """
    """

    return not be.counters[agent.id][UNATK_TIMES] % value

def teammate_dead_gt(agent, be, value):
    """
    """

    return len(be.deads[agent.gid]) > value

def hp_lt(agent, be, value):
    """
    """

    return agent.value < value

def rage_lt(agent, be, value):
    """
    """

    return agent.anger < value

def teammate_dead_lt(agent, be, value):
    """
    """

    return len(be.deads[agent.gid]) < value

def strength_dead_gt(agent, be, value):
    """
    """

    a, b = map(len, be.deads)
    return numpy.abs(a - b) > value

def strength_dead_lt(agent, be, value):
    """
    """

    a, b = map(len, be.deads)
    return numpy.abs(a - b) > value

def opponent_dead_gt(agent, be, value):
    """
    """
    
    opp_gid = be.OPP_GROUPS[agent.gid]

    return len(be.deads[opp_gid]) > value

def opponent_dead_lt(agent, be, value):
    """
    """
    
    opp_gid = be.OPP_GROUPS[agent.gid]

    return len(be.deads[opp_gid]) < value

def opponent_exists_job(agent, be, value):
    """
    """

    opp_gid = be.OPP_GROUPS[agent.gid]

    return value in be.actors[opp_gid]

def self_attr_gt(agent, be, value):
    return False

def self_attr_lt(agent, be, value):
    return False

def storm_times(agent, be, value):
    """
    """

    return not be.counters[agent.id][STORM_TIMES] % value

def dodge_times(agent, be, value):
    """
    """
    return not be.counters[agent.id][DODGE_TIMES] % value

def unstorm_times(agent, be, value):
    """
    """
    return not be.counters[agent.id][UNSTORM_TIMES] % value

matchs = {
    ATK_TIMES: cycle_atk_trigger,
    UNATK_TIMES: cycle_unatk_trigger,
    HP_LT: hp_lt,
    RAGE_LT: rage_lt,
    TEAMMATE_DEAD_GT: teammate_dead_gt,
    TEAMMATE_DEAD_LT: teammate_dead_lt,
    STRENGTH_DEAD_GT: strength_dead_gt,
    STRENGTH_DEAD_LT: strength_dead_lt,
    OPPONENT_DEAD_GT: opponent_dead_gt,
    OPPONENT_DEAD_LT: opponent_dead_lt,
    OPPONENT_EXISTS_JOB: opponent_exists_job,
    SELF_ATTR_GT: self_attr_gt,
    SELF_ATTR_LT: self_attr_lt,
    STORM_TIMES: storm_times,
    DODGE_TIMES: dodge_times,
    UNSTORM_TIMES: unstorm_times,
}

def destiny_skill_match(be, self):
    """
    """

    if not self.dskill:
        return False

    return matchs[dskill.trigger_type](agent, be, dskill.trigger_value)
