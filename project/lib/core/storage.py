# coding: utf-8

import sys
import MySQLdb
import redis
import MySQLdb.cursors
import tornadoredis
import logging
from tornadoredis.client import PUB_SUB_COMMANDS

#PUB_SUB_COMMANDS.append('PUBLISH')

CONNECT_CLASS = {
    'redis': redis.Redis,
    'mysql': MySQLdb.connect,
    'tornadoredis': tornadoredis.Client,
}


class ConnectPool(object):
    _cache = {}
    connects = {}

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
        #self.connects = {}
        #logging.info('storage size: %s' % sys.getsizeof(self))

    def rawget(self, db_name):
        """ 获取指定类型的数据库连接

        目前只用户注册redis lua脚本
        """
        params = self.env.settings.DATABASES[db_name]
        db_direct = CONNECT_CLASS['redis']

        return db_direct(**params)

    def get(self, field, carrier=None, long_connect=False):
        """ 
        """
        if carrier:
            db_name = carrier.DATABASE
        else:
            db_name = field.get_database()

        params = self.env.settings.DATABASES[db_name]
        db_direct = CONNECT_CLASS[field.STORAGE_TYPE]

        if isinstance(params, dict):
            key = db_name
            db_params = params
        else:
            if carrier:
                shared_key = carrier.pk % len(params)
            else:
                shared_key = field.shared_key

            key = "%s.%d" % (db_name, shared_key)
            db_params = params[shared_key]

        conn = self.connects.get(key)

        #logging.info('connect1: %s %r' % (key, conn))
        if not long_connect and conn:
            return conn

        conn = db_direct(**db_params)
        self.connects[key] = conn
        #logging.info('connect2: %s %r' % (key, conn))

        return conn

    def __del__(self):
        for conn in self.connects.itervalues():
            if hasattr(conn, 'close'):
                conn.close()


class Storage(object):
    def __init__(self, env):
        """
        """
        #logging.info('storage init: %r %r' % (env, env.env))
        self.env = env
        self.connects = ConnectPool(env)

    def save(self, obj):
        """
        """
        for field in obj.important:
            item = getattr(obj, field)
            #logging.info('storage save: %r %r' % (field, item.changed))

            if item.changed:
                connection = self.connects.get(item, obj)
                item.save(connection, field, obj)

                if item.CACHE_TYPE and obj.CACHE_ENABLE:
                    if item.reload_cache:
                        stmt = self.select(field, obj)
                        item.loader(stmt)
                        stmt.close()

                    self.env.cache.set(obj, field)

                item.finish_save()

    def select(self, attr_name, carrier):
        """
        """
        attr = getattr(carrier, attr_name)

        connection = self.connects.get(attr, carrier)
        cursor = connection.cursor()
        cursor.execute(*attr.sql_select(attr_name, carrier))

        return cursor

