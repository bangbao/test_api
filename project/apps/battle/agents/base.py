# coding: utf-8
from __future__ import division
from heapq import heappush
from collections import defaultdict
from lib.utils import get_it
from lib.utils import sys_random as random
from instantft.battle.timer import AttackRound
from instantft.battle.timer import MoveRound
from instantft.battle.skill import (NORMAL_ATTACK,
                                    MAGIC_ATTACK,
                                    CURE_ATTACK,
                                    REVIVAL_ATTACK,
                                    SKILL_BUFF,
                                    COST_ALL_ANGER)
from instantft.battle.skill.destiny import (destiny_skill_match,
                                            ATK_TIMES,
                                            UNATK_TIMES,
                                            STORM_TIMES,
                                            DODGE_TIMES,
                                            UNSTORM_TIMES)
import itertools

WARRIOR_AGENT = 0
MAGE_AGENT = 1
PASTOR_AGENT = 2
ROBBER_AGENT = 3
KNIGHT_AGENT = 4
RANGER_AGENT = 5
COMMON_AGENT = 101
CATAPULT_AGENT = 102

HIT_E = 10
STORM_E = 0.25

ATK_NORMAL = 0
ATK_STORM = 1
ATK_STORM_BASE = 1
NATK_MIN_VALUE = 1
MATK_MIN_VALUE = 1
ATTACK_MISS = (0, ATK_NORMAL)

def attack_hit(hit, dodge):
    """ 判断攻击是否命中

    一次攻击是否可以打中对手

    Args:
       hit: 攻击方命中
       dodge: 受击方闪避

    Returns:
       是否击中
    """

    probability = int(hit / (hit + (dodge / HIT_E)) * 100)

    return get_it(probability)

def get_storm_value(storm, holdout):
    """ 计算暴击机率

    Args:
       storm: 暴击数值
       holdout: 抵抗数值

    Returns:
       暴击数值
    """

    value = storm * STORM_E
    probability = (value / (value + holdout)) * 100

    if get_it(probability):
        return ATK_STORM_BASE + (probability * 0.01)

    return ATK_STORM_BASE

def get_atk_value(agent, target):
    """
    """

    atk_values = {
        NORMAL_ATTACK: max(1, agent.nattack - target.ndefend),
        MAGIC_ATTACK: max(1, agent.mattack - target.mdefend),
    }

    storm_hit = get_storm_value(agent.storm_hit, target.holdout_storm)

    atk_type = ATK_NORMAL

    if storm_hit > ATK_STORM_BASE:
        atk_type = ATK_STORM

    def wrapper(values, hurt_type):
        hurts = []
        total_hurt = 0

        for value in values:
            if hurt_type == NORMAL_ATTACK:
                normal = max(1, value - target.ndefend)
                magic = atk_values[MAGIC_ATTACK]
            elif hurt_type == MAGIC_ATTACK:
                magic = max(1, value - target.mdefend)
                normal = atk_values[NORMAL_ATTACK]

            hurt = int((normal + magic) * storm_hit)
            heappush(hurts, (hurt, atk_type))
            total_hurt += hurt

        return total_hurt, hurts

    return wrapper, storm_hit

