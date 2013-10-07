# coding: utf-8
from base import BattleAgent
from base import COMMON_AGENT

class CommentAgent(BattleAgent):
    @property
    def actor(self):
        return COMMON_AGENT
