# coding: utf-8


GOBLIN_TEAM_POS_KEYS = ('pos0', 'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6', 'pos7')

GOBLIN_FROM_INIT = 0
GOBLIN_FROM_FORGE = 2
GOBLIN_FROM_ADMIN = 3

GOBLIN_MASTER_UP_CYCLE_DAYS = 3
# GOBLIN_MASTER_UP_KCOIN_TIMES = 5
# GOBLIN_MASTER_UP_KCOIN_COST = 5
GOBLIN_FORGE_DAILY_TIMES = 50
GOBLIN_FORGE_DELTA = 10
GOBLIN_DEFAULT_MASTERS = '0,0,0,0'
GOBLIN_DEFAULT_MASTER_TYPES = ('point', 'crt', 'effect', 'luck')
GOBLIN_FORGE_MODES = [
    {'gold': 500, 'kcoin': 0, 'effect': 1},
    {'gold': 0, 'kcoin': 2, 'effect': 1.2},
    {'gold': 0, 'kcoin': 5, 'effect': 1.5},
    {'gold': 0, 'kcoin': 10, 'effect': 2},
]
GOBLIN_FORGE_POINT_MIN = 40
GOBLIN_FORGE_POINT_MAX = 160
GOBLIN_FORGE_POINT_CRT_DEFAULT = 1
GOBLIN_FORGE_POINT_INSPIRE_DEFAULT = 0
GOBLIN_FORGE_POINT_INSPIRE_RATE = 10
GOBLIN_FORGE_POINT_INSPIRE_AREA = (1, 1)
GOBLIN_FORGE_POINT_INSIGHT_RATE = 10
GOBLIN_FORGE_POINT_INSIGHT_AREA = (0, 1, 2, 3)
GOBLIN_EXP_TYPE_NOT_MERGE = 0
GOBLIN_EFFECT_SORT_MAP = {
    0: None,
    1: 'natk',  # 英雄物理攻击力
    2: 'ndef',  # 英雄物理防御力
    3: 'hp',  # 英雄血量
    4: 'matk',  # 英雄魔法攻击力
    5: 'mdef',  # 英雄魔法防御力
    6: 'hit',  # 命中
    7: 'dodge',  # 闪避
    8: 'storm_hit',  # 暴击率
    9: 'crt_damage',  # 暴击伤害
    10: 'holdout_storm',  # 暴击抵抗
    11: 'final_damage',  # 最终伤害
    12: 'final_nerf',  # 最终减免
}

GOBLIN_POS_HOLE_DEQ = [0, 1, 2, 3, 4, 5]
GOBLIN_POS_HOLE_UNOPENED = 'unopened'
GOBLIN_POS_HOLE_DEFAULTS = {
    'none': GOBLIN_POS_HOLE_UNOPENED,
}


