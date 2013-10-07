# coding: utf-8

from instantft.ai.action.move import MoveAction
from instantft.ai.action.attack import AttackAction
from instantft.ai.action.dead import DeadAction
from instantft.ai.action.idle import IdleAction
from instantft.ai.action.breathe import BreatheAction
from base import BaseManipulate

class Butcher(BaseManipulate):
    """ 屠夫操作模式
    """

    def __init__(self, agent, opp, be):
        self.agent = agent
        self.opp = opp
        self.be = be

    def frame(self):
        """ 当未完成动作时逐帧返回数据
        """

        line = self.be.astar(self.agent.id, self.opp.id)

        if not self.be.atk2get(self.agent, self.opp, line):
            if line:
                obj = MoveAction(self.agent, line[0: self.agent.rate], self.be)
            else:
                return IdleAction(self.agent, self.be)
        else:
            obj = AttackAction(self.agent, self.opp, self.be)

        return obj

    def finish(self):
        """ 判断是否屠杀完一个目标
        """

        return not (self.agent.alive() and self.opp.alive() and self.tempt())

    def tempt(self):
        """ 是否被新的目标引诱

        """

        opphelper = self.be.opphelper_loader(self.agent)
        opps = self.be.get_opps(self.agent.id)
        opp_id = opphelper.scan(opps)

        return opp_id != self.opp.id

class Corpse(BaseManipulate):
    def __init__(self, agent, be, breathe=1):
        self.agent = agent
        self.be = be
        self.breathe = breathe

    def frame(self):
        breathe = self.breathe
        self.breathe -= 1
        
        if not breathe:
            return DeadAction(self.agent, self.be)

        return BreatheAction(self.agent, self.be)

    def finish(self):
        return self.agent.alive()

class Idler(BaseManipulate):
    def __init__(self, agent, be):
        self.agent = agent
        self.be = be

    def frame(self):
        return IdleAction(self.agent, self.be)
    
    def finish(self):
        return True
