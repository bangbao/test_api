# coding: utf-8

from lib.db import Carrier
from lib.db.fields import ModelDict
from lib.db.fields import ModelList
from lib.db.field_redis import RedisSortedSet
from lib.db.field_redis import RedisSortedSetHM
from lib.db.field_redis import RedisString
from lib.db.field_redis import RedisHash
from lib.db.metaclass import DynamicModel


class Hero(Carrier):
    """用户卡牌常用属性
    Attributes:
        data: 存放属性
            resolve: 当前剩余免费分解次数
        equips: 装备背包
            cfg_id: 配置ID
            level: 等级
            hp: 血量
    """
    __metaclass__ = DynamicModel
    NAME = 'hero'
    DATABASE = 'clusters'
    FIELDS = ['heros', 'data']

    def init(self):
        self.data = ModelDict({
                               'resolve': 0,
                            })
        self.heros = ModelList({'cfg_id': 0,
                                'level': 1,
                               }, 'hero_id', 'uid')

    def load_all(self, env):
        """加载此模块所有数据
        """
        self.load(env)

    def reset_all(self, env):
        """重置此模块所有数据
        """
        env.storage.save(self)


class Game(Carrier):
    """用户游戏常用属性模块

    必须定义的类属性:
        NAME: 模块名
        DATABASE: 所用的settings中哪个数据库
        FIELDS: 定义游戏属性, 其中key用于与NAME组合成数据库表名, value为定义的属性集合

    Attributes:
        user: 存放经常修改的属性
            level: 用户级别
        arena: 竞技场排名

        equip: 编队装备
            pos0~pos7: 编队的对应位置
    """
    __metaclass__ = DynamicModel
    NAME = 'game'
    DATABASE = 'clusters'
    FIELDS = ('info', 'user', 'friends', 'arena', 'award',
              'equip', 'goblin', 'announce')

    def init(self):
        self.info = ModelDict({
                            'username': '',
                            })

        self.friends = ModelList({'foreign_at': ''},
                             'fid', 'uid')
        self.arena = RedisSortedSet('redis')
        self.announce = RedisSortedSetHM('redis')

    def load_all(self, env):
        """加载此模块所有数据
        """

    def reset_all(self, env):
        """重置此模块所有数据
        """
        env.storage.save(self)

