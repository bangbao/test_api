# coding: utf-8
import numpy

def target_land_site(xlen, ylen):
    x = xlen / 2
    y = ylen / 2

    def wrapper(agent, target, be):
        """
        """

        return be.in_agent_range(target, x, y)

    return wrapper

def face_to_matrix(x, y):
    def wrapper(agent, target, be):
        pass

    return wrapper

def my_land_site(xlen, ylen):
    x = xlen / 2
    y = ylen / 2

    def wrapper(agent, target, be):
        """
        """

        return be.in_agent_range(agent, x, y)

    return wrapper

def target_only(agent, target, be):
    return [target]

def all_teammate(agent, target, be):
    gdeads = be.deads[agent.gid]
    groups = be.groups[agent.gid]

    for agent_id in groups:
        if not agent_id in gdeads:
            yield be.agents[agent_id]

def all_opponent(agent, target, be):
    opp_gid = be.OPP_GROUPS[agent.gid]
    gdeads = be.deads[opp_gid]
    groups = be.groups[opp_gid]

    for agent_id in groups:
        if not agent_id in gdeads:
            yield be.agents[agent_id]

def offset_matrix(be, current_pos, width, high):
    """
    """
    
    x_ext = int(width / 2)
    y_ext = int(high / 2)

    return be.in_pos_range(current_pos, x_ext, y_ext)

def hit_all(agent, be):
    """
    """

    def wrapper(target):
        return target.alive()

    return wrapper


def hit_teammate(agent, be):
    """
    """

    def wrapper(target):
        """
        """

        return agent.gid == target.gid and target.alive()

    return wrapper

def hit_opponent(agent, be):
    """
    """

    def wrapper(target):
        """
        """

        return agent.gid != target.gid and target.alive()

    return wrapper

def hit_daed_teammate(agent, be):
    """
    """

    def wrapper(target):
        """
        """

        return agent.gid == target.gid and not target.alive()

    return wrapper
