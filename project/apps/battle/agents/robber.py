# coding: utf-8
from base import BattleAgent
from base import ROBBER_AGENT

class RobberAgent(BattleAgent):
    @property
    def actor(self):
        return ROBBER_AGENT
