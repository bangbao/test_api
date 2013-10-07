# coding: utf-8
from apps import notify as notify_app
import constants

def index(env):
    """
    """

    pass

@notify_app.checker
def create(env):
    """
    """

    name = env.req.get_argument('name')
    guild_app = env.import_app('guild')

    if not name:
        return constants.GUILD_NAME_EMPTY
        
    user = env.user
    user.guild.load_info()
    user.load_all()

    if user.user['kcoin'] < constants.CREATE_GUILD_COST_KCOIN:
        return constants.GUILD_KCOIN_NOT_ENOUGH

    if user.user['gold'] < constants.CREATE_GUILD_COST_GOLD:
        return constants.GUILD_GOLD_NOT_ENOUGH

    if user.game.info['guild']:
        return constants.GUILD_JOINED_EXISTS

    env.params['name'] = name
    env.params['kcoin'] = constants.CREATE_GUILD_COST_KCOIN
    env.params['gold'] = constants.CREATE_GUILD_COST_GOLD

@notify_app.checker
def request(env):
    """
    """

    user = env.user
    guild_id = env.req.get_argument('guild_id')
    msg = env.req.get_argument('msg')

    guild_app = env.import_app('guild')

    user.load_all()

    if user.game.info['guild']:
        return constants.GUILD_JOINED_EXISTS

    guild = guild_app.get_guild(guild_id)
    guild.load_info()
    guild.load(env)

    if not guild.pk:
        return constants.GUILD_NOT_EXISTS

    free = guild_app.get_member_free(env, guild)
        
    if free < 1:
        return constants.GUILD_IS_FULL

    env.params['guild'] = guild
    env.params['msg'] = msg

@notify_app.checker
def apply(env):
    """
    """

    user = env.user
    guild_id = env.req.get_argument('guild_id')
    member_id = env.req.get_argument('member_id')
    guild_app = env.import_app('guild')
    user_app = env.import_app('user')

    user.guild.load_info()
    user.guild.load_members(keys=[user.pk])
    user.guild.load_apply4(keys=[member_id])
    user.load_all()

    if not user.guild:
        return constants.GUILD_NOT_EXISTS

    if not guild_app.has_guild_perm(user.guild, user, guild_app.PERM_APPLY):
        return constants.NOT_HAS_GUILD_PERM

    free = guild_app.get_member_free(env, user.guild)
        
    if free < 1:
        return constants.GUILD_IS_FULL

    if not member_id in user.guild.apply4:
        return constants.REQUEST_MEMBER_NOT_EXISTS

    member = user_app.get_user(env, member_id)

    if not member:
        return constants.REQUEST_MEMBER_NOT_EXISTS

    member.game.load_info()
    member.game.load(env)

    if member.game.info['guild']:
        return constants.USER_IS_A_GUILD_MEMBER

    env.params['member'] = member

@notify_app.checker
def reject(env):
    """
    """

    member_id = env.req.get_argument('member_id')
    guild_app = env.import_app('guild')
    user_app = env.import_app('user')

    user = env.user
    user.guild.load_members(keys=[user.pk])
    user.guild.load_apply4(keys=[member_id])
    user.load_all()

    if not guild_app.has_guild_perm(user.guild, user, guild_app.PERM_APPLY):
        return constants.NOT_HAS_GUILD_PERM

    if member_id not in user.guild.apply4:
        return constants.NOT_HAS_APPLY_REQUEST

    env.params['user_id'] = member_id

@notify_app.checker
def promoted(env):
    """
    """

    member_id = env.req.get_argument('member_id')
    power = env.req.get_argument('power')
    user_app = env.import_app('user')
    
    user = env.user
    user.guild.load_info()
    user.guild.load_members(key=[member_id, user.pk])
    user.load_all()

    user_power = user.guild.members[user.pk]['power']
    member_power = user.guild.members[member_id]['power']

    if user_power < power or member_power > user_power:
        return constants.PERM_RANGE_OVERFLOW

    env.params['user_id'] = member_id
    env.params['power'] = power

@notify_app.checker
def quit(env):
    """ 
    """

    guild_app = env.import_app('guild')
    user = env.user
    user.guild.load_members(keys=[user.pk])

    user.load_all()

    disband = user_power == guild_app.GUILD_MASTER and \
              not guild_app.has_guild_perm(user.guild, user, 
                                           guild_app.PERM_DISBAND)

    if disband:
        user.guild.load_members()
        user.guild.load_apply4()
        user.load_all()

    env.params['disband'] = disband
