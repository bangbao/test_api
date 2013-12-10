# coding: utf-8

from apps.admin import handle
from apps.admin.form import Form
from . import constants


TEMPLATE = 'admin/hero/heromain.html'

def index(env):
    """hero模块后台首页，提供UID输入
    """
    data = {'op': 'input', 'field': 'heros'}
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
    field_obj = getattr(u.hero, field)

    hero_app = env.import_app('hero')
    equip_app = env.import_app('equip')
    goblin_app = env.import_app('goblin')
    pet_app = env.import_app('pet')
    
    used_set = None
    if field == 'heros':
        used_set = hero_app.team_get(u)
    elif field == 'equips':
        used_set = equip_app.get_used_equip(u)
    elif field == 'goblins':
        used_set = goblin_app.get_used_goblin(u)
    elif field == 'pets':
        used_set = pet_app.get_played_pet(u)

    if used_set:
        field_obj['used_set'] = used_set

    formtable = Form(env, field, field_obj, constants.CONFIG).show()

    if '<other_params_panel>' in formtable:
        formtable = formtable.replace(
            '<other_params_panel>', 
            (u'<input type="hidden" name="uid" value="%s"/>'
            u'<input type="hidden" name="field" value="%s" />'
            u'<input type="hidden" name="next_op" value="save"/>') 
            % (uid, field))

    if '<add_panel>' in formtable:
        add_params = constants.CONFIG[field]['add']
        add_html = handle.add_panel(uid, 'hero', field, len(field_obj), add_params)
        formtable = formtable.replace('<add_panel>', add_html)

    info_str = ''
    static_info = constants.CONFIG[field].get('info', {})
    if static_info:
        fd_info_list = []
        for gp in static_info:
            curr_info = static_info[gp]
            gp_list = [u'%s' % curr_info['title']]
            if 'detail' in curr_info:
                for alt, desc in curr_info['detail'].iteritems():
                    gp_list.append(u'%s.%s' % (alt, desc))
            fd_info_list.append(u'&nbsp;'.join(gp_list))

        info_str = u'<br/>'.join(fd_info_list)    

    formtable = formtable.replace('<static_panel>', info_str)
        
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
    """保存hero模块data属性的修改
    """
    uid = env.req.get_argument('uid', '')
    field = env.req.get_argument('field', 'data')

    u = getmodel(uid, env)
    field_obj = getattr(u.hero, field)
    form_data = Form(env, field, field_obj, constants.CONFIG, env.req).mdictdata()

    changed = form_data.pop('form_changed')

    msg = ''
    if changed:
        field_obj.update(form_data)
        field_obj.changed = changed
        setattr(u.hero, field, field_obj)
        env.storage.save(u.hero)

        msg = handle.MSG['SUCCESS']

    return show(env, uid=uid, field=field, msg=msg)


def modify(env):
    """修改用户道具
    
    卡牌， 装备， 卡牌材料， 装备材料， 零件
    """
    uid = env.req.get_argument('uid', '')
    field = env.req.get_argument('field', '')

    u = getmodel(uid, env)

    field_obj = getattr(u.hero, field)
    pk, mdata, changed = Form(env, field, field_obj, constants.CONFIG, env.req).mlistdata()

    msg = ''
    if changed:
        game_config = env.game_config
        hero_app = env.import_app('hero')
        equip_app = env.import_app('equip')
        goblin_app = env.import_app('goblin')
        pet_app = env.import_app('pet')

        new_obj = None
        if field == 'heros':
            new_obj = hero_app.logics.hero_birth(mdata.pop('cfg_id'), game_config, **mdata)

        elif field == 'equips':
            new_obj = hero_app.logics.equip_birth(mdata.pop('cfg_id'), game_config, **mdata)

        elif field == 'materials':
            equip_app.incr_material(u, pk, mdata['num'], modify=True)

        elif field == 'items':
            hero_app.incr_item(u, pk, mdata['num'], modify=True)

        elif field == 'goblin':
            new_obj = goblin_app.logics.goblin_birth(mdata.pop('cfg_id'), game_config, **mdata)

        elif field == 'pets':
            new_obj = pet_app.logics.pet_birth(mdata.pop('cfg_id'), game_config, **mdata)

        if new_obj:
            field_obj.modify(pk, **new_obj)

        env.storage.save(u.hero)

        msg = handle.MSG['SUCCESS']

    return show(env, uid=uid, field=field, msg=msg)


def delete(env):
    """删除用户道具
    
    卡牌， 装备， 卡牌材料， 装备材料， 零件
    """
    uid = env.req.get_argument('uid', '')
    field = env.req.get_argument('field', '')

    u = getmodel(uid, env)

    pk = env.req.get_argument('pk', '')

    if pk.isdigit():
        pk = int(pk)

    field_obj = getattr(u.hero, field)
    field_obj.remove(pk)
    env.storage.save(u.hero)

    return show(env, uid=uid, field=field, msg=handle.MSG['SUCCESS'])


def add(env):
    """为用户添加道具
    
    卡牌， 装备， 卡牌材料， 装备材料， 零件
    """
    uid = env.req.get_argument('uid', '')
    field = env.req.get_argument('field', '')

    add_params = constants.CONFIG[field]['add']

    params = {}
    valid = True
    for param_info in add_params:
        name = 'add_%s' % param_info[0]
        par = env.req.get_argument(name)
        if not par.isdigit():
            valid = False
            break
        params[param_info[0]] = int(par)

    if not valid:
        return show(env, uid=uid, field=field, msg=handle.MSG['ID_ERROR'])

    u = getmodel(uid, env)
    hero_app = env.import_app('hero')
    equip_app = env.import_app('equip')
    goblin_app = env.import_app('goblin')
    pet_app = env.import_app('pet')

    cfg_id = params.pop('cfg_id')
    num = params.pop('num')
    if field == 'materials':
        equip_app.incr_material(u, cfg_id, num)

    elif field == 'items':
        hero_app.incr_item(u, cfg_id, num)

    else:
        while num > 0:

            if field == 'heros':
                obj_from = hero_app.constants.HERO_FROM_ADMIN
                hero_app.birth_hero(u, cfg_id, where=obj_from, **params)

            elif field == 'equips':
                obj_from = equip_app.constants.EQUIP_FROM_ADMIN
                equip_app.birth_equip(u, cfg_id, where=obj_from, **params)
                
            elif field == 'goblins':
                obj_from = goblin_app.constants.GOBLIN_FROM_ADMIN
                goblin_app.birth_goblin(u, cfg_id, where=obj_from, **params)

            elif field == 'pets':
                pet_app.birth_pet(u, cfg_id, **params)

            num -= 1

    u.save_all()

    return show(env, uid=uid, field=field, msg=handle.MSG['SUCCESS'])


def reset(env):
    """重置或清空数据
    """
    uid = env.req.get_argument('uid', '')
    field = env.req.get_argument('field', '')

    u = getmodel(uid, env)

    field_obj = getattr(u.hero, field)
    field_obj.reset()
    setattr(u.hero, field, field_obj)

    env.storage.save(u.hero)

    return show(env, uid=uid, field=field, msg=handle.MSG['SUCCESS'])


def getmodel(uid, env):
    """获取并处理user，加载必要的数据
    """
    user_app = env.import_app('user')
    u = user_app.get_user(env, int(uid))

    env.user = u
    u.hero.load_all(env)
    u.game.load_all(env)

    return u


