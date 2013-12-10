# coding: utf-8

from apps import notify as notify_app
from apps.notify import constants as notices


@notify_app.checker
def pets(env):
    """宠物界面
    """
    user = env.user
    user.hero.load_pets()
    user.hero.load_items()
    user.load_all()


@notify_app.checker
def played(env):
    """更换出战宠物
    """
    pet_id = env.req.get_argument('pet_id')

    user = env.user
    user.hero.load_pets(keys=[pet_id])
    user.load_all()

    if not pet_id in user.hero.pets:
        return notices.KCOIN_NOT_ENOUGH

    env.params['pet_id'] = pet_id


@notify_app.checker
def feed(env):
    """喂养宠物
    """
    pet_id = env.req.get_argument('pet_id')
    item_id = int(env.req.get_argument('item_id'))

    user = env.user
    user.hero.load_pets(keys=[pet_id])
    user.hero.load_items()
    user.load_all()

    game_config = env.game_config
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

    env.params['pet_id'] = pet_id
    env.params['item_id'] = item_id


@notify_app.checker
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


@notify_app.checker
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

