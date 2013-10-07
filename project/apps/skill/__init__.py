# coding: utf-8
"""
全局技能脚本模块, 实现技能相关调用

PWD: 当前文件对目标，用来加载技能脚本
skill_caches: 技能脚本模块的缓存，不会重复生成
"""

import os
import sys
import imp

PWD = [os.path.abspath(os.path.dirname(__file__))]

skill_caches = {}

def get_skill(skill_config):
    """ 根据技能配置获取到技能脚本的模块

    技能脚本动态编写，根据战场环境动态控制内容

    Args:
       skill_config: 技能配置

    Returns:
       技能脚本模块对象
    """

    effective = skill_caches.get(skill_config['effective'])

    if not effective:
        module = skill_config['effective']
        effective = imp.load_module(module, *imp.find_module(module, PWD))
        setattr(effective, 'skill_effect', skill_config['effect'])

        skill_caches[module] = sys.modules.pop(module)

    return effective

def skill_atk_distance(agent, target, distances):
    """ 根据角色计算合理的攻击范围

    技能的攻击范围是固定的，但占位大的角色可以增加技能的距离

    Args:
       agent: 战斗单位对象
       target: 攻击目标
       distances: 技能的有效攻击范围

    Returns:
       战斗单位使用技能时的有效攻击范围

    TODO:
       添加target参数，之前算使用的是一个点，应该攻击目标的所有占位  张建
    """

    width, high = distances

    return width, high

if __name__ == "__main__":
    agent = type('agent', (), {'width': 5, 'high': 5})
    target = type('agent', (), {'width': 5, 'high': 5})

    print skill_atk_distance(agent, target, (80, 30))
