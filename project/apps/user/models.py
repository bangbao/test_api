# coding: utf-8

import uuid
import hashlib
import weakref

from lib.db import Carrier
from lib.db.fields import ModelDict
from lib.db.metaclass import DynamicModel


USER_DATABASE = 'auth'
USER_MODEL_NAME = 'user'
FIELD_KEY = 'data'


class CarrierUser(Carrier):
    def init(self):
        self.data = ModelDict({
                        'username': '',
                        'password': '',
                        'salt': '',
                        'token': ''})


class NewUser(CarrierUser):
    __metaclass__ = DynamicModel
    NAME = USER_MODEL_NAME
    DATABASE = USER_DATABASE
    FIELD_KEY = FIELD_KEY
    FIELDS = [FIELD_KEY]

    @classmethod
    def create(cls, env, token, password):
        obj = cls(None)  # primary key is None
        salt = str(uuid.uuid1())
        salt_password = salt + password
        obj.data['salt'] = salt
        obj.data['password'] = hashlib.sha1(salt_password).hexdigest()
        obj.data['token'] = token

        env.storage.save(obj)

        return obj.pk


class User(CarrierUser):
    """用户模块

    必须定义的类属性:
        NAME: 模块名
        DATABASE: 所用的settings中哪个数据库
        FIELDS: 定义游戏属性, 其中key用于与NAME组合成数据库表名, value为定义的属性集合

    Attributes:
        FIELD_KEY: FIELDS属性的key，方便直接使用
        data:
            username: 用户帐号
            password: 用户密码
            salt: 用户注册时生成的salt
            token: 用户标识
    """
    __metaclass__ = DynamicModel
    NAME = USER_MODEL_NAME
    DATABASE = USER_DATABASE
    FIELD_KEY = FIELD_KEY
    FIELDS = [FIELD_KEY]

    @classmethod
    def create(cls, env, token, password):
        """
        """
        uid = NewUser.create(env, token, password)

        return cls(env, uid)

    def __init__(self, env, pk, read_only=True):
        """
        """
        super(User, self).__init__(pk, read_only)

        self.env = weakref.proxy(env)
        self.on_loaded = []

        if not read_only:
            self.on_loaded = []

    def hash_db_shared(self):
        """
        """
        return self.pk % self.env.settings.DATABASE_CLUSTERS

    def load_all(self):
        """统一加载数据，并处理一些前置数据
        """

    def save_all(self):
        """统一保存用户数据
        """



