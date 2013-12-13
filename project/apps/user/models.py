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

    def __init__(self, env, pk, read_only=False):
        """
        """
        super(User, self).__init__(pk, read_only)

        self.env = weakref.proxy(env)
        self.on_loaded = []

        game_app = env.import_app('game')
        hero_app = env.import_app('hero')
        adven_app = env.import_app('adven')
        arena_app = env.import_app('arena')

        if not read_only:
            self.on_loaded = [
                game_app.pre_use_game,
                hero_app.pre_use_hero,
                arena_app.pre_use_arena,
            ]

        self.game = game_app.Game(pk, read_only)
        self.hero = hero_app.Hero(pk, read_only)
        self.adven = adven_app.Adven(pk, read_only)
        self.arena = arena_app.Arena(pk, read_only)

    def hash_db_shared(self):
        """
        """
        return self.pk % self.env.settings.DATABASE_CLUSTERS

    def load_base(self):
        """默认加载一些常用的数据表
        """
        self.game.load_info()
        self.game.load_user()

        self.hero.load_data()
        self.adven.load_adven()
        self.arena.load_data()

    def load_fight(self, members=None):
        """加载战斗所需的数据
        """
        self.game.load_info()
        self.game.load_user()
        self.game.load_equip()
        self.game.load_goblin()
        self.game.load(self.env)

        hero_app = self.env.import_app('hero')
        equip_app = self.env.import_app('equip')
        goblin_app = self.env.import_app('goblin')
        pet_app = self.env.import_app('pet')

        team = hero_app.team_get(self)
        used_equip = equip_app.get_used_equip(self)
        used_goblin = goblin_app.get_used_goblin(self)
        played_pet = pet_app.get_played_pet(self)

        hero_keys = team + members if members else team
        self.hero.load_heros(keys=hero_keys)
        self.hero.load_equips(keys=used_equip.keys())
        self.hero.load_goblins(keys=used_goblin.keys())
        self.hero.load_pets(keys=[played_pet])
        self.hero.load(self.env)

    def load_all(self):
        """统一加载数据，并处理一些前置数据
        """
        self.game.load(self.env)
        self.hero.load(self.env)
        self.adven.load(self.env)
        self.arena.load(self.env)

        for pre_use in self.on_loaded:
            pre_use(self.env)

        self.on_loaded = []

    def save_all(self):
        """统一保存用户数据
        """
        self.env.storage.save(self.game)
        self.env.storage.save(self.hero)
        self.env.storage.save(self.adven)
        self.env.storage.save(self.arena)

    def reset_all_data(self):
        """重置用户所有数据
        """
        self.game.reset_all(self.env)
        self.hero.reset_all(self.env)
        self.adven.reset_all(self.env)
        self.arena.reset_all(self.env)

    def load_all_data(self):
        """加载用户所有数据
        """
        self.game.load_all(self.env)
        self.hero.load_all(self.env)
        self.adven.load_all(self.env)
        self.arena.load_all(self.env)

