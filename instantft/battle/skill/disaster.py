# coding: utf-8

from instantft.ai.helper.disaster import simple
from instantft.ai.helper.disaster import generate
from instantft.ai.helper.opp import simple as helper_simple
from instantft.ai.action import simple as action_simple
import attribute

def bulle(speed, rounds):
    """
    """

    def wrapper(atk):
        """
        """

        return simple.BulletDisaster(atk, speed, rounds)

    return wrapper


def attack(frames=1):
    """
    """

    def wrapper(atk):
        return simple.AttackDisaster(atk, frames)

    return wrapper

def revival(atk):
    """
    """

    return simple.RevivalDisaster(atk)

def summon_bulle(speed, rounds, life_frames):
    """
    """

    def wrapper(atk):
        return generate.SummonDisaster(atk, speed, rounds, life_frames)

    return wrapper

def hidetranshide(speed, rounds, high):
    def wrapper(atk):
        actions = [
            helper_simple.StubbornHelper(action_simple.HideAction, 
                                         atk.agent, atk.be),
            helper_simple.OnceHelper(action_simple.AppearAction, 
                                     atk.agent, atk.be)
        ]

        return generate.TransformDisaster(atk, speed, rounds, high, actions)

    return wrapper

def kick_target(be, agent, target):
    pos = be.places[target.id]
    target_pos = be.places[target.id]
    kick_pos = target_pos
    distances = be.bf.xslice(pos)
    highs = be.bf.yslice(pos)
    blocks = be.get_blocks()
    step = 1
    length = distances[1]

    if be.bf.face_to(pos, target_pos):
        step = -1
        length = distances[0]

    for i in xrange(length):
        kick_pos += step

        if kick_pos not in blocks:
            return target_pos, ((target, kick_pos),)

def blew_add_range(rage, frames=1):
    add_range = attribute.add_range(rage)

    def wrapper(atk):
        return generate.Suicide(atk, add_range)

    return wrapper
