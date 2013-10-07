# coding: utf-8

def info(env):
    """
    """

    user_app = env.import_app('user')

    return user_app.user_info(env)
