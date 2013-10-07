# coding: utf-8
from constants import (B_PERCENT, 
                       B_ABILITY_ADD, 
                       B_VALUE)
from base import BaseEffect
from instantft.ai.helper.opp import DizzinessHelper
from instantft.ai.helper.opp import MumHelper
from instantft.ai.helper.opp import TwiningHelper

class Twining(BaseEffect):
    def effective(self):
        self.be.wrappers[self.agent.id] = TwiningHelper

    def die(self):
        del self.be.wrappers[self.agent.id]

class Mum(BaseEffect):
    def effective(self):
        self.be.wrappers[self.agent.id] = MumHelper

    def die(self):
        del self.be.wrappers[self.agent.id]

class Dizziness(BaseEffect):
    def effective(self):
        self.be.wrappers[self.agent.id] = DizzinessHelper

    def die(self):
        del self.be.wrappers[self.agent.id]
