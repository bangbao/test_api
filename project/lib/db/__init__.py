# coding: utf-8
from metaclass import DynamicModel
from fields import ModelDict
from fields import ModelList
from expressions import Incr

class Carrier(object):
    CACHE_ENABLE = True

    def __init__(self, pk, read_only=False):
        self.pk = pk
        self.read_only = False
        self.reload_cache = False
        self._loads = {}
        self.init()

    def init(self):
        """
        """

        raise NotImplementedError

    def load(self, env):
        """
        """

        for name in self._loads.keys():
            obj = getattr(self, name)
            kwargs = self._loads.pop(name)

            if obj.CACHE_TYPE and self.CACHE_ENABLE:
                env.cache.get(self, name, kwargs)
            else:
                obj.init(env, name, self)

if __name__ == "__main__":
    class Game(Carrier):
        __metaclass__ = DynamicModel

        NAME = 'game'
        DATABASE = 'clusters'

        FIELDS = ['data']

        def init(self):
            self.data = ModelDict({'username': 2,
                                  'password': '',
                                  'salt': '',
                                  'token': ''})
    g = Game(1)
    g.data['username'] = 1123
    g.data['token'] = Incr('token', 1, g.data)

    print g.data.sql_update('data', g)
