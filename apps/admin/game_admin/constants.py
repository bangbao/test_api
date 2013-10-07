# coding: utf-8

from apps.admin import handle

FIELD_LINKS = [
    ('user', u'经常变动数据'),
    ('info', u'不常变动数据'),
]

CONFIG = {
    'info': {
        'desc': handle.field_to_form(u'不常修改', 'game'),
        'type': 'dict',
        'values': {
            'username': (handle.value_to_form(u'用户名'), handle.tostr),
            'role': (handle.value_to_form(u'角色'), handle.toint),
            'vip': (handle.value_to_form(u'VIP经验'), handle.toint),
            'equip': (handle.value_to_form(u'装备积分'), handle.toint),
            'hero': (handle.value_to_form(u'卡牌积分'), handle.toint),
            'exp': (handle.value_to_form(u'当前经验上限'), handle.toint),
            'energy': (handle.value_to_form(u'当前体力上限'), handle.toint),
            'enter': (handle.value_to_form(u'标识用户是否注册过'), handle.toint),
            'cost': (handle.value_to_form(u'能力值上限'), handle.toint),
            'friend': (handle.value_to_form(u'好友上限'), handle.toint),
            'energy_fill_at': (handle.value_to_form_time(u'行动力最后补充时间'), handle.totime),
        },
    },
    'user':{
        'desc': handle.field_to_form(u'经常修改', 'game'),
        'type': 'dict',
        'values': {
            'level': (handle.value_to_form(u'用户级别'), handle.toint),
            'exp': (handle.value_to_form(u'当前经验'), handle.toint),
            'light': (handle.value_to_form(u'光明点数'), handle.toint),
            'dark': (handle.value_to_form(u'黑暗点数'), handle.toint),
            'battle': (handle.value_to_form(u'征战点数'), handle.toint),
            'energy': (handle.value_to_form(u'当前行动力'), handle.toint),
            'kcoin': (handle.value_to_form(u'酷币数量'), handle.toint),
            'gold': (handle.value_to_form(u'金钱数量'), handle.toint),
            'team': (handle.value_to_form_team(u'战斗阵容'), handle.toteam),
        },
    },
}
