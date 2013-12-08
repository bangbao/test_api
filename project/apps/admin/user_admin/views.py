# coding: utf-8

import constants
from apps.admin import handle
from lib.db.fields import ModelDict
from apps.user.models import User

TEMPLATE = 'admin/user/usermain.html'

def index(env, msg=None):
    """用户列表
    """

    connection = env.storage.connects.get(ModelDict, User)
    cursor = connection.cursor()

    query = "SELECT id, username FROM %s_%s" % (User.NAME, User.FIELD_KEY)

    cursor.execute(query)
    user_data = cursor.fetchall()

    return env.render(TEMPLATE, {'user_data': user_data, 'msg': msg})

def reset(env):
    """重置用户相关的数据
    """

    uid = env.req.get_argument('uid', '')

    user = getmodel(uid, env)
    user.reset_all_data()

    return index(env, msg=handle.MSG['SUCCESS'])

def getmodel(uid, env):
    """获取并处理user，加载必要的数据
    """

    user_app = env.import_app('user')
    user = user_app.get_user(env, int(uid))

    return user
