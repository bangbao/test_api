# coding: utf-8

from base import BaseAction

class BreatheAction(BaseAction):

    def __init__(self, agent, be):
        self.agent = agent
        self.be = be

    def frames(self):
        if False:
            yield
