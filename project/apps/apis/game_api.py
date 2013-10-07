# coding: utf-8


def load(env):
    """用户首次登录
    """
    user_app = env.import_app('user')

    game_enter = bool(env.user.game.info['enter'])
    result_data = {'game_enter': game_enter}

    if game_enter:
        result_data.update(user_app.user_info(env))

    return result_data


def rename(env):
    """校验用户名是否唯一
    """
    user = env.user
    name = env.params['name']
    user.game.info['username'] = name
    user.data['username'] = name

    env.storage.save(user)
    user.save_all()

    return {
        'name': env.params['name'],
    }


def enter(env):
    """初始化用户游戏数据

    Args:
        name: 用户昵称
        role: 用户角色

    Returns:
        用户信息
    """
    user = env.user
    role = env.params['role']
    role_config = env.game_config['player'][role]
    user_config = env.game_config['user'][role_config['level']]
    user_app = env.import_app('user')
    hero_app = env.import_app('hero')
    team = []

    # 如果用户已经注册过， 直接登录
    if env.user.game.info['enter']:
        return user_app.user_info(env)

    for hero_cfg_id in role_config['team']:
        obj = hero_app.birth_hero(user, hero_cfg_id,
                                  where=hero_app.constants.HERO_FROM_INIT,
                                  ext=role)
        team.append(obj['hero_id'])

    for hero_cfg_id, level in role_config['heros']:
        hero_app.birth_hero(user, hero_cfg_id,
                            where=hero_app.constants.HERO_FROM_INIT,
                            ext=role,
                            level=level)

    user_game = user.game
    user_game.user['kcoin'] = role_config['kcoin']
    user_game.user['level'] = role_config['level']
    user_game.user['gold'] = role_config['gold']

    user_game.info['energy'] = user_config['energy']
    user_game.info['exp'] = user_config['exp']
    user_game.info['role'] = role
    user_game.info['enter'] = 1

    hero_app.team_put(user, team)
    user.save_all()

    return user_app.user_info(env)

