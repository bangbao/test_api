# coding: utf-8
from base import BattleAgent
from base import PASTOR_AGENT

class PastorAgent(BattleAgent):
    @property
    def actor(self):
        return PASTOR_AGENT
