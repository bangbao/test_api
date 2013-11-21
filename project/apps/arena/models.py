# coding: utf-8

from lib.db import Carrier
from lib.db.fields import ModelDict
from lib.db.fields import ModelList
from lib.db.metaclass import DynamicModel


class Arena(Carrier):
    """用户竞技场数据接口

    Attributes:
        data: 基本数据
            buy_count: 酷币购买竞技次数
            battle: 当前已竞技次数
            battle_at: 输的时间记录战斗时间戳，计算cd时间用
            refresh: 刷新竞技对手次数
            rivals: 当前竞技对手uid们
            last_date: 更新时间，'2013-01-01'
            award_at: 领取排名奖励时间字符串，'2013-01-01 01:00:00'
            per_at: 领取间隔时间奖励时间戳
            cont_win: 连胜的次数
            score: 当前积分，不是排名用的积分
            rank: 当前排名
            rank_score: 排名用的积分, 保存为字符串类型

        logs: 竞技日志记录
            ts: 发生时间戳
            type: 日志类型，atk表示攻击， def表示被攻击
            win: 是否胜利 0表示失败， 1 表示胜利
            target_id: 目标用户uid
            target_name: 目标用户昵称
            change_rank: 排名改变，0表示没改变， 其它表示当前排名
            log_id: 日志id, 标识此条日志
            uid: 用户uid

    """
    __metaclass__ = DynamicModel

    NAME = 'arena'
    DATABASE = 'clusters'
    FIELDS = ['data', 'logs']

    def init(self):
        self.data = ModelDict({
                            'buy_count': 0,
                            'battle': 0,
                            'battle_at': 0,
                            'refresh': 0,
                            'rivals': '',
                            'last_date': '',
                            'award_at': '',
                            'per_at': 0,
                            'cont_win': 0,
                            'score': 0,
                            'rank': 0,
                            'rank_score': '',
                            })
        self.logs = ModelList({
                            'ts': '',
                            'type': '',
                            'win': 0,
                            'target_id':'',
                            'target_name': '',
                            'change_rank': 0,
                            }, 'log_id', 'uid')


    def load_all(self, env):
        """加载此模块所有数据
        """
        self.load_data()
        self.load_logs()

        self.load(env)

    def reset_all(self, env):
        """重置此模块所有数据
        """
        self.load_all(env)
        self.data.reset()
        self.logs.reset()

        env.storage.save(self)


