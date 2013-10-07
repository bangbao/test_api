# coding: utf-8

from apps import notify as notify_app
from apps.notify import constants as notices


def pets(env):
    """宠物界面
    """

    user = env.user
    user.hero.load_pets()
    user.hero.load_items()
    user.load_all()

def played(env):
    """更换出战宠物
    """

    pet_id = env.req.get_argument('pet_id')

    user = env.user
    user.hero.load_pets(keys=[pet_id])
    user.load_all()

    env.params['pet_id'] = pet_id

    return check_played(env, pet_id)

def feed(env):
    """喂养宠物
    """
    pet_id = env.req.get_argument('pet_id')
    item_id = int(env.req.get_argument('item_id'))

    user = env.user
    user.hero.load_pets(keys=[pet_id])
    user.hero.load_items()
    user.load_all()

    env.params['pet_id'] = pet_id
    env.params['item_id'] = item_id

    return check_feed(env, pet_id, item_id, env.game_config)

def refresh_skill(env):
    """刷新技能
    """
    pet_id = env.req.get_argument('pet_id')
    pos = int(env.req.get_argument('pos'))

    user = env.user
    user.hero.load_pets(keys=[pet_id])
    user.load_all()

    env.params['pet_id'] = pet_id
    env.params['pos'] = pos

def remove_skill(env):
    """删除一个技能
    """
    pet_id = env.req.get_argument('pet_id')
    pos = int(env.req.get_argument('pos'))

    user = env.user
    user.hero.load_pets(keys=[pet_id])
    user.load_all()

    env.params['pet_id'] = pet_id
    env.params['pos'] = pos


@notify_app.checker
def check_played(env, pet_id):
    """检查是否可以更换宠物出战
    """

    user = env.user

    if not pet_id in user.hero.pets:
        return notices.KCOIN_NOT_ENOUGH

@notify_app.checker
def check_feed(env, pet_id, item_id, game_config):
    """检查是否可以喂养宠物
    """

    user_hero = env.user.hero
    pet_app = env.import_app('pet')
    pet_obj = user_hero.pets.get(pet_id)

    if not pet_obj:
        return notices.KCOIN_NOT_ENOUGH

    detail = pet_app.logics.get_pet_detail(pet_obj, game_config)

    if pet_obj['full'] >= detail['full']:
        return notices.KCOIN_NOT_ENOUGH

    item_obj = user_hero.items.get(item_id)

    if not item_obj or item_obj['num'] < 1:
        return notices.KCOIN_NOT_ENOUGH


