# coding: utf-8


def destiny_effect1(obj, detail, game_config):
    """
    """
    obj['hp'] += detail['value1']
    obj['hp'] += int(obj['bf_init']['hp'] * detail['value2'] / 100.0)


def destiny_effect2(obj, detail, game_config):
    ""
    ""
    obj['natk'] += detail['value1']
    obj['natk'] += int(obj['bf_init']['natk'] * detail['value2'] / 100.0)


def destiny_effect3(obj, detail, game_config):
    """
    """
    obj['ndef'] += detail['value1']
    obj['ndef'] += int(obj['bf_init']['ndef'] * detail['value2'] / 100.0)


def destiny_effect4(obj, detail, game_config):
    """
    """
    obj['matk'] += detail['value1']
    obj['matk'] += int(obj['bf_init']['matk'] * detail['value2'] / 100.0)


def destiny_effect5(obj, detail, game_config):
    """
    """
    obj['mdef'] += detail['value1']
    obj['mdef'] += int(obj['bf_init']['mdef'] * detail['value2'] / 100.0)


def destiny_effect6(obj, detail, game_config):
    """
    """
    obj['rage'] += detail['value1']


def destiny_effect7(obj, detail, game_config):
    """
    """
    skill_cfg_id = detail['value1']
    obj['normal_skill'] = game_config['skill_data'][skill_cfg_id]


def destiny_effect8(obj, detail, game_config):
    """
    """
    skill_cfg_id = detail['value1']
    obj['destiny_skill'] = game_config['skill_data'][skill_cfg_id]

