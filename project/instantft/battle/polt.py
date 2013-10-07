# coding: utf-8
from collections import defaultdict
from instantft.ai.action.move import MoveAction
from instantft.ai.action.dead import DeadAction
from instantft.ai.action.idle import IdleAction
from instantft.ai.action.birth import BirthAction
from instantft.ai.action.simple import HideAction
from instantft.ai.action.simple import AppearAction
from instantft.ai.helper.disaster.base import BaseDisaster
from instantft.ai import ROUND
from instantft.ai import PLAYED
from instantft.ai import WIN_GROUP
from instantft.ai import ROUND_OVER
from instantft.ai import ROUND_START
from instantft.ai import FACE_TURN_KEY
import itertools

ATTACK_GROUP = 0
DEFENSE_GROUP = 1

class Polt(object):
    def __init__(self):
        """
        """

        self.agents = []
        self.chunks = [[]]
        self.positions = {}
        self.groups = {}
        self.current = defaultdict(dict)
        self.mx_len = 0
        self.my_len = 0
        self.sky_len = 0
        self.counter = 0
        self.new_chunk = False
        self.b_points = defaultdict(list)
        self.data = None

    def set_mapinfo(self, x, y, sky, pixel, attack, defend):
        self.mx_len = x
        self.my_len = y - sky
        self.sky_len = sky
        self.map_pixel = pixel
        self.mf_attack = {'x': attack[0], 'y': attack[1]}
        self.mf_defend = {'x': defend[0], 'y': defend[1]}

    def trans2pos(self, x, y):
        return y * self.mx_len + x

    def birth_agent(self, conf_id, x, y):
        pos = self.trans2pos(x, y)
        agent_id = self.counter
        self.counter += 1
        self.current[agent_id][BirthAction.FIELD_NAME] = None
        self.new_chunk = True
        idx = len(self.chunks)
        self.positions[agent_id] = pos
        self.b_points[idx].append((agent_id, conf_id))

        return agent_id

    def add_agent(self, conf_id, x, y):
        """
        """

        pos = self.trans2pos(x, y)
        agent_id = self.counter

        self.counter += 1
        self.agents.append(conf_id)
        self.positions[agent_id] = pos

        return agent_id

    def set_atk_group(self, *agents):
        """
        """

        for agent_id in agents:
            self.groups[agent_id] = ATTACK_GROUP

    def set_def_group(self, *agents):
        """
        """

        for agent_id in agents:
            self.groups[agent_id] = DEFENSE_GROUP

    def face_to_left(self, *agents):
        """
        """

        self.current[FACE_TURN_KEY] = dict.fromkeys(agents, DEFENSE_GROUP)

    def face_to_right(self, *agents):
        """
        """

        self.current[FACE_TURN_KEY] = dict.fromkeys(agents, ATTACK_GROUP)

    def new_frame(self):
        """
        """

        if self.new_chunk:
            self.chunks.append([])
            self.new_chunk = False

        self.chunks[-1].append(dict(self.current))
        self.current = defaultdict(dict)

    def move(self, agent_id, coordinate_list, frames):
        """
        """

        positions = []
        
        for x, y in coordinate_list:
            positions.append(self.trans2pos(x, y))

        self.current[agent_id][MoveAction.FIELD_NAME] = [positions, frames]

    def idle(self, agent_id):
        """
        """

        self.current[agent_id][IdleAction.FIELD_NAME] = None

    def dialog(self, agent_id, *content):
        """
        """

        self.current[agent_id]['dialog'] = content

    def aside(self, *content):
        """
        """

        self.current['aside'] = content

    def dead(self, *agents):
        """
        """

        for agent_id in agents:
            self.current[agent_id][DeadAction.FIELD_NAME] = None

    def attack1(self, agent_id, target_id, effect):
        self.current[agent_id]['attack1'] = [target_id, 0, effect]

    def attack2(self, agent_id, target_id, effect):
        self.current[agent_id]['attack2'] = [target_id, 0, effect]

    def attack3(self, agent_id, target_id, effect):
        self.current[agent_id]['attack3'] = [target_id, 0, effect]

    def hide(self, agent_id):
        """
        """

        self.current[agent_id][HideAction.FIELD_NAME] = None

    def appear(self, agent_id, x, y):
        """
        """

        self.current[agent_id][AppearAction.FIELD_NAME] = self.trans2pos(x, y)

    def hurt(self, agent_id, effect, value, storm=0):
        """
        """

        if not BaseDisaster.HURT_FIELD_NAME in self.current[agent_id]:
            self.current[agent_id][BaseDisaster.HURT_FIELD_NAME] = {}

        self.current[agent_id][BaseDisaster.HURT_FIELD_NAME][effect] = [[value, storm]]

    def record(self, summon_hero, be):
        if not self.data:
            self.finish(summon_hero, be)

        return self.data
        
    def finish(self, summon_hero, be):
        if self.current:
            self.new_frame()

        init_data = {}
        played = []

        for agent_id, conf_id in enumerate(self.agents):
            agent = summon_hero(conf_id, 1)
            init_data[agent_id] = {
                'hp': agent.hp,
                'hurt': agent.hurt,
                'face_to': self.groups[agent_id],
                'gid': self.groups[agent_id],
                'move_speed': agent.move.step,
                'atk_speed': agent.atk_cd.step,
                'res': agent.res,
                'actor': agent.actor,
                'bf_init': agent.bf_init
            }
            played.append((agent_id, self.positions[agent_id]))

        for frame, object_list in self.b_points.iteritems():
            for agent_id, conf_id in object_list:
                agent = summon_hero(conf_id, 1)
                self.chunks[frame][0][agent_id][BirthAction.FIELD_NAME] = {
                    'hp': agent.hp,
                    'hurt': agent.hurt,
                    'face_to': self.groups[agent_id],
                    'gid': self.groups[agent_id],
                    'move_speed': agent.move.step,
                    'atk_speed': agent.atk_cd.step,
                    'res': agent.res,
                    'pos': self.positions[agent_id],
                    'actor': agent.actor,
                    'bf_init': agent.bf_init
                }

        round_start = ({
            ROUND_START: {
                ROUND: 0,
                PLAYED: played,
            }
        },)

        frames = list(itertools.chain(round_start, *self.chunks))
        frames.append({ROUND_OVER: {
            ROUND: 0,
            WIN_GROUP: 0,
        }})

        self.data = {
            'bf': {
                'size': (self.mx_len, self.my_len + self.sky_len),
                'pixel': self.map_pixel,
                'sky': self.sky_len,
                'focus': {
                    'attack': self.mf_attack,
                    'defend': self.mf_defend,
                },
                'init': init_data
            },
            'fight': {
                'frames': frames,
                'len': len(frames),
            }
        }

        self.chunks = None

if __name__ == "__main__":
    polt = Polt()
    polt.dialog(0, "你大爷你要爆啊！", "我跟你说过你真的完了！")
    polt.dialog(1, "大哥我们搞定他！")
    polt.move(0, [35, 34, 54], 10)
    polt.move(1, [35, 34, 54], 10)
    polt.idle(2)
    polt.idle(3)
    polt.new_frame()
    polt.attack(0)
    polt.attack(1)
    polt.hurt(2, 'a', 90)
    polt.hurt(3, 'a', 90)
    polt.new_frame()
    polt.idle(0)
    polt.idle(1)
    polt.dead(2)
    polt.dead(3)

    print polt.record()
