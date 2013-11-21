# coding: utf-8
""" 聊天细节处理
"""
from lib.db.fields import ModelChat
import itertools

CHAT_CONNECTIONS = {}
CHAT_CHANNEL = 'chat_channel'
ALL_USER = 0


def get_connect(handler):
    """ 获取相对应的redis链接

    Args:
       handler: 请求handler

    Returns:
       根据环境创建的链接对象
    """
    env = handler.env

    client = env.storage.connects.get(ModelChat, long_connect=True)
    client.connect()

    return client


def get_channel(handler):
    """ 获取相对应的聊天频道

    Args:
       handler: 请求handler

    Returns:
       聊天频道名称
    """
    return CHAT_CHANNEL


def open_connect(handler):
    """ 处理打开链接
    
    将handler放入全局变量，方便广播

    Args:
       handler: 请求handler
    """
    env = handler.env
    CHAT_CONNECTIONS[env.user.pk] = handler


def send_message(handler, message):
    """ 处理客户端发送消息

    Args:
       handler: 请求handler
       message: 发送的消息
    """
    client = get_connect(handler)
    channel = get_channel(handler)
    client.publish(channel, message)
    client.disconnect()


def message(body):
    """ 广播消息

    根据从聊天频道里得到的数据，来发送到指定socket

    Args:
       body: 消息内容
    """
    object_list = body.split(',')
    message = object_list.pop()
    object_list = map(int, object_list)
    keys = []

    if object_list[0] == ALL_USER:
        keys = CHAT_CONNECTIONS.iterkeys()
    else:
        keys = itertools.ifilter(CHAT_CONNECTIONS.has_key, object_list)

    broadcast(message, keys)


def close_connect(handler):
    """ 处理链接关闭
    
    当链接关闭后做相对应的整理

    Args:
       handler: 请求handler
    """
    channel = get_channel(handler)
    handler.SUBSCRIBE_CHANNELS[channel] -= 1

    if handler.SUBSCRIBE_CHANNELS[channel] < 1 and handler.client.subscribed:
        handler.client.unsubscribe(channel)
        handler.client.disconnect()
        handler.SUBSCRIBE_CHANNELS[channel] = 0
        handler.SUBSCRIBE_PROCESS[channel] = False

    user = handler.env.user

    if user and user.pk in CHAT_CONNECTIONS:
        del CHAT_CONNECTIONS[user.pk]


def broadcast(message, keys):
    """ 对指定用户进行广播数据

    Args:
       message: 要广播的消息
       keys: 指定的广播人选
    """
    for key in keys:
        CHAT_CONNECTIONS[key].write_message(message)

