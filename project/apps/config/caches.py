# coding: utf-8

import sys
import logging


class AppCacheConfig(object):
    """ app应用配置缓存

    当应用调用env.game_config时会自动检查
    当次请求已存在指定的配置时，不加载直接使用，当没有时
    会重新加载一次配置，并在当次使用该配置，直到请求结束

    Attributes:
       env: 运行环境
       caches: 全局配置缓存
       loader: 配置加载函数
    """
    loader = None
    _cache = {}
    caches = {}

    def __new__(cls, env):
        """
        """
        super_new = super(AppCacheConfig, cls).__new__
        env_id = env.env.identity

        obj = cls._cache.get(env_id)
        if not obj:
            obj = cls._cache[env_id] = super_new(cls, env)
            #logging.info('new config %r' % cls._cache)

        #logging.info('new config %r' % repr(obj.caches.keys()))
        return obj

    def __init__(self, env):
        self.env = env
        #self.caches = {}
        #logging.info('config size: %s' % (sys.getsizeof(self)))

    def __getitem__(self, name):
        if not name in self.caches:
            #logging.info('get config %s' % name)
            self.caches[name] = self.loader(self.env, name)

        return self.caches[name]

    def __setitem__(self, name, value):
        self.caches[name] = value
