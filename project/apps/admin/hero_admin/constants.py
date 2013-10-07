# coding: utf-8

from apps.admin import handle

FIELD_LINKS = [
    ('heros', u'卡牌包'),
    ('equips', u'装备包'),
    ('goblins', u'零件包'),
    ('pets', u'宠物包'),
    ('items', u'卡牌转职材料包'),
    ('materials', u'装备分解材料包'),
    ('data', u'其他属性'),
]

GROUP_LABELS = {
    'heros': {
        'cfg_id': u'卡牌配置ID',
        'level': u'卡牌等级',
        'exp': u'卡牌当前经验',
        'hp': u'卡牌血量',
        'natk': u'物理攻击',
        'ndef': u'物理防御',
        'matk': u'魔法攻击',
        'mdef': u'魔法防御',
        'sign': u'卡牌签名',
        'cost': u'卡牌cost值',
        'lock': u'卡牌是否被锁定',
        'askill': u'卡牌怒气技能等级',
        'nskill': u'卡牌普通技能等级',
    },
    'equips': {
        'cfg_id': u'装备配置ID',
        'level': u'等级',
        'st_cd': u'冷却时间',
        'st_at': u'最后一次强化时间',
        'matk': u'魔法攻击',
        'mdef': u'魔法防御',
        'natk': u'物理攻击',
        'ndef': u'物理防御',
        'hp': u'血量',
    },
    'pets': {
        'cfg_id': u'配置ID',
        'level': u'等级',
        'exp': u'经验',
        'full': u'饱食度',
        'clone': u'繁衍代数',
        'skill': u'技能们',
    },
    'materials':{
        'num': u'数量',
    },
    'items': {
        'num': u'数量',
    },
    'goblin': {
        'cfg_id': u'零件配置ID',
        'level': u'当前等级',
        'exp': u'当前经验',
        'level_up': u'当前剩余经验',
        'goblin_id': u'零件标识id',
    },
}

GROUP_FUNC = {
    'heros': {
        'cfg_id': (handle.one_to_group_no, handle.toint),
        'level': (handle.one_to_group, handle.toint),
        'exp': (handle.one_to_group_no, None),
        'hp': (handle.one_to_group_no, None),
        'natk': (handle.one_to_group_no, None),
        'ndef': (handle.one_to_group_no, None),
        'matk': (handle.one_to_group_no, None),
        'mdef': (handle.one_to_group_no, None),
        'sign': (handle.one_to_group, handle.tostr),
        'cost': (handle.one_to_group_no, None),
        'lock': (handle.one_to_group, handle.toint),
        'askill': (handle.one_to_group_no, None),
        'nskill': (handle.one_to_group_no, None),
    },
    'equips': {
        'cfg_id': (handle.one_to_group_no, handle.toint),
        'level': (handle.one_to_group, handle.toint),
        'matk': (handle.one_to_group_no, None),
        'mdef': (handle.one_to_group_no, None),
        'natk': (handle.one_to_group_no, None),
        'ndef': (handle.one_to_group_no, None),
        'hp': (handle.one_to_group_no, None),
    },
    'pets': {
        'cfg_id': (handle.one_to_group_no, handle.toint),
        'level': (handle.one_to_group, handle.toint),
        'exp': (handle.one_to_group_no, None),
        'full': (handle.one_to_group, None),
        'clone': (handle.one_to_group, None),
        'skill': (handle.one_to_group, None),
    },
    'materials':{
        'cfg_id': (handle.one_to_group_no, handle.toint),
        'num': (handle.one_to_group, handle.toint),
    },
    'items': {
        'cfg_id': (handle.one_to_group_no, handle.toint),
        'num': (handle.one_to_group, handle.toint),
    },
    'goblin': {
        'cfg_id': (handle.one_to_group_no, handle.toint),
        'level': (handle.one_to_group, handle.toint),
        'exp': (handle.one_to_group_no, None),
        'level_up': (handle.one_to_group_no, None),
    },
}

GROUP_SORT = {
    'heros': [
        'cfg_id', 'level', 'exp', 'hp', 'natk', 'ndef', 'matk', 
        'mdef', 'sign', 'cost', 'lock', 'askill', 'nskill'
    ],
    'equips': [
        'cfg_id', 'level',
        'matk', 'mdef', 'natk', 'ndef', 'hp'
    ],
    'materials': ['num'],
    'items': ['num'],
    'goblin': ['cfg_id', 'level', 'exp', 'level_up'],
    'pets': ['cfg_id', 'level', 'exp', 'full', 'clone', 'skill'],
}

