# coding: utf-8
from instantft.battle.timer import Train
from instantft.battle.timer import Lateral
from instantft.ai.helper.opp import simple
from instantft.ai.action.dead import DeadAction
from cheetahes.utils import sys_random as random
from base import BaseDisaster
from simple import BulletDisaster
from simple import AttackDisaster
import itertools

class SummonDisaster(BaseDisaster):
    """
    """

    SPEED = 1
    ROUNDS = 1
    DIE_KEY = DeadAction.FIELD_NAME
    
    def __init__(self, atk_action, speed, rounds, life_frames):
        """
        """
        
        self.be = atk_action.be
        self.agent = atk_action.agent
        self.opper = atk_action.opper
        self.skill = atk_action.skill
        self.bulle = BulletDisaster(atk_action, speed, rounds)
        self.timer = Train(life_frames, self.SPEED, self.ROUNDS)

        self.summoned = False
        self.targets = []

    def finish(self):
        """
        """

        return self.summoned and self.timer.stop()

    def frame(self, data):
        """
        """

        if not self.summoned:
            if not self.bulle.finish():
                self.bulle.frame(data)
            else:
                self.summoned = True

                total_kicks = []
                
                for i in xrange(self.skill.SKILL_SUMMONS):
                    hero_id = random.choice(self.skill.SKILL_SUMMON_HEROS)
                    birth_pos, kicks = self.skill.summon_birth(self.be, self.agent, 
                                                               self.opper)

                    total_kicks.extend(kicks)

                    target = self.be.new_agent(hero_id, self.agent, birth_pos)
                    action = simple.BirthHelper(target, self.be)
                    self.be.set_action(target.id, action)
                    self.targets.append(target.id)

                for kicker, kick_pos in total_kicks:
                    action = simple.KickerHelper(kicker, self.be, kick_pos)
                    self.be.set_action(kicker.id, action)
        else:
            if self.timer.move():
                for target_id in self.targets:
                    target = self.be.die_agent(target_id)

                    if target.alive():
                        data[target_id] = {self.DIE_KEY: None}

class TransformDisaster(BaseDisaster):
    """
    """

    def __init__(self, atk_action, speed, rounds, high, actions):
        self.be = atk_action.be
        self.high = high
        self.agent = atk_action.agent
        self.opper = atk_action.opper
        self.skill = atk_action.skill
        self.current_pos = self.be.places[self.agent.id]
        self.target_pos = atk_action.get_target_pos()
        self.delay = atk_action.total_frame - 1
        self.actions = actions

        distance = self.be.bf.straight_distance(self.current_pos, 
                                                self.target_pos)

        face_to = 1

        if self.be.bf.face_to(self.current_pos, self.target_pos, self.agent.face_to):
            face_to = -1

        self.timer = Lateral(distance, speed, rounds, face_to)

    def finish(self):
        """
        """

        return self.timer.stop()

    def frame(self, data):
        """
        """

        if self.delay < 1:
            self.be.set_action(self.agent.id, self.actions[0])
            for width, distance in self.timer.move():
                self.current_pos += distance
                targets = self.skill.hit_range(self.be, self.current_pos, 
                                           width, self.high)
                hurts = self.agent.attack_to(self.skill, self.be, *targets)

                self.frame_update(data, hurts)
        else:
            self.delay -= 1

    def on_finish(self):
        """
        """

        self.be.set_agent_pos(self.agent, self.target_pos)
        self.be.set_action(self.agent.id, self.actions[1])

class Suicide(AttackDisaster):
    """ 自杀式灾难
    """

    def __init__(self, atk_action, adjust_func, frames=1):
        super(Suicide, self).__init__(atk_action, frames)
        
        self.adjust_func = adjust_func

    def on_finish(self):
        """
        """

        corpse = simple.CorpseHelper(self.agent, self.be)

        self.adjust_func(self.be, self.agent, self.opper)
        self.agent.to_dead()
        self.be.set_action(self.agent.id, corpse)

class Migrate(BaseDisaster):
    """ 转移式灾难

    将指定的目标在地图上转移到指定位置
    """

    def __init__(self, atk_action):
        self.be = atk_action.be
        self.agent = atk_action.agent
        self.opper = atk_action.opper
        self.skill = atk_action.skill

        distance = self.be.bf.straight_distance(
            self.be.places[self.agent.id],
            self.be.places[self.opper.id])

        self.first = Train(distance, start_speed, start_rounds)
        self.second = Train(distance, after_speed, after_rounds)
        self.targets = None

    def frame(self, data):
        """
        """

        if self.first.move():
            if self.second:
                self.targets = self.skill.hit_range(self.agent, self.opper, self.be)
                self.first, self.second = self.second, None
            else:
                pass

    def finish(self):
        """
        """

        return not self.second and \
            self.first.stop()

    def on_finish(self):
        """
        """

        pass
