# coding:utf-8
from base import BattleAgent
from base import RANGER_AGENT

class RangerAgent(BattleAgent):
    @property
    def actor(self):
        return RANGER_AGENT
