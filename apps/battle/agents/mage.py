# coding: utf-8
from base import BattleAgent
from base import MAGE_AGENT

class MageAgent(BattleAgent):
    """ 法师战场对象
    """

    @property
    def actor(self):
        return MAGE_AGENT
