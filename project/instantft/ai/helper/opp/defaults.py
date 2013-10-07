# coding: utf-8
"""
Default AI.

When agnet has attack cd, this AI help it action.
"""

from instantft.ai.action.move import MoveAction
from instantft.ai.action.idle import IdleAction
from instantft.battle.timer import MoveRound
from base import BaseHelper

class AssaultHelper(BaseHelper):
    def __init__(self, agent, be, skill):
        """ 突击型战斗角色
        """

        self.agent = agent
        self.skill = skill
        self.be = be
        self.ai_frames = be.frames
        self.counter = 0

    def frame(self):
        """
        """

        return IdleAction(self.agent, self.be)

        # goal_pos = self.be.adjust_atk_pos(self.agent, self.skill)

        # if goal_pos < 0:
        #     return IdleAction(self.agent, self.be)

        # moves = self.agent.move.move()
        # line = []

        # if moves:
        #     line = self.be.goal_astar(self.agent.id, goal_pos, moves)

        # self.counter += self.agent.move.moved(line, moves)

        # return MoveAction(self.agent, line, self.be, self.counter,
        #                   self.ai_frames, goal_pos)

    def finish(self):
        """
        """

        return not self.agent.has_attack_cd()

    def on_finish(self):
        self.agent.move.init()

        return True


class CastHelper(BaseHelper):
    def __init__(self, agent, be, skill):
        """ 远程型
        """

        self.agent = agent
        self.skill = skill
        self.be = be
        self.ai_frames = be.frames
        self.counter = 0

    def frame(self):
        """
        """

        if not self.agent.target or self.agent.id == self.agent.target:
            return IdleAction(self.agent, self.be)

        target = self.be.agents[self.agent.target]
        distance = self.be.touch_distance(self.agent, target, self.skill)
        goal_pos = self.be.trasferta_pos(self.agent, target, distance)

        if not goal_pos:
            return IdleAction(self.agent, self.be)

        moves = self.agent.move.move()
        line = []

        if moves:
            line = self.be.goal_astar(self.agent.id, goal_pos, moves)

        self.counter += self.agent.move.moved(line, moves)

        return MoveAction(self.agent, line, self.be, self.counter,
                          self.ai_frames, goal_pos)

    def finish(self):
        """
        """

        return not self.agent.has_attack_cd()

    def on_finish(self):
        self.agent.move.init()

        return True

class ProtectHelper(BaseHelper):
    def __init__(self, agent, be, skill):
        self.agent = agent
        self.skill = skill
        self.target = be.agents.get(agent.target)
        self.be = be
        self.ai_frames = be.frames
        self.counter = 0
        self.locus = []

    def frame(self):
        """
        """

        if not self.target:
            return IdleAction(self.agent, self.be)

        distance = self.be.touch_distance(self.agent, self.target, self.skill)
        moves = min(distance, self.agent.move.move())
        goal_pos = self.be.places[self.target.id]
        line = []

        if moves:
            line = self.be.goal_astar(self.agent.id, goal_pos, moves, 
                                      self.locus)
            self.locus.extend(line)

        self.counter += self.agent.move.moved(line, moves)

        return MoveAction(self.agent, line, self.be, self.counter,
                          self.ai_frames, goal_pos)

    def finish(self):
        """
        """

        return (self.target and self.target.hurt) or \
            self.be.has_new_fight(self.ai_frames)

    def on_finish(self):
        self.agent.move.init()

        return True

ACTOR_DEFAULT_HELPER = [AssaultHelper, CastHelper, ProtectHelper,
                        AssaultHelper, AssaultHelper, AssaultHelper,
                        AssaultHelper, AssaultHelper]
