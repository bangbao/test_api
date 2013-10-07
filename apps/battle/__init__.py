# coding: utf-8
from instantft.ai import AI
from instantft.battle.field import BattleField
from instantft.battle.buff import Buff
from agents.base import (MAGE_AGENT,
                         WARRIOR_AGENT,
                         PASTOR_AGENT,
                         ROBBER_AGENT,
                         KNIGHT_AGENT,
                         RANGER_AGENT,
                         CATAPULT_AGENT,
                         COMMON_AGENT)
import agents

AGENT_MAPPING = {
    MAGE_AGENT: agents.MageAgent,
    WARRIOR_AGENT: agents.WarriorAgent,
    PASTOR_AGENT: agents.PastorAgent,
    ROBBER_AGENT: agents.RobberAgent,
    KNIGHT_AGENT: agents.KnightAgent,
    RANGER_AGENT: agents.RangerAgent,
    CATAPULT_AGENT: agents.CatapultAgent,
    COMMON_AGENT: agents.CommentAgent,
}


def create_agent(agent_job, **kwargs):
    """生成一个战斗agent

    Args:
        agent_job: 职业
        kwargs: 战斗agent所需数据集合

    Returns:
        战斗agent
    """
    cls = AGENT_MAPPING[agent_job]
    obj = cls(**kwargs)

    return obj


def battle(env, map_info, attacker, defender, **kwargs):
    """获取战斗数据

    Args:
        env: 运行环境
        map_info: 战斗所在地图配置
        attacker: 攻击阵容
        defender: 防御阵容
        kwargs: 扩展参数
            max_frames: 最大帧数默认3分钟
            polt_name:  剧情脚本名称

    Returns:
        战斗数据
    """
    max_frames = kwargs.get('max_frames', 1800)
    polt_name = kwargs.get('polt_name', 'stage10001')

    skill_app = env.import_app('skill')
    hero_app = env.import_app('hero')
    polt_app = env.import_app('polt')
    skill_buff = env.game_config['skill_buff']
    summon_hero = hero_app.summon_hero(env)
    buff = Buff(skill_buff)
    polt = polt_app.get_polt(polt_name)
    bf = BattleField(map_info)
    ai = AI(bf, skill_app, summon_hero, buff, 
            attacker, defender, max_frames)

    while not ai.over():
        ai.working()

    if ai.has_final():
        ai.final()

    if polt.opening:
        ai.opening = polt.opening.record(summon_hero, ai.be)

    if polt.takeabow:
        ai.takeabow = polt.takeabow.record(summon_hero, ai.be)

    return ai

