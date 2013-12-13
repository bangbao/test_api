# coding: utf-8

from lib.db.fields import ModelDict
from . import logics
from .models import User, NewUser

COOKIE_AUTH_KEY = 'sign_data'


def auth(env, req):
    """用户签名验证

    使用cookie验证, sign_data为'用户uid|签名sign'的组合，用户登录成功时会写入cookie
    验证流程：
        通过uid取出用户数据，用用户标识token, 及创建用户时生成的salt，再加上uid
        生成签名，与此签名比较， 相等刚验证通过

    Args:
        env: 运行环境
        sign_data: 签名数据

    Returns:
        用户对象
    """
    user_token = req.get_argument('user_token', '')
    sign_data = req.get_cookie(COOKIE_AUTH_KEY)

    if not user_token or not sign_data:
        return None

    uid_str, sign = sign_data.split('|')
    uid = int(uid_str)
    user = get_user(env, uid)

    new_sign = logics.build_signature(user_token, user.data['salt'], uid)

    if sign == new_sign:
        user.load_base()
        return user


def login(env, req):
    """用户登录

    根据用户标识token取出用户数据，按一定顺序生成签名，写入到cookie中

    Args:
        env: 运行环境
        req: APIRequestHandler实例

    Returns:
        用户对象
    """
    user_token = req.get_argument('user_token', '')
    password = req.get_argument('password', '')

    if not user_token:
        return None

    uid = get_uid(env, user_token, password)
    user = get_user(env, uid)

    sign = logics.build_signature(user.data['token'], user.data['salt'], uid)

    sign_data = "%s|%s" % (uid, sign)
    req.set_cookie(COOKIE_AUTH_KEY, sign_data)

    user.load_base()

    return user


def get_uid(env, token, password):
    """取出或创建 token 对应的用户uid

    先从数据库中查找token记录， 若不存在则创建记录。 返回记录的id

    Args:
        env: 运行环境
        token: 用户标识
        password: 密码

    Returns:
        token 对应的 uid
    """
    connection = env.storage.connects.get(ModelDict, User)
    cursor = connection.cursor()

    query = "SELECT id FROM %s_%s WHERE token='%s'" % (User.NAME, User.FIELD_KEY, token)
    cursor.execute(query)
    data = cursor.fetchone()

    if data:
        return data['id']

    return NewUser.create(env, token, password)


def get_user(env, uid, read_only=False):
    """
    """
    user = User(env, uid, read_only)
    user.load_data()
    user.load(env)

    return user


def user_info(env):
    """用户角色信息

    Args:
        env: 运行环境

    Returns:
        用户角色信息
    """
    user = env.user
    user.save_all()
    game_app = env.import_app('game')
    adven_app = env.import_app('adven')

    result_data = {
        'user': {'uid': env.user.pk},
        'game': game_app.get_game_data(user),
        'adven': adven_app.get_adven_record(user),
        'hero': {
            'hero_len': 100,
        },
        'pet': {
            'pet_len': 100,
        },
        'arena': {
            'rank': user.arena.data['rank'],
        },
    }

    return result_data


