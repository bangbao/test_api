# coding: utf-8

from collections import defaultdict
from instantft.algorighm import pathfind
from instantft.battle.buff import Buff
from instantft.ai.helper.opp import simple
from instantft.ai.helper.opp import defaults
from instantft.ai.action.attack import AttackAction

from heapq import heappush
import itertools

counter_factory = lambda : defaultdict(int)

ATTACK_HELPERS = {
    True: simple.AttackHelper,
    False: simple.ChaseHelper,
}

CHANGE_FACE = [1, 0]

LSTEP, RSTEP, BASE_POS, DIRECTION, LENGTH = xrange(5)

class BattleEnviron(object):
    """ 战场动态数据

    Attributes:
        bf: BattleField战场环境数据
        skill_app: 技能应用，所有技能相关数据的生成
        summon_hero: 召唤英雄对应的接口
        agents: 所有战斗单位在战场中的信息
        wrappers: 针对所有动作的包装，可以控制当前战斗中的动作
        actors: 记录双方战斗前两队的职业数据
        groups: 所有战斗单位的分组信息
        places: 所有战斗单位的位置信息
        actions: 所有战斗单位当前的动作对象
        deads: 战场上所有死亡的单位id
        enmities: 全局仇恨列表
        init_status: 战场初始化时每个战斗单位的状态
        counter: 战斗单位生成id的基数
        frames: 当前战斗所处的帧数
        para_postion: 默认战斗单位对位表
        disasters: 战场中的灾害单位列表
        last_atk_frame: 最后一次发生战斗的帧数
        buff: buff对象, 控制buff的属性的生命周期
        counters: 战斗计数器

        ATTACK_GROUP: 攻击方组的id
        DEFEND_GROUP: 防守方组的id
        DIRECT_ATK: 直接攻击到目标，用户计算仇恨列表
        OPP_GROUPS: 对手组的id
        FORMATION_ORDERS: 阵型排布顺序
    """

    ATTACK_GROUP = 0
    DEFEND_GROUP = 1
    DIRECT_ATK = 0
    OPP_GROUPS = [DEFEND_GROUP, ATTACK_GROUP]
    FORMATION_ORDERS = [0, 1, 2, 3, 4, 5, 6]
    DEFAULT_ENMITY_NUM = 3
    TARGET_ORDERS = [
        [0, 1, 2, 3],
        [1, 0, 2, 3],
        [2, 1, 3, 0],
        [3, 2, 1, 0],
    ]

    def __init__(self, bf, skill_app, summon_hero, skill_buff):
        """ 初始化战斗环境

        Args:
           bf: 战场对象
           skill_app: 技能应用
           summon_hero: 召唤英雄接口
           skill_buff: buff对象
        """

        self.bf = bf
        self.skill_app = skill_app
        self.summon_hero = summon_hero
        self.buff = skill_buff
        self.frames = 0
        self.counter = 0
        self.init_status = {}

    def init(self):
        """ 对象初始化操作

        当回合结束后，需要将战斗的数据重新整理一下
        为计算下一节战斗做准备
        """

        self.agents = {}
        self.groups = [None, None]
        self.places = {}
        self.wrappers = {}
        self.actors = [set(), set()]
        self.actions = {}
        self.deads = [set(), set()]
        self.enmities = {}
        self.para_postion = [{}, {}]
        self.disasters = set()
        self.last_atk_frame = 0
        self.counters = defaultdict(counter_factory)

    @property
    def size(self):
        """ 战场大小

        """

        return (self.bf.xlen, self.bf.ylen)

    def bf_status(self, init_data):
        """
        """

        return {
            'size': self.size,
            'pixel': self.bf.pixel,
            'focus': self.bf.focus,
            'sky': self.bf.sky,
            'init': init_data,
        }

    def frame_up(self, data=None):
        """ 帧数递增

        Args:
           data: 当前帧数据
        """

        self.frames += 1

        if data and self.buff.frame():
            self.buff.sort_out(self, data)

    def get_action_agents(self):
        """ 取得当前需要行动的agent列表
        """

        for agent_id, agent in self.agents.iteritems():
            if not self.has_agent_dead(agent_id):
                yield agent

    def get_action_disasters(self):
        """ 取得当前需要行动的灾难列表
        """

        return tuple(self.disasters)

    def formations(self, teams):
        """ 部署阵型，将人物等数据放置在地图上

        Args:
           teams: 攻防两端的阵容
        """

        len0 = len(teams[self.ATTACK_GROUP]) + self.counter
        len1 = len(teams[self.DEFEND_GROUP])
        members = [range(self.counter, len0), 
                   range(len0, len0 + len1)]

        for gid, team in enumerate(teams):
            self.formation_team(gid, team, members)

        self.counter = members[-1][-1] + 1

    def formation_team(self, gid, team, members):
        """ 队伍部阵型

        将一个组队伍的队员安放到战场中

        Args:
            gid: 队员所属组id
            team: 队员对象列表
            members: 队员对应的编号
        """

        opp_gid = self.OPP_GROUPS[gid]
        opps = members[opp_gid]
        group = set()

        for i, (member, pos) in enumerate(itertools.izip(team, 
                                          self.FORMATION_ORDERS)):
            if member:
                member.set_info(members[gid][i], gid, pos)
                self.para_postion[opp_gid][pos] = member.id
                self.agents[member.id] = member
                self.places[member.id] = self.bf.places[gid][pos]

                group.add(member.id)

        self.groups[gid] = group

    def init_battle(self):
        """ 初始化战斗数据
        """

        played_agents = []

        for agent_id, agent in self.agents.iteritems():
            self.actors[agent.gid].add(agent.gid)
            opp_gid = self.OPP_GROUPS[agent.gid]
            self.enmities[agent_id] = dict.fromkeys(self.groups[opp_gid], 0)

            filter_func = self.para_postion[agent.gid].has_key
            contraposition = itertools.ifilter(filter_func, 
                                               self.TARGET_ORDERS[agent.position])

            agent.set_target(None)

            opp_pos = next(contraposition)
            opp_id = self.para_postion[agent.gid][opp_pos]
            target = self.agents[opp_id]
            value = agent.enmity[self.DIRECT_ATK][target.actor][agent.actor]
            self.enmities[agent.id][target.id] = value * \
                                            target.nattack * \
                                            self.DEFAULT_ENMITY_NUM

            self.init_status[agent_id] = self.get_agent_status(agent)
            played_agents.append((agent_id, self.places[agent_id]))

        return played_agents

    def get_agent_status(self, agent):
        """ 战斗单位状态
        """

        return {
            'hp': agent.hp,
            'hurt': agent.hurt,
            'face_to': agent.face_to,
            'gid': agent.gid,
            'move_speed': agent.move.step,
            'atk_speed': agent.atk_cd.step,
            'res': agent.res,
            'actor': agent.actor,
            'bf_init': agent.bf_init,
        }

    def has_agent_dead(self, agent_id):
        """ 判断一个角色是否死亡

        Args:
           agent_id: 战斗单位id

        Returns:
           角色是否死亡
        """
        
        agent = self.agents[agent_id]

        return agent_id in self.deads[agent.gid]

    def has_new_fight(self, frame):
        """ 在指定的帧数后是否发生过战斗
        """

        return self.last_atk_frame > frame

    def touch_distance(self, agent, target, skill):
        """ 计算两者之间的有效攻击的安全距离

        对于一些辅助职业，需要与目标保持一定的距离

        Args:
           agent: 攻击角色
           target: 目标角色
           skill: 攻击角色使用的技能

        Returns:
           需要移动的格子数
        """

        atk_pos = self.places[agent.id]
        target_pos = self.places[target.id]

        swidth, shigh = self.skill_app.skill_atk_distance(agent, target, 
                                                    skill.SKILL_ATK_DISTANCE)

        return self.bf.touch_distance(atk_pos, (swidth, shigh), target_pos)

    def get_focus_pos(self, pos, target_pos):
        """ 得到一个离指定点最近的有效点

        Args:
           pos: 指定点的 id
           target_pos: 面向的点

        Returns:
           有效点的id
        """

        blocks = self.get_blocks()

        distances = self.bf.xslice(pos)
        step = 1
        length = distances[1]

        if self.bf.focus_to(pos, target_pos):
            step = -1
            length = distances[0]

        if length:
            target_pos += step

        return self.bf.near_empty(target_pos, blocks)

    def set_agent_pos(self, agent, pos):
        """
       """

        agent_pos = self.places[agent.id]

        self.places[agent.id] = self.get_focus_pos(agent_pos, pos)

    def new_agent(self, hero_id, parent, birth_pos):
        """ 在战场上创建一个新的战斗单位

        Args:
           hero_id: 武将卡牌id
           parent: 所属的战斗单位
           birth_pos: 初始位置起始点, 当点被占用时会在该点附近生成

        Returns:
           战斗单位的对象
        """

        self.counter += 1

        agent = self.summon_hero(hero_id, parent.level)
        agent.set_info(self.counter, parent.gid)
        agent.face_to = parent.face_to

        self.places[agent.id] = birth_pos
        self.agents[agent.id] = agent
        self.enmities[agent.id] = dict(self.enmities[parent.id])

        return agent

    def die_agent(self, agent_id):
        """ 使一个agent消失

        用于召唤出来的角色，在指定的时间内消失

        Args:
           agent_id: 要消失的agent编号
        """

        del self.places[agent_id]
        del self.enmities[agent_id]
        self.deads.discard(agent_id)

        return self.agents.pop(agent_id)

    def set_action(self, agent_id, action):
        """ 对一个战半单位指定特殊的动作

        Args:
           agent_id: 战斗单位id
           action: 动作对象
        """

        self.actions[agent_id] = action

    def unatk_enmity(self, agent, target, atk_type, atk_hurt):
        """ 计算被攻击时的仇恨

        当产生伤害时，会根据产生的伤害计算仇恨列表

        Args:
           agent: 攻击对象
           target: 受击目标
           atk_type: 攻击的类型
           atk_hurt: 攻击的伤害值
        """

        gid = target.gid

        if agent.teammate(target):
            gid = self.OPP_GROUPS[target.gid]

        for target_id in self.groups[gid]:
            if target.id != target_id:
                member = self.agents[target_id]
                value = member.enmity[atk_type][agent.actor]
            else:
                member = target
                value = target.enmity[self.DIRECT_ATK][agent.actor][member.actor]

            self.enmities[member.id][agent.id] += value * atk_hurt

        self.last_atk_frame = self.frames

    def add_disaster(self, disaster):
        """ 添加一个灾难对象

        为环境添加一个灾难对象

        Args:
           disaster: 灾难对象
        """

        self.disasters.add(disaster)

    def damage(self, disaster, frame_data):
        """ 判断当前灾难产生的破坏

        战斗中的战斗单位的攻击动作是以灾难对象的方式存在于战场中
        当攻击方攻击时会产生一个灾难对象，灾难对象是一个向量矩形,
        以指定的速度向目标点移动, 灾难的每一次移动都有可能会造成伤害,
        具体数据在技能脚本实现

        Args:
            disaster: 灾难对象
            frame_data: 帧数据
        """

        if not disaster.finish():
            disaster.frame(frame_data)
        else:
            disaster.on_finish()
            self.disasters.remove(disaster)

    def action(self, agent):
        """ 判断当前战斗单位的动作

        当前环境会保存每个战斗单位的当前动作，每个动作都是有完成条件
        当前战斗单位不存在动作或动作结束后，重新生成一个新的动作执行

        Args:
           agent: 战斗单位对象

        Returns:
           战斗单位当前的动作
        """

        sofar = self.actions.get(agent.id)

        if not sofar or (sofar.finish() and sofar.on_finish()):
            sofar = self.opphelper_loader(agent)

            self.actions[agent.id] = sofar

        wrapper = self.wrappers.get(agent.id)

        if wrapper:
            return wrapper(sofar)

        return sofar

    def opphelper_loader(self, agent):
        """ 根据战斗单位的类型选择攻击类型

          对手选择助手,实现战斗中对手的选择和操作

        Args:
           agent: 战斗单位

        Returns:
           助手对象
        """

        if not agent.alive():
            return simple.CorpseHelper(agent, self)

        skill = agent.get_atk_skill(self)

        opper = None

        if not agent.has_attack_cd():
            opper = skill.target_match(agent, self)
            
        if opper:
            change_helper = self.atk2get(agent, opper, skill)

            return ATTACK_HELPERS[change_helper](agent, opper, self, skill)
        else:
            return defaults.ACTOR_DEFAULT_HELPER[agent.ai](agent, self, skill)

    def measure(self, atk_id, opp_id):
        """
        """

        atk_pos = self.places[atk_id]
        opp_pos = self.places[opp_id]

        return self.bf.heuristic(atk_pos, opp_pos)

    def direction2pos(self, agent, goal_pos):
        """
        """

        pos = self.places[agent.id]

        return self.bf.direction(pos, goal_pos)

    def get_blocks(self, locus=None):
        """
        """

        if locus:
            blocks = set(locus)
        else:
            blocks = set()

        for agent_id, pos in self.places.iteritems():
            if not self.has_agent_dead(agent_id):
                blocks.add(pos)

        return blocks

    def get_agent_blocks(self, goal_pos, locus=None):
        """
        """

        blocks = self.get_blocks(locus)
        blocks.discard(goal_pos)

        return blocks

    def goal_astar(self, atk_id, goal_pos, speed, locus=None):
        """
        """

        atk_pos = self.places[atk_id]
        agent = self.agents[atk_id]
        blocks = self.get_agent_blocks(goal_pos, locus)
        line = pathfind.astar(atk_pos, goal_pos, blocks, 
                                   self.bf, speed)
        return line

    def adjust_atk_pos(self, agent, skill):
        """ 调整为最佳攻击位置
        
        为了在战斗中显示较好的效果在近身英雄的默认AI上，
        会自动按
           3   7   5
           1   *   2
           4   8   6
        的顺序站位

        Args:
           agent: 攻击方英雄对象
           skill: 攻击方所使用的技能

        Returns:
           调整过后的地图编号id
           -1为不需要调整
        """

        target = self.agents.get(agent.target)

        if not target or self.has_agent_dead(target.id):
            return -1

        target_pos = self.places[target.id]
        agent_pos = self.places[agent.id]
        blocks = self.get_agent_blocks(target_pos)
        width, high = self.skill_app.skill_atk_distance(agent, target, 
                                                      skill.SKILL_ATK_DISTANCE)

        queue = self.bf.edges(agent_pos, target_pos, width, high)

        try:
            pos = next(queue)

            while pos != agent_pos:
                if pos not in blocks:
                    return pos

                pos = next(queue)
        except StopIteration:
            return -1

    def atk2get(self, atker, opper, skill):
        """
        """

        atk_pos = self.places[atker.id]
        opp_pos = self.places[opper.id]
        width, high = skill.SKILL_ATK_DISTANCE

        return self.bf.in_range(atk_pos, opp_pos, width, high)

    def trasferta_pos(self, agent, target, max_len):
        """
        """

        blocks = self.get_agent_blocks(agent)
        pos = self.places[agent.id]
        target_pos = self.places[target.id]

        return self.bf.trasferta(pos, target_pos, max_len, blocks)

    def in_agent_range(self, agent, width, high):
        """
        """

        pos = self.places[agent.id]

        return self.in_pos_range(pos, width, high)

    def in_pos_range(self, pos, width, high):
        """
        """

        for target in self.agents.itervalues():
            if self.bf.in_range(pos, self.places[target.id], width, high):
                yield target

    def lateral_pos(self, agent, target):
        """ 找到当前战斗单位与目标单位的侧面交叉点

        Args:
            agent: 战斗单位
            target: 目标单位

        Returns: 
            横向向叉点
        """

        pos = self.places[agent.id]
        target_pos = self.places[target.id]

        return self.bf.lateral_pos(pos, target_pos)

    def change_face(self, agent, goal_pos):
        """
        """
        
        pos = self.places[agent.id]

        if not self.bf.face_to(pos, goal_pos, agent.face_to):
            agent.face_to = CHANGE_FACE[agent.face_to]
            return True

        return False
