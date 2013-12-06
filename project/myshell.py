#!/usr/bin/python 
#! coding: utf-8

import time
import sys
import os


uid = 2
target_id = 1
static_config = False
dev1 = ('develop:0.0.1', 2)
#dev2 = ('develop:0.0.1', 2)
dev2 = ('develop:0.0.2', 1)

env_id, short_id = dev2

argv = sys.argv[1:]
if argv:
    s = argv[0]
    if s == 'config':
        static_config = True
    elif s == 'dev1':
        env_id, short_id = dev1
    else:
        uid = int(s) or uid


########################################################
from lib.core.environ import ShellEnviron
#from lib.db.expressions import Incr 
from apps import config as config_app
from apps import settings


env = ShellEnviron.build_env(env_id)
env.set_short_id(short_id)
env.set_config_loader(config_app.AppCacheConfig)
config_app.loadall(env)
g = game_config = env.game_config


############import app######################################
pwd = os.path.dirname(os.path.abspath(__file__))
apps_root = os.path.join(pwd, 'apps')
for root, dirs, files in os.walk(apps_root):
    for dname in dirs:
        func = "%s_app = env.import_app('%s')" % (dname, dname)
        try:
            exec(func)
            #print 'import %s success' % dname
        except ImportError:
            pass
            #print 'import %s failtrue' % dname

#user_app = env.import_app('user')
#game_app = env.import_app('game')
#hero_app = env.import_app('hero')
#adven_app = env.import_app('adven')
#arena_app = env.import_app('arena')
#equip_app = env.import_app('equip')
#destiny_app = env.import_app('destiny')
#goblin_app = env.import_app('goblin')
#chat_app = env.import_app('chat')
#pet_app = env.import_app('pet')

##########end import app##################################

#########import config csv##################
path = './csv'
from apps.config.logics import static_import 
if static_config:
    static_import(env, path)
    print '-----static import config: success'
############################################

u = user = user_app.get_user(env, uid)
target = user_app.get_user(env, target_id)
env.user = u

u.game.load_arena()
u.game.load_award()
u.game.load_all(env)
u.hero.load_all(env)
u.adven.load_all(env)
u.arena.load_all(env)

def pickler(data):

    delimiter = ','
    team = data['team']

    if isinstance(team, list):
        temp = [obj or '' for obj in team]
        data['team'] = delimiter.join(temp)
    
    return repr(data)
    
def unpickler(data):
    
    data = eval(data)
    team = data['team']
    delimiter = ','
    
    if not isinstance(team, list):
        temp = team.split(delimiter)
        data['team'] = [obj or None for obj in temp]
    
    return data


def add_hero(env, pk, cfg_id=2, num=1):
    user_app = env.import_app('user')
    hero_app = env.import_app('hero')

    u = user_app.get_user(env, pk)

    u.game.load_user()
    u.game.load_info()
    u.game.load(env)

    u.hero.load_data()
    u.hero.load_heros()
    u.hero.load(env)

    env.user = u

    for i in xrange(num):
        hero_app.birth_hero(env, cfg_id)

    env.storage.save(u.hero)


def add_heros(env, pk, num=10):
    user_app = env.import_app('user')
    hero_app = env.import_app('hero')

    u = user_app.get_user(env, pk)

    u.game.load_user()
    u.game.load_info()
    u.game.load(env)

    u.hero.load_data()
    u.hero.load_heros()
    u.hero.load(env)

    env.user = u

    for i in xrange(num):
        for j in xrange(1, 7):
            hero_app.birth_hero(env, j)

    env.storage.save(u.hero)

#for i in xrange(36, 40):
#    for j in xrange(8, 13):
#        print i, j 
#        add_hero(env, i, j, 5)


#for i in xrange(1, 40):
#    u = user_app.get_user(env, i)
#    u.adven.load_adven()
#    u.adven.adven['stage'] = 12
#    env.storage.save(u.adven) 
#    print i

#for uid in xrange(1, 40):
#    u = user_app.get_user(env, uid)
#    env.user = u
#    u.hero.load_equips()
#    u.hero.load(env)
#
#    for i in xrange(1, 7):
#        print hero_app.equip.birth_equip(env, i)
#
#    u.save_all()

    
def get_used_equip(user):
    """获取使用中的装备id
    """

    equip = user.game.equip
    used_equip = set()
    
    for pos in constants.EQUIP_TEAM_POS_KEYS:
        pos_list = logics.delimiter_list(equip[pos])
        used_equip.update(pos_list)

    used_equip.discard(None)

    return used_equip


#u1 = user_app.get_user(env, 2)
#u1.hero.load_all(env)
#u2 = user_app.get_user(env, 16)
##u2.hero.load_all(env)
#env.user = u1

a = arena = u.game.arena
#a.init(env, 'arena', u.game)
b = award = u.game.award
#b.init(env, 'award', u.game)

#a.incr(0)

def get_all_users():
    for uid in range(1, 50):
        u = user_app.get_user(env, uid)
        yield u

all_users = get_all_users()

def add_user_in_arena():
    for user in get_all_users():
        user.game.load_arena()
        user.game.load_all(env)
        user.arena.load_all(env)
        arena = user.game.arena
        score = user.arena.data['rank_score']
       
        if score:
            print user.pk, score
            arena.zadd(float(score))

def test_user_in_arena():
    for uid in range(1, 21):
        u = user_app.get_user(env, uid)
        a = u.game.arena
        a.incr(uid)
        print a.nearby_pos(100, 100, 1)

def test_username():
    for uid in xrange(1, 31):
        u = user_app.get_user(env, uid)
        u.game.load_info()
        u.game.load(env)
        u.game.info['username'] = u.game.info['username'] or u.data['token'] + str(uid)
        u.save_all()
        print u.game.info['username']

def trash_goblin():
    goblins = game_config['goblins']

    for u in all_users:
        u.hero.load_goblins()
        u.hero.load(u.env)

        for gid, obj in u.hero.goblins.iteritems():
            if obj['cfg_id'] not in goblins:
                print gid
                u.hero.goblins.remove(gid)

        u.save_all()

def add_goblin(user):
    goblins = game_config['goblins']
    for cfg_id in goblins:
        goblin_app.birth_goblin(user, cfg_id)
    user.save_all()

def add_pet(user):
    pets = game_config['pets']
    for cfg_id in pets:
        pet_app.birth_pet(user, cfg_id)
    user.save_all()

def cron_strengthen_ratio(env):
    """
    """

    import random
    now = int(time.time())
    base_ratio, up, up_time = game_config['strengthen_ratio'] 

    quotient, remainder = divmod(now - up_time, 10)

    MAX_RATIO = 100
    MIN_RATIO = 75

    if quotient > 0:
        up_time = now - remainder
        change_ratio = random.randint(5, 8)

        ratio = (base_ratio + change_ratio) if up else (base_ratio - change_ratio)
        if not MIN_RATIO <= ratio <= MAX_RATIO:
            limit_ratio = MAX_RATIO if ratio > MAX_RATIO else MIN_RATIO
            up = not up
            ratio = limit_ratio - (ratio - limit_ratio)

        print base_ratio, change_ratio, '|||', ratio, up, up_time
        config_app.set_config(env, 'strengthen_ratio',
                              (ratio, up, up_time))


import redis 

r = redis.Redis(host='127.0.0.1', port=16379)
