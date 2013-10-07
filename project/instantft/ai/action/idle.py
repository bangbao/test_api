# coding: utf-8

from base import BaseAction

class IdleAction(BaseAction):
    FIELD_NAME = 'idle'

    def __init__(self, agent, be):
        self.agent = agent
        self.be = be

    def frames(self):
        """
        """

        yield self.agent.id, {self.FIELD_NAME: None}
