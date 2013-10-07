# coding: utf-8

from base import BaseAction

class MoveAction(BaseAction):

    FIELD_NAME = 'move'
    
    def __init__(self, agent, line, be, frames, ai_frames, goal_pos):
        self.agent = agent
        self.line = line
        self.be = be
        self.cost_frames = frames
        self.ai_frames = ai_frames
        self.goal_pos = goal_pos

    def frames(self):
        """
        """
        if self.line:
            self.be.places[self.agent.id] = self.line[0]
            yield self.agent.id, reversed(self.line)

    def frame_update(self, ai, frame, data, agent_id):
        """
           move: [[12, 13], 5]
        """

        if self.be.frames > self.ai_frames:
            obj = {self.FIELD_NAME: [[], 0]}
            obj = ai.frames[self.ai_frames].setdefault(agent_id, obj)
            if self.FIELD_NAME in obj:
                obj[self.FIELD_NAME][0].extend(data)
                obj[self.FIELD_NAME][1] = self.cost_frames
            else:
                obj[self.FIELD_NAME] = [list(data), self.cost_frames]
        else:
            frame[agent_id][self.FIELD_NAME] = [list(data), self.cost_frames]


    def get_target_pos(self):
        """
        """

        return self.goal_pos

