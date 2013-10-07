# coding: utf-8

import sys
import redis
import logging


class ConnectPool(dict):
    _cache = {}

    def __new__(cls, env):
        """
        """
        super_new = super(ConnectPool, cls).__new__
        env_id = env.env.identity
 
        obj = cls._cache.get(env_id)
        if not obj:
            obj = cls._cache[env_id] = super_new(cls, env)

        return obj

    def __init__(self, env):
        self.env = env
        #logging.info('cache size: %s' % sys.getsizeof(self))

    def __getitem__(self, name):
        sid, cache_config = self.env.hash_caches(name)
        obj = super(ConnectPool, self).get(sid)

        if not obj:
            obj = redis.Redis(**cache_config)
            super(ConnectPool, self).__setitem__(sid, obj)

        return obj


class Cache(object):
    """
    """
    def __init__(self, env):
        """
        """
        #logging.info('cache init: %r %r' % (env, env.env))
        self.env = env
        self.connects = ConnectPool(env)

    def get(self, carrier, attr_name, kwargs):
        """
        """
        key = self.env.generate_cache_key(carrier, attr_name)
        rclient = self.connects[key]
        attr = getattr(carrier, attr_name)
        obj = None

        if attr.CACHE_TYPE == 'string':
            obj = rclient.get(key)
        elif attr.CACHE_TYPE == 'hash':
            keys = set(kwargs.get('keys', []))
            keys.discard(None)

            if keys:
                obj = rclient.hmget(key, keys)

                if not all(obj):
                    obj = None
            else:
                obj = rclient.hgetall(key)

        if obj:
            attr.cache_loader(obj, **kwargs)
            rclient.expire(key, self.env.settings.CACHE_KEY_DELAY_SECONDS)
        else:
            stmt = self.env.storage.select(attr_name, carrier)
            attr.loader(stmt)
            stmt.close()

            self.set(carrier, attr_name)

    def set(self, carrier, attr_name):
        """
        """
        key = self.env.generate_cache_key(carrier, attr_name)
        rclient = self.connects[key]
        pipe = rclient.pipeline()
        value = getattr(carrier, attr_name)
        data = value.tocache()

        if value.CACHE_TYPE == 'string':
            pipe.set(key, data)
        elif value.CACHE_TYPE == 'hash':
            pipe = rclient.pipeline()
            pipe.hmset(key, data)

            if value.removes:
                pipe.hdel(key, *value.removes)
            #for hkey, hvalue in data:
            #    pipe.hset(key, hkey, hvalue)

            #for hkey in value.removes:
            #    pipe.hdel(key, hkey)

        pipe.expire(key, self.env.settings.CACHE_KEY_DELAY_SECONDS)
        pipe.execute()

        return data

    def remove(self, key):
        """
        """
        rclient = self.connects[key]
        rclient.remove(key)

