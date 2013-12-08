# coding: utf-8

import time

from lib.core.environ import Environ
from lib.db.fields import ModelConfig
from . import logics
from . import transfer
from .models import Config
from .caches import AppCacheConfig


game_configs = {}


def loadall(env):
    """加载指定环境的所有配置

    根据指定环境，加载当前环境的所有配置到game_configs中
    key为当前环境的标识
    global: 存放当前环境公用配置
    local: 若此环境存在内分服，刚存放各个内分服版本的配置

    Args:
        env: 指定的环境
    """
    global game_configs
    data = {}
    vers = {}
    connection = env.storage.connects.get(ModelConfig, Config)
    cursor = connection.cursor()
    query = "SELECT ver,name,value FROM %s WHERE env='%s'" % (Config.NAME,
                                                              env.env.identity)
    cursor.execute(query)

    for row in cursor:
        if row['ver']:
            if row['ver'] in vers:
                vers[row['ver']][row['name']] = eval(row['value'])
            else:
                vers[row['ver']] = {row['name']: eval(row['value'])}
        else:
            data[row['name']] = eval(row['value'])

    game_configs[env.env.identity] = {'global': data,
                                      'local': vers
                                    }


def set_config(env, name, value):
    """设置指定环境的配置

    配置存放在mysql中，每次更新直接写入数据库
    表字段含义：
        id: 标识当前配置，为环境标识，内分服标识， 配置名字组合而成
        env: 当前环境标识，字符串
        ver: 内分服标识，现默认为空字符串
        name: 配置名字， 字符串
        value: 配置值， 字符串
        updated_at: 配置更新时间，整型
        created_at: 配置添加时间，整型

    Args:
        env: 指定的环境
        name: 配置名字
        value: 配置内容, 必须可转为字符串
    """
    connection = env.storage.connects.get(ModelConfig, Config)
    cursor = connection.cursor()
    env_id = env.env.identity
    ver = ''
    config_id = ':'.join((env_id, ver, name))
    data = repr(value)
    timestamp = int(time.time())

    query = "UPDATE %s SET value=%s, updated_at=%s WHERE id='%s'" % (
                    Config.NAME, '%s', '%s', config_id)

    if not cursor.execute(query, [data, timestamp]):
        query = "INSERT INTO %s (id,env,ver,name,value,created_at) \
                    VALUES('%s','%s','%s','%s',%s,%s)" % (Config.NAME,
                           config_id, env_id, ver, name, '%s', '%s')
        cursor.execute(query, [data, timestamp])

    connection.commit()


def get_config(env, name):
    """获取配置内容

    Args:
        env: 指定环境
        name: 配置名字

    Returns:
        配置内容
    """
    #loadall(env)
    ver = None
    obj = game_configs[env.env.identity]

    if env.env.multi():
        ver = env.user.multi_token

    if ver in obj['local']:
        return obj['local'][name]
    elif name in obj['global']:
        return obj['global'][name]
    else:
        return game_configs[Environ.GLOBAL_ENVIRON][name]


def get_configs(env, names):
    """获取配置内容

    Args:
        env: 指定环境
        names: 动态配置名字们

    Returns:
        配置内容
    """
    game_config = {}

    for name in names:
        game_config[name] = get_config(env, name)

    return game_config


AppCacheConfig.loader = staticmethod(get_config)

