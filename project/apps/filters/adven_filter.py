# coding: utf-8

import itertools

from apps import notify as notify_app
from apps.notify import constants as notices


@notify_app.checker
def world_map(env):
    """世界地图
    """
    user_adven = env.user.adven
    user_adven.load_adven()
    user_adven.load_readven()
    user_adven.load_data()
    env.user.load_all()


@notify_app.checker
def area_map(env):
    """区域地图
    """
    env.params['area'] = int(env.req.get_argument('area', 1))

    user_adven = env.user.adven
    user_adven.load_adven()
    user_adven.load_readven()
    user_adven.load_data()
    env.user.load_all()


@notify_app.checker
def chapter_map(env):
    """章节地图
    """
    env.params['area'] = int(env.req.get_argument('area', 1))
    env.params['chapter'] = int(env.req.get_argument('chapter', 1))

    user_adven = env.user.adven
    user_adven.load_adven()
    user_adven.load_readven()
    user_adven.load_data()
    env.user.load_all()


@notify_app.checker
def stage(env):
    """攻关前页面
    """
    env.params['area'] = int(env.req.get_argument('area', 1))
    env.params['chapter'] = int(env.req.get_argument('chapter', 1))
    env.params['stage'] = int(env.req.get_argument('stage', 1))
    select = env.req.get_argument('select', 'light')

    user = env.user
    user.load_fight()
    user.adven.load_readven(keys=[env.params['chapter']])
    user.adven.load_data(keys=[env.params['stage']])
    user.load_all()

    hero_app = env.import_app('hero')
    env.params['user_team'] = hero_app.team_get(user)
    env.params['select'] = select


@notify_app.checker
def fight(env):
    """攻关战斗
    """
    members = env.req.get_arguments('members')
    area = int(env.req.get_argument('area', 1))
    chapter = int(env.req.get_argument('chapter', 1))
    stage = int(env.req.get_argument('stage', 1))
    select = env.req.get_argument('select', 'light')

    hero_app = env.import_app('hero')
    members = hero_app.logics.rectify_team(members)

    user = env.user
    user.load_fight(members=members)
    user.adven.load_readven(keys=[chapter])
    user.adven.load_data(keys=[stage])
    env.user.load_all()

    stage_cost = env.game_config['stages'][stage]['cost']

    if user.game.user['energy'] < stage_cost['energy']:
        return notices.ADVEN_FIGHT_NOT_ENOUGH_ENERGY

    member_not_exists = False

    for member in itertools.ifilter(None, members):
        if member not in user.hero.heros:
            member_not_exists = True
            break

    if any(members) and not member_not_exists:
        env.params['members'] = members
    else:
        env.params['members'] = hero_app.team_get(user)

    env.params['area'] = area
    env.params['chapter'] = chapter
    env.params['stage'] = stage
    env.params['select'] = select



