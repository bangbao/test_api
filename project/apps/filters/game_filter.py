# coding: utf-8

from apps import screen_replace
from apps import notify as notify_app
from apps.notify import constants as notices


@notify_app.checker
def load(env):
    """用户首次登录
    """
    env.user.load_all()


@notify_app.checker
def rename(env):
    """校验用户名是否唯一
    """
    name = env.req.get_argument('name', '')

    if isinstance(name, unicode):
        name = name.encode('utf-8')

    env.user.load_all()

    name = screen_replace(name)

    env.params['name'] = name


@notify_app.checker
def enter(env):
    """初始化用户游戏数据
    """
    role = int(env.req.get_argument('role', 1))

    game_config = env.game_config
    env.user.hero.load_heros()
    env.user.load_all()

    if role not in game_config['player']:
        return notices.SYSTEM_ERROR

    env.params['role'] = role



