# coding: utf-8

from apps import notify as notify_app


def load(env):
    """用户首次登录
    """

    env.user.load_all()

def rename(env):
    """校验用户名是否唯一
    """

    name = env.req.get_argument('name', '')

    if isinstance(name, unicode):
        name = name.encode('utf-8')

    env.user.load_all()

    env.params['name'] = name

def enter(env):
    """初始化用户游戏数据
    """

    name = env.req.get_argument('name', '')
    role = int(env.req.get_argument('role', 1))

    if isinstance(name, unicode):
        name = name.encode('utf-8')

    env.user.hero.load_heros()
    env.user.load_all()

    env.params['name'] = name
    env.params['role'] = role
