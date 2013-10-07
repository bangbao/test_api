# coding:utf-8

import time
import string
import itertools

HERO_ANNOUNCEME = 1
ADVEN_ANNOUNCEME = 2

ANNOUNCEMENTS = "%d,%d" % (HERO_ANNOUNCEME, 
                           ADVEN_ANNOUNCEME)

def format_hero(env, formats):
    """ 针对英雄类的公告进行格式化

    Args:
        env: 运行环境
        formats: 格式化参数字符串

    Returns:
        被格式化后的公告内容
    """
    uid, hero_id = formats.split(',')

    return TEMPLATES[HERO_ANNOUNCEME] % (uid, hero_id)

def format_adven(env, formats):
    """ 针对关卡类的公告进行格式化

    Args:
        env: 运行环境
        formats: 格式化参数字符串

    Returns:
        被格式化后的公告内容
    """
    uid, adven_id = formats.split(',')

    return TEMPLATES[ADVEN_ANNOUNCEME] % (uid, adven_id)


FORMATS = {
    str(HERO_ANNOUNCEME): format_hero,
    str(ADVEN_ANNOUNCEME): format_adven,
}

TEMPLATES = {
    HERO_ANNOUNCEME: "%s鸿运当头，获取传奇武将%s",
    ADVEN_ANNOUNCEME: "%s势不可挡，通过关卡%s",
}

BASE_WEIGHTS = {
    HERO_ANNOUNCEME: HERO_ANNOUNCEME * (10 ** 11),
    ADVEN_ANNOUNCEME: ADVEN_ANNOUNCEME * (10 ** 11),
}

item_split = lambda s: string.split(s, ':')

def post_announcement(env, tp, formats, receivers=None):
    """ 产生一条公告

    根据类型和内容生成一个公告数据,放入redis SortedSet里
    key   为内容简介可以在发给前端时可以反向解释出来的标识数据
    score 基础权重 * 10000000000 + 时间戳
    
    Args:
       env: 运行环境
       tp: 公告类型，决定权重和格式化模板
       formats: 格式化所需参数
       receivers: 接收者id列表 默认为广播
    """
    if not receivers:
        pop_user = '0'
        receivers = ()
    else:
        pop_user = receivers.pop()

    formats[0] = "%s:%s" % (pop_user, formats[0])

    key = ','.join(itertools.imap(str, itertools.chain((tp,),
                                  receivers, formats)))
    game = env.user.game
    score = BASE_WEIGHTS[tp] + int(time.time())

    if not game.announce.key:
        game.load_announce()
        game.load(env)

    game.announce.zadd(key, score)


def recv_announcement(env):
    """ 接受指定数量的公告

    根据用户最后一次获取公告的时间，向后取出指定数据
    公告给前端显示

    Args:
        env: 运行环境

    Returns:
        针对当前用户过滤好的公告列表
    """
    public_app = env.import_app('public')

    game = env.user.game
    data = game.announce.evalsha(public_app.LUA_SHAS['announcement'], 3,
                                 game.announce.key, ANNOUNCEMENTS, game.pk)
    announcements = []

    for tp, formats in itertools.imap(item_split, data):
        announcements.append(FORMATS[tp](env, formats))

    return announcements

