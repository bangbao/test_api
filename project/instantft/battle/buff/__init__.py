# coding: utf-8
from collections import defaultdict
from instantft.battle.skill import SKILL_BUFF
from constants import (B_EFFECT, B_CYCLE, B_VALUE, B_PERCENT, B_DURATIONS)
import simple
import action
import itertools

E_TOP_HP = 1
E_RAGE = 2
E_HP = 3
E_NATK = 4
E_MATK = 5
E_NDEF = 6
E_MDEF = 7
E_HIT = 8
E_DODGE = 9
E_STORM = 10
E_STORM_HURT = 11
E_STORM_HOLDOUT = 12
E_FINAL_HURT = 13
E_DEAD_SUMMON = 14
E_HIDE_SUMMON = 15
E_CYCLE_SUMMON = 16
E_TWINING = 17
E_MUM = 18
E_DIZZINESS = 19
E_UNBEATABLE = 20 
E_ARMOR = 21

BUFF_EFFECTS = {
    E_TOP_HP: simple.TopHP,
    E_NATK: simple.NAtk,
    E_MATK: simple.MAtk,
    E_NDEF: simple.NDef,
    E_MDEF: simple.MDef,
    E_HIT: simple.Hit,
    E_DODGE: simple.Dodge,
    E_STORM: simple.Storm,
    E_STORM_HURT: simple.StormHoldout,
    E_TWINING: action.Twining,
    E_MUM: action.Mum,
    E_DIZZINESS: action.Dizziness,
}

SKILL_BUFF_ATTR = 'attrs'
BUFF_ADD = 'add_buff'
BUFF_DIE = 'die_buff'
BUFF_HURT = 'hurt'

BUFF_NAMES = {
    E_TOP_HP: 'top_hp',
    E_NATK: 'natk',
    E_MATK: 'matk',
    E_NDEF: 'ndef',
    E_MDEF: 'mdef',
    E_HIT: 'hit',
    E_DODGE: 'dodge',
    E_STORM: 'storm',
    E_STORM_HOLDOUT: 'storm_holdout',
    E_TWINING: 'twining',
    E_MUM: 'mum',
    E_DIZZINESS: 'dizziness',

    E_UNBEATABLE: 'unbeatable',
    E_HP: 'hp',
    E_RAGE: 'rage',
    E_STORM_HURT: 'storm_hurt',
    E_FINAL_HURT: 'final_hurt',
    E_ARMOR: 'armor',
}

def buff_effect_name(buff_obj, buffs, attrs, hurts):
    """
    """

    target_id = buff_obj.agent.id

    buffs[target_id].append(BUFF_NAMES[buff_obj.effect])

def buff_die_name(buff_obj, buffs, attrs, hurts):
    target_id = buff_obj.agent.id

    buffs[target_id].append(BUFF_NAMES[buff_obj.effect])

def cmp_buff(src, dest):
    """ 对比两个buff谁的效果更好

    Args:
       src: 原buff
       target: 目标buff

    Returns:
       原buff是否优于目标buff
    """

    return src[B_VALUE] >= dest[B_VALUE] or \
        src[B_PERCENT] >= dest[B_PERCENT]

