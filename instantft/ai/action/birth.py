# coding: utf-8

from base import BaseAction

class BirthAction(BaseAction):

    FIELD_NAME = 'birth'
    
    def __init__(self, agent, be):
        self.agent = agent
        self.be = be

    def frames(self):
        agent_status = self.be.get_agent_status(self.agent)
        agent_status['pos'] = self.be.places[self.agent.id]

        yield self.agent.id, {self.FIELD_NAME: agent_status}


