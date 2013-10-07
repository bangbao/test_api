# coding: utf-8

DATABASES = {
    'main': {'host': 'localhost',
             'passwd': '111111',
             'user': 'root',
             'db': 'main',
         },
    'storages': {
        'mc1': {'host': 'localhost', 'passwd': '111111', 'user': 'root', 'db': 'm1'},
        'mc2': {'host': 'localhost', 'passwd': '111111', 'user': 'root', 'db': 'm2'},
        'mc3': {'host': 'localhost', 'passwd': '111111', 'user': 'root', 'db': 'm3'},
        'mc4': {'host': 'localhost', 'passwd': '111111', 'user': 'root', 'db': 'm4'}
    }
}

CACHES = {
    'main': {
        'mc1': {'host': 'localhost', 'port': 6379, 'db': 0},
        'mc2': {'host': 'localhost', 'port': 6379, 'db': 0},
    },
    'caches': {
        'cc1': {'host': 'localhost', 'port': 6379, 'db': 0},
        'cc2': {'host': 'localhost', 'port': 6379, 'db': 0},
        'cc3': {'host': 'localhost', 'port': 6379, 'db': 0},
        'cc4': {'host': 'localhost', 'port': 6379, 'db': 0},
    }
}
