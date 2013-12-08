# coding: utf-8

import re
import numpy
import itertools
from collections import defaultdict

from . import trans

def wrapper_lines(seq, lines, mapping, filter_func=all):
    trans_map = trans.group_keys(seq, mapping)

    for row in itertools.ifilter(filter_func, lines):
        item = {}

        for name, factory in trans_map.iteritems():
            item[name] = trans.trans_field(factory, row)

        yield item['pk'], item


def mapinfo(mapping):
    def wrapper(seq, lines):
        obj = {}
        trans_map = trans.group_keys(seq, mapping)

        for row in lines:
            item = {}

            for name, factory in trans_map.iteritems():
                item[name] = trans.trans_field(factory, row)

            pk = item.pop('pk')
            item['size']['y'] -= item['useless']

            field = numpy.zeros((item['size']['y'],
                                 item['size']['x']),
                                dtype=int)

            for x in xrange(item['size']['x']):
                for y in xrange(item['size']['y']):
                    field[y][x] = y * item['size']['x'] + x

            max_pos = field[y][x]

            attack = []
            defend = []

            for value in item['positions']:
                attack.append(field[value['y'] - 1][value['x'] - 1])

            for value in item['epositions']:
                defend.append(field[value['y'] - 1][value['x'] - 1])

            obj[pk] = {
                'size': (item['size']['x'], item['size']['y'] + item['useless']),
                'pixel': item['pixel'],
                'focus': item['focus'],
                'attack': attack,
                'defend': defend,
                'useless': item['useless'],
                'max_pos': max_pos,
            }

        return obj

    return wrapper


def battle_emenity(mapping):
    def wrapper(seq, lines):
        from instantft.battle.skill import CURE_ATTACK
        from instantft.battle.skill import MAGIC_ATTACK
        from instantft.battle.skill import NORMAL_ATTACK

        obj = {
            0: {},  # direct attack
            NORMAL_ATTACK: {},
            MAGIC_ATTACK: {},
            CURE_ATTACK: {},
        }

        for pk, item in wrapper_lines(seq, lines, mapping):
            direct = {}

            for hero_id, value in enumerate(item['emenity']):
                direct[hero_id] = value

            obj[0][pk] = direct

            if item['normal']:
                obj[NORMAL_ATTACK][pk] = item['normal']

            if item['cure']:
                obj[CURE_ATTACK][pk] = item['cure']

            if item['anger']:
                obj[MAGIC_ATTACK][pk] = item['anger']

        return obj

    return wrapper


def monster_drop(mapping):
    def wrapper(seq, lines):
        obj = {}

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):

            pk = item.pop('pk', pk)
            weight = 0
            weights = []
            goods = []

            for key, value in item.iteritems():

                if not value['weight']:  # 没有权重直接过滤
                    continue

                if key != 'none':
                    for g in value['goods']:
                        goods.append((key, g))
                else:
                    goods.extend(((key, value['goods']),))

                for w in value['weights']:
                    weights.append(weight + w)

                weight += value['weight']

            obj[pk] = {
                 'weight': weight,
                 'weights': weights,
                 'goods': goods
                }

        return obj

    return wrapper


def skill_buff(mapping):
    def wrapper(seq, lines):
        obj = {}

        for pk, item in wrapper_lines(seq, lines, mapping, any):
            effect = []
            effect.append((item['effect1'], item['cycle1'],
                           item['percent1'], item['ability_add1'],
                           item['value1'], item['durations'],
                           item['affected']))

            if item['effect2']:
                effect.append((item['effect2'], item['cycle2'],
                               item['percent2'], item['ability_add2'],
                               item['value2'], item['durations'],
                               item['affected']))

            obj[pk] = tuple(effect)

        return obj

    return wrapper


def equip_resolve(mapping):
    def wrapper(seq, lines):
        config = {}

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            data = config.setdefault(pk, {})
            obj = data.setdefault(item['sort'], {})

            for key, value in item['data'].iteritems():
                weight = value['none']
                weights = [weight]
                goods = [('none', [])]

                for good in value['material']:
                    g, w = tuple(good[:3]), good[-1]
                    weight += w
                    weights.append(weight)
                    goods.append(('material', g))

                obj[key] = {
                    'weight': weight,
                    'weights': weights,
                    'goods': goods,
                }

        return config

    return wrapper


def material(mapping):
    def wrapper(seq, lines):
        config = {}

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            data = config.setdefault(item['star'], {})
            obj = data.setdefault(item['sort'], [])

            obj.append(item['pk'])

        return config

    return wrapper


