# coding: utf-8

from apps.admin import handle
from apps.admin.form import Form
from lib.db.fields import ModelDict
from apps.user.models import User

import logics
import constants


def index(env, msg=None):
    """用户列表
    """
    connection = env.storage.connects.get(ModelDict, User)
    cursor = connection.cursor()

    query = "SELECT id, username, token FROM %s_%s" % (User.NAME, User.FIELD_KEY)

    cursor.execute(query)
    user_data = cursor.fetchall()
    user_data = (logics.userinfo(getmodel(env, obj['id']), **obj)
                 for obj in user_data)

    return env.render('admin/user/index.html',
                      {'user_data': user_data, 'msg': msg})

def show(env, msg=None):
    """显示用户选定数据
    """
    uid = env.req.get_argument('uid')
    field = env.req.get_argument('field', 'game.user')

    user = getmodel(env, uid, field)

    data = {
        'user_field': constants.USER_FIELD,
        'user': user,
        'field': field,
        'form': logics.get_form(user, field),
        'msg': msg,
    }

    return env.render('admin/user/show.html', data)

def modify(env):
    """修改用户数据
    """
    uid = env.req.get_argument('uid')
    field = env.req.get_argument('field')
    submit = env.req.get_argument('submit')

    user = getmodel(env, uid, field)
    field_obj = eval('user.%s' % field)
    form = constants.CONFIG[field]

    msg = ''

    if submit == 'reset':
        field_obj.reset()
        user.save_all()
        msg = handle.MSG['SUCCESS']

    elif submit == 'delete':
        pk = env.req.get_argument('pk')
        field_obj.remove(pk)
        user.save_all()
        msg = handle.MSG['SUCCESS']

    if msg:
        return show(env, msg=msg)

    form_data = form.formdata(env.req, field_obj)
    if form_data:
        field_obj.update(form_data)
        field_obj.changed = True
        user.save_all()
        msg = handle.MSG['SUCCESS']

    return show(env, msg=msg)

def reset(env):
    """重置用户相关的数据
    """
    uid = env.req.get_argument('uid', '')

    user = getmodel(env, uid)
    user.reset_all_data()

    return index(env, msg=handle.MSG['SUCCESS'])


def getmodel(env, uid, field=None):
    """获取并处理user，加载必要的数据
    """
    user_app = env.import_app('user')
    user = user_app.get_user(env, int(uid), read_only=True)

    if field:
        eval('user.%s.load_%s()' % tuple(field.split('.')))
    else:
        user.load_base()

    user.load_all()

    return user