class BattleAgent(object):
    """ 战场中战斗单位的基类
     
      控制所有战斗单位的基础动作

    Attributes: 
      id: 战场上的唯标识
      gid: 所属分组，区分攻守双方
      position: 在战场中所属于几号球的选手
      actor: 动画类型
      buffers: 身上所有的效果
      hp: 总血量
      ai: AI类型
      atk_cd: 攻击间隔
      atk_round: 回合数，结合atk_cd判断是否可以出手
      nattack: 物理攻击力
      mattack: 魔法攻击力
      nskill: 物理攻击技能
      mskill: 魔法攻击技能
      ndefend: 物理防御力
      mdefend: 魔法防御力
      move: 移动能力的计数器
      enmity: 受到时仇恨计算的系数
      res: 前端对应的人物资源
      face_to: 单位面对的方向0为向左，1为向右
      level: 战斗单位的等级
      bf_init: 战场所需要的属性
      hit: 命中值
      dodge: 闪避值
      storm_hit: 暴击数值
      holdout_storm: 暴击抵抗

      hurt: 受伤总量
      last_hurt: 最后一次受伤的数值，用来计算仇恨数据
      anger: 怒气值，当怒气值达到指定数量时可以释放怒气技能
      target: 攻击目标，当在进行目标选择时，需要将当前的攻击目标保存
      attacked: 是否进行过攻击，用来控制是否需要初始化攻击回合计数
    """

    def __init__(self, **kwargs):
        self.id = None
        self.gid = None
        self.position = None
        self.buffers = {}
        self.hp = kwargs['hp']
        self.face_to = None
        self.ai = kwargs['ai']
        self.atk_cd = AttackRound(*kwargs['atk_cd'])
        self.nattack = kwargs['natk']
        self.mattack = kwargs['matk']
        self.ndefend = kwargs['ndef']
        self.mdefend = kwargs['mdef']
        self.nskill = kwargs['normal_skill']
        self.mskill = kwargs['anger_skill']
        self.dskill = kwargs['destiny_skill']
        self.storm_hit = kwargs['storm_hit']
        self.move = MoveRound(kwargs['speed'], kwargs['speed_round'])
        self.width = kwargs['width']
        self.high = kwargs['high']
        self.enmity = kwargs['enmity']
        self.res = kwargs['res']
        self.release_anger = kwargs['release_anger']
        self.level = kwargs['level']
        self.bf_init = kwargs['bf_init']
        self.hit = kwargs['hit']
        self.dodge = kwargs['dodge']
        self.holdout_storm = kwargs['holdout_storm']
        self.anger = kwargs['rage']

        self.hurt = 0
        self.target = None
        self.atk_times = 0
        self.attacked = False

        self.reduce_hurt = {
            REVIVAL_ATTACK: self.reduce_revival,
            NORMAL_ATTACK: self.reduce_normal_hurt,
            MAGIC_ATTACK: self.reduce_magic_hurt,
            CURE_ATTACK: self.reduce_cure_hurt
        }

    @property
    def actor(self):
        """ 战斗单位身份
        
        用来区别单位的身份，默认AI的选择

        """

        raise NotImplementedError

    def set_info(self, pk, gid, position=None):
        """ 设置单位信息

        在战斗中用户标识用户身份的数据

        Args:
            pk:  单位的主键
            gid: 单位所属的组
            position: 单位在几号位
        """

        if not self.id:
            self.id = pk

        self.gid = gid
        self.position = position
        self.face_to = gid

    def set_target(self, target_id):
        """
        """

        self.target = target_id

    def is_self(self, agent):
        """
        """

        return self.id == agent.id

    def bout(self):
        """
        """

        if self.atk_cd.circle(self.attacked):
            self.attacked = False

    def has_attack_cd(self):
        """
        """

        return not self.atk_cd.able_to()

    def get_atk_skill(self, be):
        """
        """

        if destiny_skill_match(be, self):
            return be.skill_app.get_skill(self.dskill)

        if self.anger >= self.release_anger and self.mskill:
            return be.skill_app.get_skill(self.mskill)

        return be.skill_app.get_skill(self.nskill)

    def can_magic_attack(self):
        """ 判断是否可以释放努气技能
        
          当怒气值达到指定数据时，会释放怒气技能

        Returns:
          是否可以释放怒气技能
        """

        return self.anger >= self.release_anger and self.mskill

    def add_anger(self, value):
        """
        """

        self.anger += value

    def alive(self):
        """ 判断当前是否存活
        
          用来判断当前战斗单位是否存活，当受伤害的数值小于
        总血量时，为存状态

        Returns:
          是否存活
        """

        return self.hurt < self.hp

    def to_dead(self):
        """ 使当前单位死亡
        """

        self.hurt = self.hp

    def lifetime(self):
        """ 获取寿命

        治疗队友选择目标时按照寿命选择
        寿命 = 剩余血量 / 总血量
        """

        return (self.hp - self.hurt) / self.hp

    def attack_to(self, skill, be, *targets):
        """ 向目标发起攻击

          根据当前状态向进行普通或魔法攻击目标

        Args:
          action: 所使用的攻击动作
          targets: 受到攻击的列表

        Returns:
          每个目标受到的攻击状态
        """

        hurts = defaultdict(list)

        filter_func = skill.hit_targets(self, be)

        be.counters[self.id][ATK_TIMES] += 1

        for target in itertools.ifilter(filter_func, targets):
            target.add_anger(skill.SKILL_ADD_ANGER)

            buff = {}
            storm = False

            if attack_hit(self.hit, target.dodge):
                hurt = skill.skill(self, target, be)
                buff = hurt.pop(SKILL_BUFF, {})
                atk_hurts, storm = self.apply_hurt(target, hurt, be)

                hurts[target.id].extend(atk_hurts)
                be.counters[target.id][UNATK_TIMES] += 1
            else:
                hurts[target.id].append(ATTACK_MISS)
                be.counters[target.id][DODGE_TIMES] += 1

            if storm:
                be.counters[self.id][STORM_TIMES] += 1
                be.counters[target.id][UNSTORM_TIMES] += 1

            for buff_id in buff:
                be.buff.add_buff(target.id, buff_id)

        if skill.IS_ANGER_SKILL:
            if skill.SKILL_COST_ANGER == COST_ALL_ANGER:
                self.anger = 0
            else:
                self.anger -= SKILL_COST_ANGER

        return dict(hurts)

    def apply_hurt(self, target, hurt, be):
        """

        """

        round_hurts = []
        atk_value, storm = get_atk_value(self, target)

        for tp, hurts in hurt.iteritems():
            total_hurt, atk_hurts = target.under_attack(tp, hurts, atk_value)

            if total_hurt and \
               (self.id in be.groups[self.gid] and \
                target.id in be.groups[target.gid]):
                be.unatk_enmity(self, target, tp, total_hurt)

            round_hurts.extend(atk_hurts)

        return round_hurts, storm

    def teammate(self, target):
        """
        """

        return self.gid == target.gid

    def reduce_normal_hurt(self, values, atk_value):
        """
        """

        return atk_value(values, NORMAL_ATTACK)

    def reduce_magic_hurt(self, values, atk_value):
        """
        """

        return atk_value(values, MAGIC_ATTACK)

    def reduce_cure_hurt(self, values, atk_value):
        """
        """

        hurts = []
        total_hurt = 0

        for value in values:
            hurt = -value
            heappush(hurts, (hurt, CURE_ATTACK))
            total_hurt += hurt

        return total_hurt, hurts

    def reduce_revival(self, none, atk_value):
        """
        """

        self.hurt = 0
        self.anger = 0
        self.target = None
        self.atk_times = 0
        self.attacked = False

        return 0, []

    def under_attack(self, atk_type, params, atk_value):
        """
        """

        last_hurt, hurts = self.reduce_hurt[atk_type](params, atk_value)
        value = min(self.hp, max(self.hurt + last_hurt, 0))
        last_hurt = value - self.hurt

        self.hurt = value

        return last_hurt, hurts
