# coding: utf-8
from instantft.ai.manipulate.simple import Punisher
from instantft.ai.manipulate.simple import Corpse
from instantft.ai.manipulate.simple import Idler


class EnmitiyHelper(object):
    def __init__(self, agent, be):
        self.agent = agent
        self.be = be
        
    def enmity(self, x):
        """
        """

        return self.be.enmities[self.agent.id][x]

    def scan(self, opps):
        """
        """

        return max(opps, key=self.enmity)

    def action(self, opp):
        """
        """

        if self.agent.alive():
            if opp in self.be.agents:
                opper = self.be.agents[opp]
                return Punisher(self.agent, opp, self.be)
            else:
                return Idler(self.agent, self.be)
        else:
            return Corpse(self.agent, self.be)
