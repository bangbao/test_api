# coding:utf-8

from instantft.battle.timer import Train
from base import BaseDisaster

class BulletDisaster(BaseDisaster):
    def __init__(self, atk_action, speed, rounds):
        self.be = atk_action.be
        self.agent = atk_action.agent
        self.opper = atk_action.opper
        self.skill = atk_action.skill
        
        distance = self.be.bf.straight_distance(
            self.be.places[self.agent.id],
            self.be.places[self.opper.id])

        self.train = Train(distance, speed, rounds)

    def finish(self):
        """
        """

        return self.train.stop()

    def frame(self, data):
        """
        """

        if self.train.move():
            targets = self.skill.hit_range(self.agent, self.opper, self.be)
            hurts = self.agent.attack_to(self.skill, self.be, *targets)

            self.frame_update(data, hurts)

class AttackDisaster(BaseDisaster):
    SPEED = 1
    ROUNDS = 1

    def __init__(self, atk_action, frames=1):
        """
        """

        self.be = atk_action.be
        self.agent = atk_action.agent
        self.opper = atk_action.opper
        self.skill = atk_action.skill
        self.train = Train(frames, self.SPEED, self.ROUNDS)

    def finish(self):
        """
        """

        return self.train.stop()

    def frame(self, data):
        """
        """

        if self.train.move():
            targets = self.skill.hit_range(self.agent, self.opper, self.be)
            hurts = self.agent.attack_to(self.skill, self.be, *targets)
            self.frame_update(data, hurts)

class RevivalDisaster(BaseDisaster):
    SPEED = 1
    ROUNDS = 1
    TOTAL_FRAME = 1

    def __init__(self, atk_action):
        """
        """

        self.be = atk_action.be
        self.agent = atk_action.agent
        self.opper = atk_action.opper
        self.skill = atk_action.skill
        self.train = Train(self.TOTAL_FRAME, self.SPEED, self.ROUNDS)

    def finish(self):
        """
        """

        return self.train.stop()

    def frame(self, data):
        """
        """

        if self.train.move():
            targets = self.skill.hit_range(self.agent, self.opper, self.be)
            hurts = self.agent.attack_to(self.skill, self.be, *targets)
