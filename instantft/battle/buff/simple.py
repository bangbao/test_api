# coding: utf-8
from constants import (B_PERCENT, 
                       B_ABILITY_ADD, 
                       B_VALUE)
from base import BaseEffect

class TopHP(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_hp = self.agent.hp + self.buff_config[B_ABILITY_ADD]
        self.diff = final_hp - self.agent.hp
        self.agent.hp = final_hp

    def die(self):
        self.agent.hp -= self.diff
        self.init()

    def efocus(self, attrs, hurts):
        self.attrs[self.agent.id].update({self.effect: self.agent.hp})

    def dfocus(self, attrs, hurts):
        self.attrs[self.agent.id].update({self.effect: self.agent.hp})

class NAtk(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_atk = self.agent.nattack + self.buff_config[B_VALUE]
        self.diff = final_atk - self.agent.nattack
        self.agent.nattack = final_atk

    def die(self):
        self.agent.nattack -= self.diff
        self.init()

class MAtk(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_atk = self.agent.mattack + self.buff_config[B_VALUE]
        self.diff = final_atk - self.agent.mattack
        self.agent.mattack = final_atk

    def die(self):
        self.agent.mattack -= self.diff
        self.init()

class NDef(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_def = self.agent.ndefend + self.buff_config[B_VALUE]
        self.diff = final_def - self.agent.ndefend
        self.agent.ndefend = final_def

    def die(self):
        self.agent.ndefend -= self.diff
        self.init()

class MDef(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_def = self.agent.mdefend + self.buff_config[B_VALUE]
        self.diff = final_def - self.agent.mdefend
        self.agent.mdefend = final_def

    def die(self):
        self.agent.mdefend -= self.diff
        self.init()

class Hit(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_hit = self.agent.hit + self.buff_config[B_VALUE]
        self.diff = final_hit - self.agent.hit
        self.agent.hit = final_hit

    def die(self):
        self.agent.hit -= self.diff
        self.init()

class Dodge(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_dodge = self.agent.dodge + self.buff_config[B_VALUE]
        self.diff = final_dodge - self.agent.dodge
        self.agent.dodge = final_dodge

    def die(self):
        self.agent.dodge -= self.diff
        self.init()

class Storm(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_storm_hit = self.agent.storm_hit + self.buff_config[B_VALUE]
        self.diff = final_storm_hit - self.agent.storm_hit
        self.agent.storm_hit = final_storm_hit

    def die(self):
        self.agent.storm_hit -= self.diff
        self.init()

class StormHoldout(BaseEffect):
    def init(self):
        self.diff = 0

    def effective(self):
        final_storm_holdout = self.agent.storm_holdout + self.buff_config[B_VALUE]
        self.diff = final_storm_holdout - self.agent.storm_holdout
        self.agent.storm_holdout = final_storm_holdout

    def die(self):
        self.agent.storm_holdout -= self.diff
        self.init()
