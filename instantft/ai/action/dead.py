# coding: utf-8

from base import BaseAction

class DeadAction(BaseAction):
    FIELD_NAME = 'dead'

    def __init__(self, agent, be):
        self.agent = agent
        self.be = be

    def frames(self):
        """
        """

        yield self.agent.id, {self.FIELD_NAME: None}
