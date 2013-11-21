# coding: utf-8

from lib.db import Carrier
from lib.db.fields import ModelDict

class Game(Carrier):
    def init(self):
        self.vip = ModelDict(self, {'vip': 1, 'exp': 0})
        self.user = ModelDict(self, {'level': 1, 'exp': 0, 
                                     'kcoin': 0, 'gold': 0})
