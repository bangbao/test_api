# coding: utf-8
from instantft.ai.action.attack import AttackAction
from instantft.ai.action.idle import IdleAction
from instantft.ai.action.move import MoveAction
from instantft.ai.action.dead import DeadAction
from instantft.ai.action.kick import KickAction
from instantft.ai.action.birth import BirthAction
from instantft.ai.action.breathe import BreatheAction
from instantft.battle.timer import MoveRound
from base import BaseHelper
import numpy

class StubbornHelper(BaseHelper):
    """ 只返回单独的action

    保持一个状态时使用
    """

    def __init__(self, cls, *args, **kwargs):
        self.action = cls(*args, **kwargs)

    def frame(self):
        return self.action

    def finish(self):
        return False

class OnceHelper(BaseHelper):
    """ 只生效一次的操作

    调用一次后自动结束
    """

    def __init__(self, cls, *args, **kwargs):
        self.action = cls(*args, **kwargs)
        self.counter = 0

    def frame(self):
        self.counter += 1
        return self.action

    def finish(self):
        return bool(self.counter)

class CorpseHelper(BaseHelper):
    """ 僵尸操作
    """

    def __init__(self, agent, be, breathe=1):
        self.agent = agent
        self.be = be
        self.breathe = breathe
        self.revival = False

    def frame(self):
        """
        """

        breathe = self.breathe
        self.breathe -= 1
        
        if not breathe:
            self.be.deads[self.agent.gid].add(self.agent.id)
            return DeadAction(self.agent, self.be)
        elif self.agent.alive():
            self.revival = True
            self.be.deads[self.agent.gid].remove(self.agent.id)
            self.be.set_agent_pos(self.agent, self.be.places[self.agent.id])
            return BirthAction(self.agent, self.be)

        return BreatheAction(self.agent, self.be)

    def finish(self):
        """
        """

        return self.revival

class KickerHelper(BaseHelper):
    """
    """

    def __init__(self, agent, be, kick_pos):
        """
        """

        self.agent = agent
        self.be = be
        self.kick_pos = kick_pos
        self.kicked = False
    
    def frame(self):
        self.kicked = True

        return KickAction(self.agent, self.be, self.kick_pos)

    def finish(self):
        """
        """

        return self.kicked

class BirthHelper(BaseHelper):
    """
    """

    def __init__(self, agent, be):
        self.agent = agent
        self.be = be
        self.birthed = False

    def frame(self):
        """
        """

        self.birthed = True

        return BirthAction(self.agent, self.be)
        
    def finish(self):
        return self.birthed

class ChaseHelper(BaseHelper):
    """ 追逐操作
    
    当前战斗单位不能直接攻击到目标时，会按照最佳的线路
    进行追逐
    """

    def __init__(self, agent, opper, be, skill):
        self.agent = agent
        self.be = be
        self.opper = opper
        self.ai_frames = be.frames
        self.skill = skill
        self.counter = 0
        self.locus = []

    def frame(self):
        """
        """

        line = []
        moves = self.agent.move.move()
        goal_pos = self.be.places[self.opper.id]

        if moves:
            line = self.be.goal_astar(self.agent.id, goal_pos, moves, 
                                      self.locus)

            self.locus.extend(line)

        self.counter += self.agent.move.moved(line, moves)

        return MoveAction(self.agent, line, self.be, self.counter,
                          self.ai_frames, goal_pos)

    def target_changes(self):
        """
        """
        
        if not self.be.has_new_fight(self.ai_frames):
            return False

        if self.agent.can_magic_attack():
            self.skill = self.be.skill_app.get_skill(self.agent.mskill)
        else:
            self.skill = self.be.skill_app.get_skill(self.agent.nskill)

        opper = self.skill.target_match(self.agent, self.be)

        return opper and opper.id != self.opper.id

    def can_attack_opp(self):
        """ 判断当前是否可以攻击到目标

        由于战斗单位周围的占位是可穿越但不可停留的，所以在可以攻击到
        目标的状态时，必须要判断当前位置是否可以停留。
        如果不可以，会强制穿越到一个可以停留的地方攻击目标
        """

        return self.be.atk2get(self.agent, self.opper, self.skill)

    def on_finish(self):
        self.agent.move.init()

        return True

    def finish(self):
        """
        """

        return not self.agent.alive() or \
            not self.opper.alive() or \
            self.can_attack_opp() or \
            self.target_changes()

class AttackHelper(BaseHelper):
    """ 攻击操作

    对攻击目标产生攻击
    """

    def __init__(self, agent, opper, be, skill):
        """
        """

        self.agent = agent
        self.be = be
        self.opper = opper
        self.skill = skill
        self.action = None
        self.attacked = False

    def frame(self):
        """ 攻击动作
        """

        if not self.action:
            self.action = AttackAction(self.agent, self.opper, 
                                       self.be, self.skill)

        return self.action

    def rel(self):
        if not self.attacked:
            self.agent.attacked = self.attacked = True
            self.be.add_disaster(self.action.create_disaster())

    def finish(self):
        """
        """

        return not self.agent.alive() or \
            self.action.finish()
