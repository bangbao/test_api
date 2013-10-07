# coding: utf-8
from base import BattleAgent
from base import CATAPULT_AGENT

class CatapultAgent(BattleAgent):
    @property
    def actor(self):
        return CATAPULT_AGENT
