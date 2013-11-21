# coding:utf-8

from lib.db import Carrier
from lib.db.fields import ModelDict
from lib.db.fields import ModelList
from lib.db.metaclass import DynamicModel

class Guilds(Carrier):
    """
    """

    __metaclass__ = DynamicModel
    NAME = 'guilds'
    DATABASE = 'lose'
    FIELDS = ('data',)

    def init(self):
        self.data = ModelDict({
            'env_id': 0,
        })

class Guild(Carrier):
    """
    """

    __metaclass__ = DynamicModel
    
    NAME = 'guild'
    DATABASE = 'clusters'
    FIELDS = ('info', 'members', 'apply4')

    def init(self):
        self.info = ModelDict({
            'name': '',
            'exp': 0,
            'level': 1,
            'members': 1,
            'announce': '',
            'need_apply': 1,
        })

        self.members = ModelList({'power': 0,
                                  'value': 0},
                                 'uid', 'gid')
        self.apply4 = ModelList({'msg': ''},
                                 'uid', 'gid')

    def load(self, env, pk=None):
        if not self.pk:
            self.pk = pk

        if self.pk:
            guilds = Guilds(self.pk)
            guilds.load(env)

            if not guilds.data['env_id']:
                return None

            super(Guild, self).load(env)

            return self

        return None
