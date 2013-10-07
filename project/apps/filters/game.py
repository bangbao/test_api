# coding: utf-8

def load(env):
    """
    """

    game_app = env.import_app('game')

    return game_app.game_load(env)
