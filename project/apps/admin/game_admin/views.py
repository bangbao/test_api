# coding: utf-8

import constants
from apps.admin import handle
from apps.admin.form import Form

TEMPLATE = 'admin/game/gamemain.html'

def index(env):
    """game模块后台首页，提供UID输入
    """
    data = {'op': 'input', 'field': 'user'}
    return env.render(TEMPLATE, {'data': data})

def show(env, uid=None, field=None, msg=None):
    """显示HTML表单
    
    Args:
        env: 环境
        uid: 用户ID
        field: game模块的属性名称
    """
    uid = env.req.get_argument('uid', uid)
    field = env.req.get_argument('field', field)

    u = getmodel(uid, env)

    field_obj = getattr(u.game, field)
    formtable = Form(env, field, field_obj, constants.CONFIG).show()
    formtable = formtable.replace(
        '<other_params_panel>', 
        (u'<input type="hidden" name="uid" value="%s"/>'
        u'<input type="hidden" name="next_op" value="save"/>') % uid)

    data = {
        'uid': uid, 
        'fields': constants.FIELD_LINKS, 
        'field': field,
        'op': 'show',
        'form': formtable,
        'msg': msg,
    }

    return env.render(TEMPLATE, {'data': data})

def save(env):
    """保存game模块user或者info属性的修改
    """
    uid = env.req.get_argument('uid', '')
    field = env.req.get_argument('field', 'user')

    u = getmodel(uid, env)

    field_obj = getattr(u.game, field)
    form_data = Form(env, field, field_obj, constants.CONFIG, env.req).mdictdata()

    changed = form_data.pop('form_changed')

    msg = ''
    if changed:
        field_obj.update(form_data)
        field_obj.changed = changed
        setattr(u.game, field, field_obj)
        env.storage.save(u.game)

        msg=handle.MSG['SUCCESS']

    return show(env, uid=uid, field=field, msg=msg)

def reset(env):
    """重置数据
    """
    uid = env.req.get_argument('uid', '')
    field = env.req.get_argument('field', 'user')

    u = getmodel(uid, env)

    field_obj = getattr(u.game, field)
    field_obj.reset()
    setattr(u.game, field, field_obj)

    env.storage.save(u.game)

    return show(env, uid=uid, field=field, msg=handle.MSG['SUCCESS'])

def getmodel(uid, env):
    """获取并处理user，加载必要的数据
    """
    user_app = env.import_app('user')
    u = user_app.get_user(env, int(uid))

    env.user = u
    u.game.load_info()
    u.game.load_user()
    u.game.load(env)

    return u
    
