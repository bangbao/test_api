# coding: utf-8

from collections import defaultdict
from instantft.battle.environ import BattleEnviron
import itertools

MAX_ROUNDS = 1
FACE_TURN_KEY = 'face_turn'
WIN_GROUP = 'win_group'
ROUND = 'round'
PLAYED = 'played'
ROUND_OVER = 'round_over'
ROUND_START =  'round_start'

class AI(object):
    """ Artificial Intelligence 人工智能战斗控制器

      通过BattleField, BattleEnviron之前的关系，控制每个Agent的行动

      BattleField 控制战斗场景相关的数据，
      如:
          地形，是否可移动，测量距离
          计算移动路线
          ...

      BattleEnviron控制战斗时刻的数据，
      如:
         Agent在移动到某个点时，是否会产生战斗
         Agent在控制范围内产生最大伤害的目标
         Agent如何移动会产生较有利的伤害
         ...

      Agent:
         根据战斗环境，产生每个单位数值的改变

    Attributes:
        bf: BattleField 战斗方面的静态数据
        be: BattleEnviron 战场环境, 战斗中的动态数据
        agents: 战斗中的所有单位的集合
        attacker: 攻击方
        defender: 防守方
        teams: 当前要交战的双方数据
        frames: 所有帧数据的集合
        win: 战斗攻方是否胜利
        opening: 开场剧情
        takeabow: 完场剧情
    """

    def __init__(self, bf, skill_app, summon_hero, 
                 buff, attacker, defender, max_frames=1800):
        self.be = BattleEnviron(bf, skill_app, summon_hero, buff)
        self.attacker = attacker
        self.defender = defender
        self.frames = []
        self.alives = [True, True]
        self.winners = [[], []]
        self.max_frames = max_frames
        self.opening = None
        self.takeabow = None
        self.rounds = 0
        self.result = [0, 0]

    def over(self):
        """ 判断战斗是否结束

        Returns:
            战斗是否结束
        """

        return self.rounds > MAX_ROUNDS

    def working(self):
        """ 运行ai

        当内部战斗没结束时，运行ai来得到战斗数据
        """

        teams = [self.attacker[self.rounds],
                 self.defender[self.rounds]]

        win_group = self.round(teams)

        for agent_id in itertools.ifilterfalse(self.be.has_agent_dead, 
                                          self.be.groups[win_group]):
            self.winners[win_group].append(self.be.agents[agent_id])

        self.result[win_group] += 1

    def round(self, teams):
        """ 计算一回合战斗的数据

        Args:
           teams: 当前回合攻守双方阵容
        """

        frames = 1
        alives = map(any, teams)

        self.be.init()

        round_data = {
            ROUND_START: {
                ROUND: self.rounds,
                PLAYED: (),
            }
        }

        self.be.formations(teams)

        if all(alives):
            round_data[ROUND_START][PLAYED] = self.be.init_battle()

            self.frames.append(round_data)
            self.be.frame_up()

            while frames < self.max_frames and all(alives):
                alives = self.frame()
                frames += 1

            alives = self.frame()
        else:
            self.frames.append(round_data)
            self.be.frame_up()

        win_group = int(alives[self.be.DEFEND_GROUP])

        self.frames.append({ROUND_OVER: {
            ROUND: self.rounds,
            WIN_GROUP: win_group,
        }})

        self.rounds += 1

        return win_group

    def has_final(self):
        """ 判断战役是否需要进行最终决战

        Returns:
            是否需要最终决斗
        """

        return all(self.winners)

    def final(self):
        """ 决战回合

        决战回和比较特殊,由前两战双方存活的武将进行
        最终决斗
        """

        win_group = self.round(self.winners)
        self.result[win_group] += 1

    def frame(self):
        """ 生成战斗每一帧的动作

          所有Agent都会有一次行动的机会

        Returns:
          当前攻守双方的存活状态
        """

        alives = [False, False]
        data = defaultdict(dict)
        face_turn = {}
        agents = self.be.get_action_agents()
        disasters = self.be.get_action_disasters()

        for disaster in disasters:
            self.be.damage(disaster, data)

        for agent in agents:
            manipulate = self.be.action(agent)
            action = manipulate.frame()
            manipulate.rel()

            for agent_id, frame in action.frames():
                action.frame_update(self, data, frame, agent_id)

            alives[agent.gid] = True
            target_pos = action.get_target_pos()

            if target_pos > 0 and self.be.change_face(agent, target_pos):
                face_turn[agent.id] = agent.face_to

            agent.bout()

        if face_turn:
            data[FACE_TURN_KEY] = face_turn

        self.be.frame_up(data)
        self.frames.append(dict(data))

        return alives

    def record(self):
        """ 组装成前端播放数据格式

        Returns:
          {
            bf: 战场地图数据
            fight: {
              len: 总长度
              frames: 帧数据
              win: 是否胜利
              falls: 阵亡人数
            }
          }
        """

        return {
            'bf': self.be.bf_status(self.be.init_status),
            'fight': {
                'len': len(self.frames),
                'frames': self.frames,
                'win': cmp(*self.result) > 0,
                'falls': len(self.be.deads[self.be.ATTACK_GROUP]),
            }
        }
