# coding: utf-8
from cheetahes.utils import sys_random as random
from base import BaseAction

class AttackAction(BaseAction):
    NORMAL_ATK = ['attack1', 'attack2']
    RAGE_ATK = 'attack3'

    def __init__(self, agent, opper, be, skill):
        self.agent = agent
        self.opper = opper
        self.be = be
        self.skill = skill
        self.attacked = False
        self.target_pos = None

        if not self.skill.IS_ANGER_SKILL:
            field_key = random.choice(skill.SKILL_ACTIONS)
            self.field_name = self.NORMAL_ATK[field_key]
            self.total_frame = skill.SKILL_TOTAL_FRAME[field_key]
        else:
            self.field_name = self.RAGE_ATK
            self.total_frame = skill.SKILL_TOTAL_FRAME

        self.over_at = be.frames + self.total_frame
        self.target_type = self.skill.target_type(self)
        self.target_pos = self.target_type[1]

    def frames(self):
        """
        """

        if not self.attacked:
            self.attacked = True
            yield self.agent.id, {self.field_name: self.target_type}

    def finish(self):
        """
        """

        return self.be.frames >= self.over_at

    def create_disaster(self):
        """
        """

        return self.skill.disaster(self)

    def get_target_pos(self):
        """
        """

        return self.target_pos