CONFIG = {
    'data': {
        'desc': handle.field_to_form(u'其他属性', 'hero'),
        'type': 'dict',
        'cname': 'data',  #对应配置名称
        'values': {
            'resolve': (handle.value_to_form(u'当前剩余免费分解次数'), handle.toint),
            'resolve_top': (handle.value_to_form(u'每天免费分解次数上限'), handle.toint),
        },
    },
    'heros': {
        'desc': handle.group_field_to_form(u'卡属性', 
                                           GROUP_LABELS['heros'], 
                                           GROUP_SORT['heros']),
        'cname': 'heros',
        'type': 'list',
        'add': [  #添加参数(参数名，中文说明，默认值)
            ('cfg_id', u'卡牌配置ID', ''), 
            ('level', u'卡牌等级', 1),
            ('num', u'添加数量', 1),
        ],
        'group': (handle.group_to_form(GROUP_LABELS['heros'], 
                                       GROUP_FUNC['heros'], 
                                       GROUP_SORT['heros']), 
                  handle.togroup(GROUP_FUNC['heros'], GROUP_SORT['heros'])),
        'info': {
            'from': {
                'title': u'PK字段最后两位数字表示卡牌来源：',
                'detail': {
                    0: u'默认来源',
                    1: u'关卡-关卡ID',
                    2: u'卡牌进阶',
                    3: u'后台添加',
                    4: u'竞技场',
                },
            },
            'alert': {
                'title': u'红色名称的卡牌属于当前战斗整容！',
            },
        },
    },
    'equips': {
        'desc': handle.group_field_to_form(u'装备', 
                                           GROUP_LABELS['equips'], 
                                           GROUP_SORT['equips']),
        'cname': 'equips',
        'type': 'list',
        'add': [
            ('cfg_id', u'装备配置ID', ''), 
            ('level', u'装备等级', 1),
            ('num', u'添加数量', 1),
        ],
        'group': (handle.group_to_form(GROUP_LABELS['equips'], 
                                       GROUP_FUNC['equips'], 
                                       GROUP_SORT['equips']), 
                  handle.togroup(GROUP_FUNC['equips'], GROUP_SORT['equips'])),
        'info': {
            'from': {
                'title': u'PK字段最后两位数字表示装备来源：',
                'detail': {
                    0: u'默认来源',
                    1: u'关卡-关卡ID',
                    2: u'装备合成',
                    3: u'后台添加',
                    4: u'竞技场',
                },
            },
            'alert': {
                'title': u'红色名称表示该装备使用中！',
            },
        },
    },
    'materials': {
        'desc': handle.group_field_to_form(u'装备材料', 
                                           GROUP_LABELS['materials'], 
                                           GROUP_SORT['materials']),
        'cname': 'equip_material',
        'type': 'list',
        'add': [
            ('cfg_id', u'材料配置ID', ''),
            ('num', u'添加数量', 1),
        ],
        'group': (handle.group_to_form(GROUP_LABELS['materials'], 
                                       GROUP_FUNC['materials'], 
                                       GROUP_SORT['materials']), 
                  handle.togroup(GROUP_FUNC['materials'], GROUP_SORT['materials'])),
    },
    'items': {
        'desc': handle.group_field_to_form(u'卡牌转职材料', 
                                           GROUP_LABELS['items'], 
                                           GROUP_SORT['items']),
        'cname': 'item', 
        'type': 'list',
        'add': [
            ('cfg_id', u'材料配置ID', ''),
            ('num', u'添加数量', 1),
        ],
        'group': (handle.group_to_form(GROUP_LABELS['items'], 
                                       GROUP_FUNC['items'], 
                                       GROUP_SORT['items']), 
                  handle.togroup(GROUP_FUNC['items'], GROUP_SORT['items'])),
    },
    'goblins': {
        'desc': handle.group_field_to_form(u'地精科技零件', 
                                           GROUP_LABELS['goblin'], 
                                           GROUP_SORT['goblin']),
        'cname': 'goblins',
        'type': 'list',
        'add': [
            ('cfg_id', u'零件配置ID', ''), 
            ('level', u'零件等级', 1),
            ('num', u'添加数量', 1),
        ],
        'group': (handle.group_to_form(GROUP_LABELS['goblin'], 
                                       GROUP_FUNC['goblin'], 
                                       GROUP_SORT['goblin']), 
                  handle.togroup(GROUP_FUNC['goblin'], GROUP_SORT['goblin'])),
        'info': {
            'from': {
                'title': u'PK字段最后两位数字表示零件来源：',
                'detail': {
                    0: u'默认来源',
                    2: u'打造',
                    3: u'后台添加',
                    4: u'竞技场',
                },
            },
            'alert': {
                'title': u'红色名称表示该零件使用中！',
            },
        },
    },
    'pets': {
        'desc': handle.group_field_to_form(u'宠物背包',
                                           GROUP_LABELS['pets'],
                                           GROUP_SORT['pets']),
        'cname': 'pets',
        'type': 'list',
        'add': [
            ('cfg_id', u'配置ID', ''),
            ('level', u'等级', 1),
            ('num', u'添加数量', 1),
        ],
        'group': (handle.group_to_form(GROUP_LABELS['pets'],
                                       GROUP_FUNC['pets'],
                                       GROUP_SORT['pets']),
                  handle.togroup(GROUP_FUNC['pets'], GROUP_SORT['pets'])),
        'info': {
            'from': {
                'title': u'PK字段最后两位数字表示来源：',
                'detail': {
                    0: u'默认来源',
                },
            },
            'alert': {
                'title': u'红色名称表示该零件使用中！',
            },
        },
    },
}


