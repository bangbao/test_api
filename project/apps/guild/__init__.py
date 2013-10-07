# coding:utf-8

import time
from models import Guild
from models import Guilds
from cheetahes.db.expressions import Incr

GUILD_MASTER = 1
GUILD_MEMBER = 99

PERM_APPLY = 1
PERM_PROMOTED = 2
PERM_IMPEACH = 3
PERM_DISBAND = 4

PERMISSIONS = {
    GUILD_MASTER: set((PERM_APPLY, PERM_PROMOTED, PERM_IMPEACH, PERM_DISBAND)),
    GUILD_MEMBER: set(),
}

def pre_use_guild(env):
    """ 公会对象使用前的处理

    主要作用是处理公会解散时，游戏数据里的索引重置
    """

    user = env.user

    if user.game.info['guild'] and not user.guild:
        user.game.info['guild'] = 0

def guild_index(env):
    """ 公会首页

    当用户属于一个公会时返回所属公会的最近状态，
    当用户没有公会时返回全服公会列表
    """

    game = env.user.game

    if game.info['guild']:
        return guild_info(game.info['guild'])
    else:
        return guild_intro()

def guilds(env):
    """ 获取指定数量的公会
    
    公会列表翻页
    """

    pass

def create_guild(env):
    """ 创建公会
    
    使用同用户创建相同的方法，需要在一个单独的表里存放索引
    公会数据散列存放
    """

    game_app = env.import_app('game')

    user = env.user
    kcoin = env.params['kcoin']
    gold = env.params['gold']

    guilds = Guilds(None)
    guilds.data['env_id'] = env.short_id
    env.storage.save(guilds)

    guild = Guild(guilds.pk)
    guild.info['name'] = env.params['name']
    env.storage.save(guild)

    add_member(guild, user, GUILD_MASTER)

    game_app.incr_user_attr(user, kcoin=-kcoin, gold=-gold)

    user.save_all()

    return guild.info

def request_guild(env):
    """ 申请加入公会

    用户对一个公会发出加入申请，
    当公会需要审批时进入审批列表，否则直接加入公会
    """

    guild = env.params['guild']
    user = env.user

    if guild.info['need_apply']:
        guild.load_apply4.add(guild.pk, {
            'msg': env.params['msg'],
            'uid': user.pk})
    else:
        add_member(guild, user, GUILD_MEMBER)

    user.save_all()

def apply_guild(env):
    """ 同意加入公会申请

    审批某用户加入公会的请求, 把用户加入成员列表
    删除加入申请
    """
    
    user = env.suer
    member = env.params['member']

    user.guild.apply4.remove(user.pk)
    add_member(user.guild, user, GUILD_MEMBER)

    user.save_all()

def reject_guild_request(env):
    """ 拒绝加入公会请求

    拒绝申请用户加入公会， 直接删除加入申请
    """

    user = env.user
    user_id = env.params['user_id']

    user.guild.apply4.remove(user_id)

    user.save_all()

def quit_guild(env):
    """ 退出公会

    退出公会，当会长退出时视为解散公会
    """

    user = env.user
    user.game.info['guild'] = 0
    user.guild.members.remove(user.pk)
    user.guild.info['members'] = Incr('members', -1, user.guild)

    if env.params['disband']:
        guild_disband(env, user)

    user.save_all()

def promoted_member(env):
    """ 提升某个会员的权限
    """

    power = env.params['power']
    user_id = env.params['user_id']

    user.guild.members.modify(user_id, {'power': power})
    user.save_all()

def impeach(env):
    """ 弹劾提定指定用户的权限
    """

    pass

def add_exp(env, guild_id, exp):
    """ 为公会添加经验
    """

    pass

def add_member(guild, user, power):
    """ 将一个用户加入公会成员列表
    
    公会加入新用户

    Args:
       env: 运行环境
       guild: 公会对象
       user: 用户对象(新成员对象)
       power: 在公会中的身份
    """

    guild.members.add(user.pk, power=power)
    guild.info['members'] = Incr('members', 1, guild)
    user.guild = guild

def get_member_top(env, guild):
    """ 获取公会成员上限

    目前公会成员上限只和公会等级关联，等级越高成员上限越高

    Args:
       env: 运行环境
       guild: 公会对象

    Returns:
       公会成员上限
    """

    return 20

def get_member_free(env, guild):
    """ 获取公会空闲位置

    当发起申请或批准加入公会时，需要保证有空闲位置加入

    Args:
       env: 运行环境
       guild: 公会对象
    
    Returns:
       公会空闲位置数量
    """

    mtop = guild_app.get_member_top(env, guild)

    return mtop - guild.info['members']

def has_guild_perm(guild, user, action):
    """ 判断用户是否有权限执行指定操作

    Args:
       guild: 公会对象
       user: 用户对象
       action: 将要执行的动作

    Returns:
       是否可以继续
    """

    if not user:
        return False

    role = guild.members[user.pk]['power']

    return action in PERMISSIONS[role]

def get_guild(guild_id):
    """ 获取公会对象

    通过公会id获取公会对象

    Args:
       guild_id: 公会id

    Returns:
       公会对象
    """

    return Guild(guild_id)

def guild_disband(env, user):
    """ 公会解散，清除公会数据

    清除公会所有数据

    Args:
       env: 运行环境
       user: 用户对象(会长)
    """
    
    conn = env.storage.connects.get(Guilds.data, Guilds)
    cursor = conn.cursor()

    query = ("DELETE FROM %s_data "
             "WHERE id=%s AND env_id=%s") % (Guilds.NAME, '%s', '%s')
    cursor.execute(query, [user.guild.pk, env.short_id])

    user.game.info['guild'] = 0
    user.guild.members.reset()
    user.guild.apply4.reset()
