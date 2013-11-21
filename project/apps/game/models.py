# coding: utf-8

from lib.db import Carrier
from lib.db.fields import ModelDict
from lib.db.fields import ModelList
from lib.db.field_redis import RedisSortedSet
from lib.db.field_redis import RedisSortedSetHM
from lib.db.field_redis import RedisString
from lib.db.field_redis import RedisHash
from lib.db.metaclass import DynamicModel


class Game(Carrier):
    """用户游戏常用属性模块

    必须定义的类属性:
        NAME: 模块名
        DATABASE: 所用的settings中哪个数据库
        FIELDS: 定义游戏属性, 其中key用于与NAME组合成数据库表名, value为定义的属性集合

    Attributes:
        info: 存放不经常修改的属性
            username: 用户昵称
            role: 用户角色
            vip: VIP经验
            equip: 装备积分
            hero: 卡牌积分
            exp: 当前经验上限
            energy: 当前体力上限
            enter: 标识用户是否注册过
            cost: 能力值上限
            friend: 好友上限
            energy_fill_at: 行动力最后补充时间

        user: 存放经常修改的属性
            level: 用户级别
            exp: 当前经验
            light: 光明点数
            dark: 黑暗点数
            battle: 征战点数
            energy: 当前行动力
            kcoin: 酷币数量
            gold: 金钱数量
            team: 战斗阵容
            pet: 出战的宠物

        friends: 好友数据
            foreign_at:
            fid:
            uid:

        arena: 竞技场排名

        award: 竞技场排名快照

        equip: 编队装备
            pos0~pos7: 编队的对应位置

        equip: 编队零件
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
                            'role': 1,
                            'vip': 0,
                            'equip': 0,
                            'hero': 0,
                            'exp': 0,
                            'energy': 0,
                            'enter': 0,
                            'cost': 0,
                            'friend': 0,
                            'energy_fill_at': 0,
                            })
        self.user = ModelDict({
                            'level': 1,
                            'exp': 0,
                            'light': 0,
                            'dark': 0,
                            'battle': 0,
                            'energy': 0,
                            'kcoin': 0,
                            'gold': 0,
                            'team': '',
                            'pet': '',
                            })
        self.friends = ModelList({'foreign_at': ''},
                             'fid', 'uid')
        self.arena = RedisSortedSet('redis')
        self.award = RedisSortedSet('redis')
        self.announce = RedisSortedSetHM('redis')
        self.equip = ModelDict({
                            'pos0': '',
                            'pos1': '',
                            'pos2': '',
                            'pos3': '',
                            'pos4': '',
                            'pos5': '',
                            'pos6': '',
                            'pos7': '',
                            })
        self.goblin = ModelDict({
                            'pos0': '',
                            'pos1': '',
                            'pos2': '',
                            'pos3': '',
                            'pos4': '',
                            'pos5': '',
                            'pos6': '',
                            'pos7': '',
                            })

    def load_all(self, env):
        """加载此模块所有数据
        """
        self.load_info()
        self.load_user()
        self.load_friends()
        self.load_equip()
        self.load_goblin()

        self.load(env)

    def reset_all(self, env):
        """重置此模块所有数据
        """
        self.load_all(env)
        self.info.reset()
        self.user.reset()
        self.friends.reset()
        self.equip.reset()
        self.goblin.reset()

        env.storage.save(self)

