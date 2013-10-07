# coding: utf-8


def item_info(user, goods_id):
    """获取用户卡牌材料信息

    Args:
        user: 用户
        goods_id: 材料ID
    """
    env = user.env
    goods_config = env.game_config['item'][goods_id]

    goods = {
        'id': goods_id,
        'name': goods_config['name'],
        'icon': goods_config['icon']
    }

    return goods


def material_info(user, goods_id):
    """获取用户装备材料信息

    Args:
        user: 用户
        goods_id: 材料ID
    """
    env = user.env
    goods_config = env.game_config['equip_material'][goods_id]

    goods = {
        'id': goods_id,
        'name': goods_config['name'],
        'star': goods_config['star'],
        'icon': goods_config['icon']
    }

    return goods


def goblin_info(user, goods_id):
    """获取用户地精零件信息

    Args:
        user: 用户
        goods_id: 材料ID
    """
    env = user.env
    user.hero.load_goblins()
    user.hero.load(env)

    goods = user.hero.goblins[goods_id]
    cfg_id = goods['cfg_id']
    goods_config = env.game_config['goblins'][cfg_id]

    goods['name'] = goods_config['name']
    goods['star'] = goods_config['star']
    goods['image'] = goods_config['image']

    return goods


def equip_info(user, goods_id):
    """获取用户装备信息

    Args:
        user: 用户
        goods_id: 装备ID
    """
    env = user.env
    user.hero.load_equips()
    user.hero.load(env)

    goods = user.hero.equips[goods_id]
    cfg_id = goods['cfg_id']
    goods_config = env.game_config['equips'][cfg_id]

    goods['name'] = goods_config['name']
    goods['star'] = goods_config['star']
    goods['image'] = goods_config['image']

    return goods


def stage_info(user, goods_id):
    """获取关卡信息

    Args:
        user: 用户
        goods_id: 关卡ID
    """
    env = user.env
    stage_config = env.game_config['stages'][goods_id]

    stage = {
        'id': goods_id,
        'name': stage_config['name'],
        'chapter': stage_config['chapter'],
        'area': stage_config['area'],
        'cost': stage_config['cost'],
        'difficult': stage_config['difficult'],
    }

    return stage


def hero_info(user, goods_id):
    """获取卡牌信息

    Args:
        user: 用户
        goods_id: 卡牌ID
    """
    env = user.env
    user.hero.load_heros()
    user.hero.load(env)

    goods = user.hero.heros[goods_id]
    cfg_id = goods['cfg_id']
    goods_config = env.game_config['heros'][cfg_id]

    goods['name'] = goods_config['name']
    goods['star'] = goods_config['star']
    goods['image'] = goods_config['image']

    return goods


def player_info(user, goods_id):
    """获取玩家信息

    Args:
        user: 用户
        goods_id: 玩家ID
    """
    env = user.env
    user_app = env.import_app('user')
    player = user_app.get_user(env, goods_id)
    
    player.game.load_info()
    player.game.load_user()
    player.game.load(env)

    info = {
        'username': player.game.info['username'],
        'level': player.game.user['level'],
    }

    return info

