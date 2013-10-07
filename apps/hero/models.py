# coding: utf-8

from cheetahes.db import Carrier
from cheetahes.db.fields import ModelDict
from cheetahes.db.fields import ModelList
from cheetahes.db.metaclass import DynamicModel

class Hero(Carrier):
    """用户卡牌常用属性

    Attributes:
        data: 存放属性
            resolve: 当前剩余免费分解次数
            resolve_top: 每天免费分解次数上限
            st_cd: 冷却时间, 单位分钟
            st_at: 最后一次强化时间戳
            last_date: 每日更新日期, '2013-01-01'
            forge: 每日锻造次数
            forge_cycle: 每10次循环中锻造次数
            forge_point: 锻造点数
            forge_level: 锻造等级
            masters: 工匠级别组合: '0,1,1,0', 数字表示级别
            master_at: 工匠清空时间字符串
            master_up: 工匠每日升级次数
            pet_at: 宠物饱食度最后一次下降时间戳
            pet_skill: 宠物每天刷新技能次数

        heros: 存放卡牌数据
            cfg_id: 卡牌配置ID
            level: 卡牌等级
            exp: 卡牌当前经验
            level_up: 卡牌当前剩余经验
            job: 卡牌当前职业
            hp: 卡牌血量
            natk: 物理攻击
            ndef: 物理防御
            matk: 魔法攻击
            mdef: 魔法防御
            sign: 卡牌签名
            cost: 卡牌cost值
            lock: 卡牌是否被锁定
            askill: 卡牌怒气技能等级
            nskill: 卡牌普通技能等级
            hero_id: 用户卡牌标识
            uid: 用户uid

        equips: 装备背包
            cfg_id: 配置ID
            level: 等级
            hp: 血量
            natk: 物理攻击
            ndef: 物理防御
            matk: 魔法攻击
            mdef: 魔法防御
            gold: 强化成功时消耗的金币累计
            sign: 签名
            equip_id: 用户装备标识
            uid: 用户uid

        materials: 装备材料背包
            cfg_id: 配置ID
            num: 数量
            uid: 用户uid

        items: 卡牌转职材料背包
            cfg_id: 配置ID
            num: 数量
            uid: 用户uid

        goblins: 零件背包
            cfg_id: 配置ID
            level: 当前等级
            exp: 当前经验
            level_up: 当前剩余经验
            goblin_id: 零件标识id
            uid: 用户uid

        pets: 宠物背包
            cfg_id: 配置ID
            level: 等级
            exp: 卡牌当前经验
            level_up: 卡牌当前剩余经验
            hp: 血量
            natk: 物理攻击
            ndef: 物理防御
            matk: 魔法攻击
            mdef: 魔法防御
            full: 当前饱食度
            clone: 当前第几代，从1开始
            skill: 拥有的技能们
            pet_id: 宠物标识id
            uid: 用户uid
    """
    __metaclass__ = DynamicModel
    NAME = 'hero'
    DATABASE = 'clusters'
    FIELDS = ['heros', 'data', 'equips', 'materials', 'items', 'goblins', 'pets']

    def init(self):
        self.data = ModelDict({
                               'resolve': 0,
                               'resolve_top': 0,
                               'st_cd': 0,
                               'st_at': 0,
                               'last_date': '',
                               'forge': 0,
                               'forge_cycle': 0,
                               'forge_point': 0,
                               'forge_level': 0,
                               'masters': '',
                               'master_at': '',
                               'master_up': 0,
                               'pet_at': 0,
                               'pet_skill': 0,
                            })
        self.heros = ModelList({'cfg_id': 0,
                                'level': 1,
                                'exp': 0,
                                'level_up': 0,
                                'job': 0,
                                'hp': 0,
                                'natk': 0,
                                'ndef': 0,
                                'matk': 0,
                                'mdef': 0,
                                'sign': '',
                                'cost': 0,
                                'lock': 0,
                                'askill': 1,
                                'nskill': 1,
                               }, 'hero_id', 'uid')
        self.equips = ModelList({
                                'cfg_id': 0,
                                'level': 1,
                                'matk': 0,
                                'mdef': 0,
                                'natk': 0,
                                'ndef': 0,
                                'hp': 0,
                                'gold': 0,
                                'sign': '',
                                }, 'equip_id', 'uid')
        self.materials = ModelList({
                                'num': 0,
                                }, 'cfg_id', 'uid')
        self.items = ModelList({
                                'num': 0,
                                }, 'cfg_id', 'uid')
        self.goblins = ModelList({
                                'cfg_id': 0,
                                'level': 1,
                                'exp': 0,
                                'level_up': 0,
                                }, 'goblin_id', 'uid')
        self.pets = ModelList({
                                'cfg_id': 0,
                                'level': 1,
                                'exp': 0,
                                'level_up': 0,
                                'full': 0,
                                'clone': 1,
                                'skill': '',
                                }, 'pet_id', 'uid')

    def load_all(self, env):
        """加载此模块所有数据
        """
        self.load_data()
        self.load_heros()
        self.load_equips()
        self.load_materials()
        self.load_items()
        self.load_goblins()
        self.load_pets()

        self.load(env)

    def reset_all(self, env):
        """重置此模块所有数据
        """
        self.load_all(env)
        self.data.reset()
        self.heros.reset()
        self.equips.reset()
        self.materials.reset()
        self.items.reset()
        self.goblins.reset()
        self.pets.reset()

        env.storage.save(self)

