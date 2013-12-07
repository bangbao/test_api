# coding: utf-8

import os

DEBUG = True

ENVIRONMENT = os.environ.get('gameenv', 'dev')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
APP_ROOT = os.path.join(PROJECT_ROOT, 'apps')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
LOGS_ROOT = os.path.join(PROJECT_ROOT, 'logs')
TMP_ROOT = os.path.join(PROJECT_ROOT, 'tmp')
TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, 'templates')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')


ENVIRONS = {
    'develop:0.0.2': (PROJECT_ROOT, 1),
    #'develop:0.0.1': (PROJECT_ROOT, 2),
    #'environ': (PROJECT_ROOT, 4),
}

execfile(os.path.join(APP_ROOT, 'settings', '%s.py' % ENVIRONMENT), globals(), locals())

TORNADO_SETTINGS = {
    'debug': DEBUG,
    'template_path': TEMPLATE_ROOT,
    'static_path': STATIC_ROOT,
    'ui_modules': {},
    'ui_methods': {},
    'static_url_prefix': '/static/',
    #'static_handler_class': StaticFileHandler,
    #'static_handler_args': {},
    #'log_function': lambda handler: None,
    'cookie_secret': '123213213123123',
    #'template_loader': template.Loader,
    #'autoescape': True,
    'login_url': '/login/',
    #'xsrf_cookies': True,
    'gzip': True,
} 
