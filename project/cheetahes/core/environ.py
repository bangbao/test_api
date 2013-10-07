# coding: utf-8

from cheetahes.core.storage import Storage
from cheetahes.core.cache import Cache

import os
import imp
import sys
import hashlib

RUNTIME_OK = 0
RUNTIME_ERROR = 1
RUNTIME_INFO = 2
RUNTIME_WARN = 4


class Environ(object):
    """
    """
    ENVIRON_PARAMS_NAME = 'Environ_name'
    ENVIRON_DOCUMENT_ROOT_NAME = 'Document_root'
    GLOBAL_ENVIRON = 'environ'
    BASE_SUB_ENVIRON = 'environs'
    DEFAULT_ENVIRON = 'defaults'
    CURRENT_ENVIRON = 'current'
    APP_FOLDER_NAME = 'apps'
    API_FOLDER_NAME = 'apis'
    FILTER_FOLDER_NAME = 'filters'

    _cache = {}

    def __new__(cls, env_id, document_root):
        """
        """
        super_new = super(Environ, cls).__new__

        obj = cls._cache.get(env_id)

        if not obj:
            obj = cls._cache[env_id] = super_new(cls, env_id, document_root)
            setattr(obj, '_modules', {})
            setattr(obj, '_paths', {})

        return obj

    def __init__(self, env_id, document_root):
        """
        """
        self.identity = env_id
        self.document_root = document_root

    def app_path(self):
        """
        """
        object_list = self._paths.get('app_path', [])
        
        if not object_list:
            if not self.is_global():
                object_list = self.join_path(self.APP_FOLDER_NAME)

            object_list.append(os.path.join(self.document_root, 
                                            self.APP_FOLDER_NAME))
        return object_list

    def api_path(self):
        """
        """
        object_list = self._paths.get('api_path', [])

        if not object_list:
            if not self.is_global():
                object_list = self.join_path(self.APP_FOLDER_NAME,
                                             self.API_FOLDER_NAME)

            object_list.append(os.path.join(self.document_root, self.APP_FOLDER_NAME,
                                            self.API_FOLDER_NAME))

        return object_list

    def filter_path(self):
        """
        """
        object_list = self._paths.get('filter_path', [])

        if not object_list:
            if not self.is_global():
                object_list = self.join_path(self.APP_FOLDER_NAME,
                                             self.FILTER_FOLDER_NAME)

            object_list.append(os.path.join(self.document_root, self.APP_FOLDER_NAME,
                                         self.FILTER_FOLDER_NAME))

        return object_list

    def join_path(self, *args):
        """
        """
        env, version = self.identity.split(':')

        return [os.path.join(self.document_root, self.BASE_SUB_ENVIRON,
                           env, version, *args),
                os.path.join(self.document_root, self.BASE_SUB_ENVIRON,
                           self.DEFAULT_ENVIRON, version, *args),
                os.path.join(self.document_root, self.BASE_SUB_ENVIRON,
                              env, self.CURRENT_ENVIRON, *args)]

    def is_global(self):
        """
        """
        return self.identity == self.GLOBAL_ENVIRON

    def multi(self):
        """
        """
        return False

    def import_module(self, module, path):
        """
        """
        for subpath in path:
            module_id = '%s/%s' % (subpath, module)
            obj = self._modules.get(module_id)

            try:
                if not obj:
                    obj = imp.load_module(module,
                                          *imp.find_module(module, [subpath]))
                    self._modules[module_id] = sys.modules.pop(module)

                return obj
            except ImportError:
                continue

        raise ImportError, "no module named %s" % module


