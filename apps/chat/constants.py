# coding: utf-8

import goods

TARGET_TYPE_ALL = 0
TARGET_TYPE_ONE = 1
TARGET_TYPE_GROUP = 2

TARGET_TYPE_CN = {
    TARGET_TYPE_ALL: u'系统',
    TARGET_TYPE_ONE: u'玩家昵称',
    TARGET_TYPE_GROUP: u'群组名称',
}

TARGET_COLOR_MAP = {
    'default': '#00EC00',  # 绿色
    TARGET_TYPE_ONE: '#FFFFFF',  # 白色
    TARGET_TYPE_ALL: '#EAC100',  # 金黄色
    TARGET_TYPE_GROUP: '#46A3FF',  # 淡蓝色
}

GOODS_TYPE_ITEM = 1  # 卡牌材料
GOODS_TYPE_MATERIAL = 2  # 装备材料
GOODS_TYPE_GOBLIN = 3  # 地精零件
GOODS_TYPE_EQUIP = 4  # 装备
GOODS_TYPE_STAGE = 5  # 关卡
GOODS_TYPE_HERO = 6  # 卡牌
GOODS_TYPE_PLAYER = 7  # 玩家
GOODS_TYPE_EXPRESSION = 8

GOODS_TEMPLATE = {
    GOODS_TYPE_ITEM: u'<a herf=\'%(data)s\' style="color: %(color)s; text-decoration: none">[%(name)s]</a>',
    GOODS_TYPE_MATERIAL: u'<a herf=\'%(data)s\' style="color: %(color)s; text-decoration: none">[%(name)s]</a>',
    GOODS_TYPE_GOBLIN: u'<a herf=\'%(data)s\' style="color: %(color)s; text-decoration: none">[%(name)s]</a>',
    GOODS_TYPE_EQUIP: u'<a herf=\'%(data)s\' style="color: %(color)s; text-decoration: none">[%(name)s]</a>',
    GOODS_TYPE_STAGE: u'<a herf=\'%(data)s\' style="color: %(color)s; text-decoration: none">[%(name)s]</a>',
    GOODS_TYPE_HERO: u'<a herf=\'%(data)s\' style="color: %(color)s; text-decoration: underline">[%(name)s(%(level)s)]</a>',
    GOODS_TYPE_PLAYER: u'<a herf=\'%(data)s\' style="color: %(color)s">@%(username)s</a>',
    GOODS_TYPE_EXPRESSION: '%(expression)s',
}

GOODS_INFO_MAPPING = {
    GOODS_TYPE_ITEM: goods.item_info,
    GOODS_TYPE_MATERIAL: goods.material_info,
    GOODS_TYPE_GOBLIN: goods.goblin_info,
    GOODS_TYPE_EQUIP: goods.equip_info,
    GOODS_TYPE_STAGE: goods.stage_info,
    GOODS_TYPE_HERO: goods.hero_info,
    GOODS_TYPE_PLAYER: goods.player_info,
}

GOODS_STAR_COLOR_MAP = {
    0: '#FFFFFF',
    1: '#00EC00',
    2: '#00EC00',
    3: '#00EC00',
    4: '#00EC00',
    5: '#00EC00',
    6: '#00EC00',
    7: '#00EC00',
}


MESSAGE_FORMET = u'<p style="color: %s">%s: %s</p>'


