# coding: utf-8


PET_SKILL_SEQ = [0, 1, 2, 3, 4, 5]
PET_SKILL_UNOPENED = 'unopened'
PET_SKILL_DEFAULTS = {
    'none': PET_SKILL_UNOPENED,
}

PET_FULL_EFFECT = {
    'full': [0.6, 0.8],
    'effect': [0.5, 0.8, 1],
}
PET_EFFECT_ATTRS = ('hp', 'natk', 'ndef', 'matk', 'mdef')
PET_SKILL_SORT_MAP = {
    1: 'hp',
    2: 'natk',
    3: 'ndef',
    4: 'matk',
    5: 'mdef',
    6: 'hit',
    7: 'dodge',
    8: 'storm_hit',
    9: 'holdout_storm',
    10: 'crt_damage',
    11: 'final_damage',
    12: 'final_nerf',
    13: 'rage',
}

PET_FOOD_ABiLITY_MAP = {
    0: None,
    1: 'hp',
    2: 'natk',
    3: 'ndef',
    4: 'matk',
    5: 'mdef',
}
PET_FOOD_TYPE_MAP = {
    'like': (1.2, 1.2, 1),  # (exp, attr, full)
    'wary': (0.8, 0.8, 0.6),
    'common': (1, 1, 0.8),
}
PET_FULL_REDUCE_CYCLE_SECENDS = 180
PET_FULL_REDUCE_RATIO = 0.01
PET_refresh_skill_nums = [1, 2, 3, 4, 5, 6]
pet_refresh_skill_cost = [1, 10, 30, 50, 100, 200]
pet_fefresh_skill_cost_default = 1
