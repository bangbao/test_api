# coding: utf-8

import itertools
import constants
import ujson


def format_message(user, message):
    """格式化用户发的消息

    Args:
        user: 用户对象
        message: 前端发送的消息文本（约定的格式）

    Returns:
        格式化后的html文本
    """
    target_type, target_id, text, goods = eval(message)

    color = constants.TARGET_COLOR_MAP[target_type]
    target_ids, target = get_target(user, target_type, target_id)
    goods_text = format_goods_text(user, goods)
    text = format_text(text, goods_text)

    message = constants.MESSAGE_FORMET % (color, target, text)

    return u'%s|%s' % (target_ids, message)


def get_target(user, target_type, target_id):
    """获取目标对象

    Args:
        user: 用户对象
        target_type: 发送目标类型
        target_id: 目标ID, 若为私聊

    Returns:
        目标id们，目标名字

    TODO:
        需要填充点击效果
    """
    user.game.load_info()
    user.game.load(user.env)
    target = user.game.info['username']

    target_ids = get_target_ids(user, target_type, target_id)

    if not isinstance(target, unicode):
        target = target.decode('utf-8')

    return target_ids, target


def get_target_ids(user, target_type, target_id):
    """获取目标用户ID

    TODO:
        完善每个类型
    """

    ids = [user.pk, target_id]

    return '|'.join(itertools.imap(str, ids))


def format_text(text, goods_data):
    """填充消息文本内容

    Args:
        text: 消息文本
        goods_data: 插入的物品消息文本

    TODO:
        text中屏蔽字替换为*
    """
    return text % tuple(goods_data)


def format_goods_text(user, goods):
    """格式化插入物品文本信息

    Args:
        user: 用户对象
        goods: 前端传入的物品标识信息(类型，ID)

    Returns:
        text_data: 物品HTML连接集合
        info_data: 物品信息集合
    """
    text_data = []

    for goods_type, goods_id in goods:
        goods_text = format_goods(user, goods_type, goods_id)
        text_data.append(goods_text)

    return text_data


def format_goods(user, goods_type, goods_id):
    """物品信息

    Args:
        user: 用户对象
        goods_type: 物品类型
        goods_id: 物品标识ID

    Returns:
        goods_text: 物品HTML连接
        goods_info: 物品信息
    """
    func_info = constants.GOODS_INFO_MAPPING[goods_type]
    goods_info = func_info(user, goods_id)
    goods_data = ujson.dumps(goods_info)

    star = goods_info.get('star', 0)
    star_color = constants.GOODS_STAR_COLOR_MAP[star]
    goods_info['color'] = star_color
    goods_info['data'] = goods_data

    goods_tempate = constants.GOODS_TEMPLATE[goods_type]
    goods_text = goods_tempate % goods_info

    return goods_text

