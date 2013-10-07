# coding: utf-8

def top_hp(diff):
    def wrapper(agent):
        agent.hp -= diff

    return wrapper
