# coding: utf-8


def skill_effect1(obj, detail, game_config):
    """
    """
    obj['hp'] += detail['value1']
    obj['hp'] += int(obj['bf_init']['hp'] * detail['value2'] / 100.0)


