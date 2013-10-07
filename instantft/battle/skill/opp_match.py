# coding: utf-8
from __future__ import division
import itertools

ENLARGE_MIN_HP_COMPARE = 1

class HateMatch(object):
    """
    """

    def __init__(self, shift):
        self.shift = shift

    def __call__(self, agent, be):
        agent_enmities = be.enmities[agent.id]

        if not agent_enmities:
            return None

        def max_key(key):
            if not be.has_agent_dead(key):
                return be.enmities[agent.id][key]

        opp_id = max(agent_enmities, key=max_key)
        opp_hate = be.enmities[agent.id][opp_id]
        target_hate = be.enmities[agent.id].get(agent.target, -1)

        if not agent.target or \
           be.has_agent_dead(agent.target) or \
           (opp_hate * self.shift) > target_hate:
            agent.set_target(opp_id)

        return be.agents[agent.target]

def dead_team_member(agent, be):
    """
    """

    if be.has_agent_dead(agent.target):
        return be.agents[agent.target]

    cmp_agent = lambda x: x == agent.id
    agent_id = agent.id

    for agent_id in itertools.ifilterfalse(cmp_agent,
                                           be.groups[agent.gid]):
        if be.has_agent_dead(agent_id):
            agent.set_target(agent_id)

            return be.agents[agent_id]

    agent.set_target(agent_id)

def min_hp_of_team(agent, be):
    """
    """

    def filter_func(agent_id):
        target = be.agents[agent_id]

        return not (be.has_agent_dead(agent_id) or \
            target.actor == agent.actor)

    target = None
    lifetime = 2

    for opp_id in itertools.ifilter(filter_func, 
                                         be.groups[agent.gid]):
        opper = be.agents[opp_id]
        lifetime_opp = opper.lifetime()

        if lifetime_opp < lifetime:
            target = opper
            lifetime = lifetime_opp

    if not target or agent.lifetime() < lifetime:
        opp_id = agent.id
        target = agent

    agent.set_target(opp_id)

    if target.hurt and target.alive():
        return target

    return None

def shift_by_hate(shift=0.7):
    """
    """

    return HateMatch(shift)


def agent_target(attack):
    """
    """

    return [attack.opper.id,
            attack.be.places[attack.opper.id],
            attack.skill.skill_effect]

def dead_target(attack):
    """
    """

    return [None,
            attack.be.places[attack.opper.id],
            attack.skill.skill_effect]

def lateral_target(attack):
    """
    """

    return [None,
            attack.be.lateral_pos(attack.agent, attack.opper),
            attack.skill.skill_effect]

