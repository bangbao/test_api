# coding: utf-8

class BaseAction(object):
    FIELD_NAME = None

    def frames(self):
        raise NotImplementedError

    def frame_update(self, ai, frame, data, agent_id):
        frame[agent_id].update(data)

    def get_target_pos(self):
        return -1
