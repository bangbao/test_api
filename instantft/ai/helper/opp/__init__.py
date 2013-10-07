# coding: utf-8
from instantft.ai.action.idle import IdleAction
from instantft.ai.action.dead import DeadAction
from instantft.ai.action.move import MoveAction
from instantft.ai.action.attack import AttackAction
from base import BaseHelper

class BaseWrapper(BaseHelper):
    def __init__(self, helper):
        self.helper = helper
        self.default_action = IdleAction(helper.agent, helper.be)

    def frame(self):
        action = self.helper.frame()

        if not self.match(action):
            return action

        return self.default_action

    def finish(self):
        return self.helper.finish()

    def match(self, action):
        return action.FIELD_NAME != DeadAction.FIELD_NAME

class TwiningHelper(BaseWrapper):
    def match(self, action):
        return action.FIELD_NAME != MoveAction.FIELD_NAME

class DizzinessHelper(BaseWrapper):
    pass

class MumHelper(BaseWrapper):
    def match(self, action):
        return isinstance(action, AttackAction) and \
            action.field_name != AttackAction.RAGE_ATK
