# coding: utf-8
from base import BattleAgent
from base import WARRIOR_AGENT

class WarriorAgent(BattleAgent):

    @property
    def actor(self):
        return WARRIOR_AGENT
