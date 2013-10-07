# coding: utf-8


def pets(env):
    """宠物背包
    """
    user = env.user
    pet_app = env.import_app('pet')

    pet_app.check_pet_full(user)
    user.save_all()

    return {
        'pet': pet_app.get_played_pet(user),
        'pets': pet_app.format_pets(user, user.hero.pets.iterkeys()),
        'items': pet_app.format_items(user),
    }


def played(env):
    """指定出战的宠物
    """
    user = env.user
    pet_id = env.params['pet_id']
    pet_app = env.import_app('pet')

    pet_app.set_played_pet(user, pet_id)
    user.save_all()

    return {
        'pet': pet_app.get_played_pet(user),
    }


def feed(env):
    """宠物喂养
    """
    user = env.user
    game_config = env.game_config
    item_id = env.params['item_id']
    pet_id = env.params['pet_id']
    hero_app = env.import_app('hero')
    pet_app = env.import_app('pet')

    pet_obj = env.user.hero.pets[pet_id]
    food_detail = game_config['item'][item_id]
    pet_detail = pet_app.logics.get_pet_detail(pet_obj, game_config)

    food_effect = pet_app.add_food_effect(pet_obj, pet_detail, food_detail)
    pet_obj = pet_app.logics.pet_upgrade(pet_obj, game_config)

    user.hero.pets.modify(pet_id, **pet_obj)
    hero_app.incr_item(user, item_id, -1)

    user.save_all()

    return {
        'food_effect': food_effect,
        'pet': pet_app.get_played_pet(user),
        'pets': pet_app.format_pets(user, [pet_id]),
        'items': pet_app.format_items(user),
    }


def clone(env):
    """宠物繁衍
    """
    pass


def refresh_skill(env):
    """刷新技能
    """
    user = env.user
    game_config = env.game_config
    pet_id = env.params['pet_id']
    skill_pos = env.params['pos']
    pet_app = env.import_app('pet')

    pet_obj = user.hero.pets[pet_id]
    detail = pet_app.logics.get_pet_detail(pet_obj, game_config)
    skills = pet_app.logics.skill_get(pet_obj)
    skill_sets = game_config['pet_skill_star'][detail['star']]

    skills[skill_pos] = pet_app.logics.random_skill(skill_sets, exclude=skills)
    pet_app.logics.skill_set(pet_obj, skills)
    user.hero.pets.modify(pet_id, skill=pet_obj['skill'])

    user.save_all()

    return {
        'pets': pet_app.format_pets(user, [pet_id]),
    }


def remove_skill(env):
    """删除技能
    """
    user = env.user
    pet_id = env.params['pet_id']
    skill_pos = env.params['pos']
    pet_app = env.import_app('pet')

    pet_obj = user.hero.pets[pet_id]
    skills = pet_app.logics.skill_get(pet_obj)

    skills[skill_pos] = None
    pet_app.logics.skill_set(pet_obj, skills)
    user.hero.pets.modify(pet_id, skill=pet_obj['skill'])

    user.save_all()

    return {
        'pets': pet_app.format_pets(user, [pet_id]),
    }

