# coding: utf-8

from instantft.battle.agent.base import BaseAgent
import random

class Agent(BaseAgent):
    """ 战斗单位基础类

      战斗单位基类，控制子类行为，创建战斗单位的基础属性

    Attributes:
       buffers: 所有保护的属性
       hp: 血上限
       hurt: 当前受到的伤害
       
       NORMAL_ATTACK_TYPE: 普通攻击
       MAGICK_ATTACK_TYPE: 魔法攻击
    """

    NORMAL_ATTACK_TYPE = 1
    MAGICK_ATTACK_TYPE = 2

    def __init__(self, hp, attack, actor, atk_distance=1, rate=1):
        """ 初始化

        Args:
           hp: 血上限
        """

        self.id = None
        self.actor = actor
        self.gid = 0
        self.buffers = {}
        self.hp = hp
        self.hurt = 0
        self.atk_distance = atk_distance
        self.rate = rate
        self.attack = attack

    def alive(self):
        """
        """

        return self.hurt < self.hp

    def setgid(self, gid):
        """
        """

        self.gid = gid

    def setpk(self, pk):
        """
        """

        self.id = pk

    def attack_to(self, *targets):
        """
        """

        hurts = {}

        for target in targets:
            tp, value = self.calc_hurt(target)
            hurts[target.id] = target.under_attack(tp, value)

        return hurts

    def under_attack(self, hurt_tp, hurt_val):
        """
        """

        hurt = self.reduce_hurt(hurt_tp, hurt_val)

        self.apply_hurt(hurt)

        return hurt

    def apply_hurt(self, hurt):
        """
        """

        value = self.hurt + hurt

        self.hurt = max(0, value)

    def reduce_hurt(self, hurt_tp, hurt_val):
        """
        """

        return random.randint(*self.attack)

    def calc_hurt(self, target):
        """
        """

        return self.NORMAL_ATTACK_TYPE, target.hp

