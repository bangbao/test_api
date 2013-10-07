# coding: utf-8
from base import BattleAgent
from base import KNIGHT_AGENT

class KnightAgent(BattleAgent):
    @property
    def actor(self):
        return KNIGHT_AGENT
