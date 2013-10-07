# coding: utf-8
from base import BaseAction

class HideAction(BaseAction):
    FIELD_NAME = 'hide'

    def __init__(self, agent, be):
        self.agent = agent
        self.be = be
        self.in_hide = False

    def frames(self):
        """
        """

        if not self.in_hide:
            self.in_hide = True
            yield self.agent.id, {self.FIELD_NAME: None}

class AppearAction(BaseAction):
    FIELD_NAME = 'appear'

    def __init__(self, agent, be):
        self.agent = agent
        self.be = be

    def frames(self):
        """
        """

        yield self.agent.id, {self.FIELD_NAME: self.be.places[self.agent.id]}
