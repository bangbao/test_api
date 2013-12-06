# coding: utf-8

import MySQLdb
import MySQLdb.cursors

mysql_host = 'localhost'
mysql_port = 3306
mysql_user = 'root'
mysql_passwd = '510312'
mysql_cursorclass = MySQLdb.cursors.DictCursor

DATABASES = {
    'lose': {
        'host': 'localhost',
        'user': 'root',
        'passwd': '510312',
        'db': 'lose',
        'port': 3306,
        'unix_socket': '/var/run/mysqld/mysqld.sock',
        'cursorclass': MySQLdb.cursors.DictCursor,
    },
    'redis': {
        'host': 'localhost',
        'port': 6379, 
        'db': 0,
    },
    'chat': {
        'host': 'localhost',
        'port': 6379, 
    },
    'auth': {
        'host': 'localhost',
        'user': 'root',
        'passwd': '510312',
        'db': 'auth',
        'port': 3306,
        'unix_socket': '/var/run/mysqld/mysqld.sock',
        'cursorclass': MySQLdb.cursors.DictCursor,
    },
    'clusters': [
       {
            'host': 'localhost',
            'user': 'root',
            'passwd': '510312',
            'db': 'cm1',
            'port': 3306,
            'unix_socket': '/var/run/mysqld/mysqld.sock',
            'cursorclass': MySQLdb.cursors.DictCursor,
       },
       {
            'host': 'localhost',
            'user': 'root',
            'passwd': '510312',
            'db': 'cm2',
            'port': 3306,
            'unix_socket': '/var/run/mysqld/mysqld.sock',
            'cursorclass': MySQLdb.cursors.DictCursor,
       },
       {
            'host': 'localhost',
            'user': 'root',
            'passwd': '510312',
            'db': 'cm3',
            'port': 3306,
            'unix_socket': '/var/run/mysqld/mysqld.sock',
            'cursorclass': MySQLdb.cursors.DictCursor,
       },
       {
            'host': 'localhost',
            'user': 'root',
            'passwd': '510312',
            'db': 'cm4',
            'port': 3306,
            'unix_socket': '/var/run/mysqld/mysqld.sock',
            'cursorclass': MySQLdb.cursors.DictCursor,
       }
    ],
}

CACHES = [
    {'host': 'localhost', 'port': 6379, 'db': 0},
    {'host': 'localhost', 'port': 6379, 'db': 0},
    {'host': 'localhost', 'port': 6379, 'db': 0},
    {'host': 'localhost', 'port': 6379, 'db': 0},
]

CACHES_LEN = len(CACHES)
CACHE_KEY_DELAY_SECONDS = 300
REDIS_PRELOAD_HOSTS = 'redis'

