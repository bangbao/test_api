# coding: utf-8

import umysqldb


REDIS_DEFAULT = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': 'F8974044A778',
    'socket_timeout': 5,
}

MYSQL_DEFAULT = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '510312',
    'db': 'lose',
    'port': 3306,
    'unix_socket': '/var/run/mysqld/mysqld.sock',
    'cursorclass': umysqldb.cursors.DictCursor,
}

DATABASES = {
    'lose': dict(MYSQL_DEFAULT, db='lose'),
    'redis': dict(REDIS_DEFAULT, db=0),
    'chat': dict(REDIS_DEFAULT, db=0),
    'auth': dict(MYSQL_DEFAULT, db='auth'),
    'clusters': [
        dict(MYSQL_DEFAULT, db='cm1'),
        dict(MYSQL_DEFAULT, db='cm2'),
        dict(MYSQL_DEFAULT, db='cm3'),
        dict(MYSQL_DEFAULT, db='cm4'),
    ],
}

CACHES = [
    dict(REDIS_DEFAULT, db=10),
    # dict(REDIS_DEFAULT, db=11),
    # dict(REDIS_DEFAULT, db=12),
    # dict(REDIS_DEFAULT, db=13),
]

CACHES_LEN = len(CACHES)
CACHE_KEY_DELAY_SECONDS = 300
REDIS_PRELOAD_HOSTS = 'redis'