class APIEnviron(object):
    """
    """
    METHOD_ARGUMENT_NAME = 'method'

    @classmethod
    def build_env(cls, req, short_id):
        """
        """
        env_id = req.request.headers[Environ.ENVIRON_PARAMS_NAME]
        document_root = req.request.headers[Environ.ENVIRON_DOCUMENT_ROOT_NAME]

        env = Environ(env_id, document_root)

        return cls(req, env, short_id)

    def __init__(self, req, env, short_id):
        """
        """
        self.req = req
        self.env = env
        self.short_id = short_id
        self.errno = 0
        self.msg = None
        self.headers = {}
        self.errno = RUNTIME_OK
        self.storage = Storage(self)
        self.cache = Cache(self)
        self.callbacks = []

        self.app_path = env.app_path()
        self.filter_path = env.filter_path()
        self.api_path = env.api_path()
        self.settings = self.import_module('settings', self.app_path)
        self.authenticate = True

        self.user = req.get_current_user(self)
        self.game_config = None
        self.params = {}

    def finish(self):
        self.params = None
        self.game_config = None

    def set_config_loader(self, loader_cls):
        """
        """
        self.game_config = loader_cls(self)

    def resolve_name(self, module_suffix=''):
        """
        """
        param = self.req.get_argument(self.METHOD_ARGUMENT_NAME)

        return param.split('.')

    def hash_caches(self, name):
        """
        """
        sid = int(hashlib.md5(name).hexdigest(), 16) % self.settings.CACHES_LEN

        return sid, self.settings.CACHES[sid]

    def generate_cache_key(self, carrier, attr_name):
        """
        """
        return "%d.c.%s.%s.%d" % (self.short_id, carrier.NAME,
                                  attr_name, carrier.pk)

    def generate_store_key(self, carrier, attr_name):
        """
        """
        return "%d.s.%s.%s" % (self.short_id, carrier.NAME,
                               attr_name)

    def api_filter(self, module, method):
        """
        """
        try:
            api_filter = self.import_module(module, self.filter_path)
            filter_method = getattr(api_filter, method, None)

            if callable(filter_method):
                return filter_method(self)

        except ImportError:
            self.params = self.req.summary_params()

    def api_method(self, module, method):
        """
        """
        api_module = self.import_module(module, self.api_path)
        api_method = getattr(api_module, method, None)

        if callable(api_method):
            return api_method(self)

    def import_module(self, module, path):
        """
        """
        if self.env.multi():
            user = self.req.get_current_user()

            return self.env.import_module(module, path)

        return self.env.import_module(module, path)

    def import_app(self, app_name):
        """
        """
        return self.import_module(app_name, self.app_path)

    def api(self):
        """
        """
        module, method = self.resolve_name()
        module_api = "%s_api" % module
        module_filter = "%s_filter" % module
        
        if self.api_filter(module_filter, method):
            return None

        return self.api_method(module_api, method)


class AdminEnviron(APIEnviron):
    """
    """
    API_FOLDER_NAME = 'admin'

    def __init__(self, req, env, short_id):
        """
        """
        self.req = req
        self.env = env
        self.short_id = short_id
        self.errno = 0
        self.msg = None
        self.headers = {}
        self.errno = RUNTIME_OK
        self.storage = Storage(self)
        self.cache = Cache(self)
        self.callbacks = []

        self.app_path = env.app_path()
        self.api_path = self._api_path()
        self.settings = self.import_module('settings', self.app_path)
        self.authenticate = True

        self.user = None
        self.game_config = None
        self.params = {}

    def _api_path(self):
        """
        """
        object_list = []

        for app_path in self.app_path:
            api_path = os.path.join(app_path, self.API_FOLDER_NAME)

            object_list.append(api_path)

        return object_list

    def api(self):
        """
        """
        admin_app = self.import_app('admin')

        func_path = admin_app.URL_MAPPING.get(self.req.request.path, '.')
        module, method = func_path.rsplit('.', 1)

        return self.api_method(module, method)

    def render(self, template_path, data=None, **kwargs):
        """
        """
        if data is None:
            data = {}

        data.update(kwargs)

        return template_path, data


class ShellEnviron(APIEnviron):
    @classmethod
    def build_env(cls, env_id=Environ.GLOBAL_ENVIRON, document_root='.'):
        env = Environ(env_id, os.path.abspath(document_root))

        return cls(env)

    def __init__(self, env):
        """
        """
        self.env = env
        self.short_id = None
        self.errno = 0
        self.msg = None
        self.headers = {}
        self.errno = RUNTIME_OK
        self.storage = Storage(self)
        self.cache = Cache(self)

        self.app_path = env.app_path()
        self.filter_path = env.filter_path()
        self.api_path = env.api_path()
        self.settings = self.import_module('settings', self.app_path)
        self.user = None
        self.authenticate = False

        self.params = {}
        self.game_config = None

    def set_short_id(self, short_id):
        self.short_id = short_id

    def set_user(self, uid):
        self.user = None

