# coding: utf-8

from lib.db import Carrier
from lib.db.fields import ModelConfig
from lib.db.metaclass import DynamicModel


class Config(Carrier):
    __metaclass__ = DynamicModel
    CACHE_ENABLE = False
    DATABASE = 'lose'
    NAME = 'game_config'
    FIELD_KEY = 'data'
    FIELDS = ['data']

    def init(self):
        self.data = ModelConfig({
                        'name':'',
                        'env': '',
                        'ver': '',
                        'value': '',
                        })


if __name__ == "__main__":
    game_config = Config(env)