def equip_merge(mapping):
    def wrapper(seq, lines):
        config = {}

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            destiny_type = item.pop('destiny_type')
            data = config.setdefault(destiny_type, [])

            data.append(pk)

        return config

    return wrapper


def goblin_get(mapping):
    def wrapper(seq, lines):
        configs = {}

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            weight = 0
            weights = []
            goods = []

            for idx, value in enumerate(item['weight']):
                if value:
                    weight += value
                    weights.append(weight)
                    goods.append(('goblin', item['item'][idx]))

            configs[pk] = {
                'point': item['point'],
                'level': item['level'],
                'loot': {
                    'weight': weight,
                    'weights': weights,
                    'goods': goods,
                }}

        return configs

    return wrapper


def arena_award(mapping):
    def wrapper(seq, lines):
        ranks = []
        configs = []

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):

            ranks.append(item['end_rank'])
            configs.append(item)

        return {
            'ranks': ranks,
            'configs': configs,
            'min_idx': 0,
            'max_idx': len(ranks) - 1,
        }

    return wrapper


def goblin_position(mapping):
    def wrapper(seq, lines):
        open_level = []
        open_ku = []
        configs = []

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):

            open_level.append(item['open_level'])
            open_ku.append(item['open_ku'])
            configs.append(item)

        return {
            'open_level': open_level,
            'open_ku': open_ku,
            'configs': configs,
            'min_idx': 0,
            'max_idx': len(open_level) - 1,
        }

    return wrapper

def pet_skill_star(mapping):
    def wrapper(seq, lines):
        configs = {}

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            skills = configs.setdefault(item['star'], [])
            skills.append(pk)

        return configs

    return wrapper

def pet(mapping):
    def pet_seq_groups(seq):
        match = re.compile('quality(\d)_sen(\d)').match

        return [map(int, match_obj.groups())
                for match_obj in itertools.imap(match, seq)]

    def wrapper(seq, lines):
        configs = {}
        star_clone_seq = pet_seq_groups(seq[1:])

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            star_data = {}

            for (star, clone), exp in itertools.izip(star_clone_seq, item['detail']):
                clone_data = star_data.setdefault(star, {})
                clone_data[clone] = exp

            configs[pk] = star_data

        return configs

    return wrapper


def file_configs(config_files):
    """生成配置文件到配置项的映射
    """
    configs = {}

    for config_key, filename in config_files.iteritems():

        config_keys = configs.setdefault(filename, [])
        config_keys.append(config_key)

    return configs


def world_map(mapping):
    def wrapper(seq, lines):
        areas = set()
        items = []

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            area = item['area']

            if not area in areas:
                items.append({'area': area, 'name': 'name'})
                areas.add(area)

        items.sort(key=lambda x: x['area'])

        return {'items': items}

    return wrapper


def chapter_map(mapping):
    def wrapper(seq, lines):
        background = {'image': 'battle_map.png'}
        configs = {}
        area_chapter = defaultdict(set)

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            area, chapter = item['area'], item['chapter']

            if chapter not in area_chapter[area]:
                chapter_data = configs.setdefault(area, {'items': [],
                                                         'background': background})
                chapter_data['items'].append({
                                        'chapter': chapter,
                                        'name': item['chapter_name'],
                                        'image': 'battle.png',
                                        'x': 80,
                                        'y': 80})
                area_chapter[area].add(chapter)

        return configs

    return wrapper


def stage_map(mapping):
    def wrapper(seq, lines):
        configs = {}

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            data = configs.setdefault(item['chapter'], {'items': []})
            data['items'].append({
                'icon': item.get('icon', '1.png'),
                'stage': pk,
                'name': item['name'],
                'side': 1,
                'difficult': item['difficult'],
            })

        return configs

    return wrapper


def chapter_stage(mapping):
    def wrapper(seq, lines):
        world_area = set()
        area_chapter = defaultdict(set)
        chapter_stage = defaultdict(set)

        for pk, item in wrapper_lines(seq, lines, mapping, filter_func=any):
            area, chapter, stage = item['area'], item['chapter'], pk

            world_area.add(area)
            area_chapter[area].add(chapter)
            chapter_stage[chapter].add(stage)

        return {
            'world_area': sorted(world_area),
            'area_chapter': dict((area, sorted(chapters))
                                  for area, chapters in area_chapter.iteritems()),
            'chapter_stage': dict((chapter, sorted(stages))
                                  for chapter, stages in chapter_stage.iteritems()),
        }

    return wrapper

