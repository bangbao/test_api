# coding: utf-8

from base import BaseAction

class KickAction(BaseAction):
    FIELD_NAME = 'kicked'

    def __init__(self, agent, be, kick_pos):
        self.agent = agent
        self.be = be
        self.kick_pos = kick_pos

    def frames(self):
        """
        """
        self.be.places[self.agent.id] = self.kick_pos
        yield self.agent.id, {self.FIELD_NAME: self.kick_pos}
