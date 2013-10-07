# coding: utf-8
from constants import (B_EFFECT, B_CYCLE, B_VALUE, B_PERCENT, B_DURATIONS)

class BaseEffect(object):
    def __init__(self, agent, buff_config, be):
        """
        """

        self.agent = agent
        self.buff_config = buff_config
        self.be = be
        self.effect = buff_config[B_EFFECT]

        self.init()

    def init(self):
        pass

    def die(self):
        raise NotImplementedError

    def effective(self):
        raise NotImplementedError

    def efocus(self, attrs, hurts):
        return None

    def dfocus(self, attrs, hurts):
        return None

    def get_durations(self):
        return self.buff_config[B_DURATIONS]