class Buff(object):
    """ buff系统实现

    在技能脚本中会对生buff属性附加到用户身上
    完成buff对战斗角色的属性更改
    完成buff有效期的控制
    完成buff在有效期内的循环生效

    Attributes:
        buffers: 当前用所有生效的buff集合
        effects: 当前buff效果
        timer_runs: 在指定回合需要生效的buff, 针对循环buff
        buff_config: 全局的buff配置, 取所有相对应的buff参数
        locus: 已经过多少回合
        buff_seq: buffid的生成序列

        pending: 待生效的buff效果
        replaces: 需要从角色身上替换一个新的buff
        add_effects: 待生效buff效果的索引，当有冲突的buff时会找一个最佳的buff生效
    """

    def __init__(self, buff_config):
        self.buffers = defaultdict(dict)
        self.effects = defaultdict(dict)
        self.timer_runs = defaultdict(list)
        self.failures = defaultdict(list)
        self.buff_config = buff_config
        self.locus = 0
        self.buff_seq = 0

        self.init()

    def init(self):
        """ 初始化数据

        当整理完一轮buff后，会将待生效，替换的列队清空
        """

        self.pending = defaultdict(dict)
        self.add_effects = defaultdict(dict)

    def effective(self, impress_id):
        """ 将一个buff效果生效在角色卡牌身上

        Args:
            impress_id: buff效果id

        Returns:
           buff效果对象
        """

        buff_obj = self.buffers[impress_id]

        if buff_obj.buff_config[B_CYCLE]:
            run_frame = self.locus + buff_obj.buff_config[B_CYCLE]
            self.timer_runs[run_frame].append(impress_id)

        buff_obj.effective()

        return buff_obj

    def apply_buff(self, target, buff_config, be):
        """ 对一个目标应用一个buff

        主要完成为分配id, 记录到期时间

        Args:
           target: 目标角色卡牌对象
           buff_config: buff的相关配置
        """

        self.buff_seq += 1

        buff_cls = BUFF_EFFECTS[buff_config[B_EFFECT]]
        buff_obj = buff_cls(target, buff_config, be)

        impress_id = self.buff_seq
        expried_at = self.locus + buff_obj.get_durations()

        self.buffers[impress_id] = buff_obj
        self.failures[expried_at].append(impress_id)

        return self.effective(impress_id)

    def add_buff(self, target_id, buff_id):
        """ 为一个目标添加一个待生效的buff

        Args:
            target_id: 目标id
            buff_id: 待生效的buff_id
        """

        buff = self.buff_config[buff_id]

        for buff_config in buff:
            exists_id = self.effects[target_id].get(buff_config[B_EFFECT])
            p_buff_config = self.add_effects[target_id].\
                            pop(buff_config[B_EFFECT], None)

            add_pending = False

            if exists_id:
                buff_obj = self.buffers[exists_id]

                if cmp_buff(buff_config, buff_obj.buff_config):
                    add_pending = True
                    self.die_buff(exists_id)
            else:
                p_buff_config = self.add_effects[target_id].\
                                pop(buff_config[B_EFFECT], None)
                add_pending = not p_buff_config
            
                if p_buff_config:
                    add_pending = cmp_buff(buff_config, p_buff_config)

            if add_pending:
                self.pending[target_id][buff_config[B_EFFECT]] = buff_config
                self.add_effects[target_id][buff_config[B_EFFECT]] = buff_config

    def die_buff(self, impress_id):
        """ 将一个buff消失

        Args:
           impress_id: buff效果id

        Returns:
           buff效果对象
        """

        buff_obj = self.buffers[impress_id]
        buff_obj.die()

        return self.buffers.pop(impress_id)

    def frame(self):
        """ 行动一帧

        会检查待生效队列，周期队列和失效队列，
        当有任一队列有需要整理的buff数据时都标志着需要整理buff数据

        Returns:
           是否需要整理buff数据
        """

        self.locus += 1

        return self.pending or self.locus in self.timer_runs or \
            self.locus in self.failures

    def sort_out(self, be, data):
        """ 对所有可能有buff修改队列进行整理操作

        Args:
            be: BattleEvniron战斗环境
            data: 帧数据
        """

        add_buffs = defaultdict(list)
        attrs = defaultdict(dict)
        hurts = defaultdict(list)
        die_buffs = defaultdict(list)
        agents = set()

        for agent_id, buffs in self.pending.iteritems():
            agent = be.agents[agent_id]

            for buff_config in buffs.itervalues():
                buff_obj = self.apply_buff(agent, buff_config, be)
                buff_effect_name(buff_obj, add_buffs, attrs, hurts)

            agents.add(agent_id)
            
        failures = self.failures.pop(self.locus, [])
        filter_func = self.buffers.get

        for impress_id in itertools.ifilter(filter_func, failures):
            buff_obj = self.die_buff(impress_id)
            buff_die_name(buff_obj, die_buffs, attrs, hurts)
            agents.add(buff_obj.agent.id)

        timers = self.timer_runs.pop(self.locus, [])

        for impress_id in itertools.ifilter(filter_func, timers):
            buff_obj = self.effective(impress_id)
            buff_modify[agent_id] = buff_effect_name(buff_obj)
            agents.add(buff_obj.agent.id)

        self.init()

        for agent_id in agents:
            obj = data[agent_id]
            
            if add_buffs[agent_id]:
                obj[BUFF_ADD] = add_buffs[agent_id]

            if die_buffs[agent_id]:
                obj[BUFF_DIE] = die_buffs[agent_id]

            if attrs[agent_id]:
                obj[SKILL_BUFF_ATTR] = attrs[agent_id]

if __name__ == "__main__":
    pass
