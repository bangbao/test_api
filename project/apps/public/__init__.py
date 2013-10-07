# coding: utf-8
import os
import logics
import constants
import generator

LUA_SHAS = {}


def register_lua_sha(env):
    """ 当进程启动时注册lua脚本到redis服务器
    """
    lua_path = os.path.join(env.env.document_root, 'lua')
    rclient = env.storage.connects.rawget(env.settings.REDIS_PRELOAD_HOSTS)

    for filename in os.listdir(lua_path):
        filepath = os.path.join(lua_path, filename)
        key, ext = os.path.splitext(filename)

        with open(filepath, 'rb') as fp:
            content = fp.read()
            LUA_SHAS[key] = rclient.script_load(content)
