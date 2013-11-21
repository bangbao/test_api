# coding: utf-8

from lib.db import Carrier
from lib.db.fields import ModelDict
from lib.db.fields import ModelList
from lib.db.metaclass import DynamicModel


class Adven(Carrier):
    """用户adven常用属性模块

    Attributes:
        adven: 存放最高记录
            chapter: 章节ID
            stage: 关卡ID

        readven: 存放重置章节的数据
            chapter: 章节ID
            stage: 关卡ID
            select: 此章节所选择的阵营: light或者dark
            reset: 重置次数，0表示没重置过

        data: 每个关卡的记录
            stage: 关卡ID
            light: 光明积分
            dark: 黑暗积分
            grade: 评分
            energy: 消耗的体力
    """
    __metaclass__ = DynamicModel
    NAME = 'adven'
    DATABASE = 'clusters'
    FIELDS = ['adven', 'readven', 'data']

    def init(self):
        self.adven = ModelDict({
                        'chapter': 1,
                        'stage': 11})
        self.readven = ModelList({
                        'stage': 0,
                        'select': '',
                        'reset': 0,
                        }, 'chapter', 'uid')
        self.data = ModelList({
                        'light': 0,
                        'dark': 0,
                        'grade': 0,
                        'energy': 0,
                        }, 'stage', 'uid')

    def load_all(self, env):
        """加载此模块所有数据
        """
        self.load_adven()
        self.load_readven()
        self.load_data()

        self.load(env)

    def reset_all(self, env):
        """重置此模块所有数据
        """
        self.load_all(env)
        self.adven.reset()
        self.readven.reset()
        self.data.reset()

        env.storage.save(self)

