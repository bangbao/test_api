# coding: utf-8

import re
import time
import itertools


def iftrueto(func, defalut=None):
    def decorator(value):
        if value:
            return func(value)
        else:
            return defalut

    return decorator


def datetime_format(fmt):
    def decorator(value):
        return int(time.mktime(time.strptime(value, fmt)))

    return decorator


def halve(func=int):
    def decorator(value):
        halve_value = (float(value) - 1) / 2
        return func(halve_value)

    return decorator


def percentage(value):
    return int(value) / 100.


def delimiter_str(delimiter, map_func, tp_func=list):
    def decorator(value):
        if not value:
            return []

        return tp_func(map(map_func, value.split(delimiter)))

    return decorator


def delimiter_list(func):
    def decorator(*value):
        obj = []

        for val in value:
            obj.append(func(val))

        return obj

    return decorator


def delimiter_random(delimiter, map_func):
    def decorator(value):
        if not value:
            return [0, 0]

        obj = map(map_func, value.split(delimiter))

        if len(obj) == 1:
            obj *= 2

        return obj

    return decorator


def delimiter_dict(delimiter, keys):
    def decorator(value):
        if not value:
            return {}

        obj = {}

        for i, val in enumerate(value.split(',')):
            if keys[i][1]:
                obj[keys[i][0]] = keys[i][1](val)
            else:
                obj[keys[i][0]] = val

        return obj

    return decorator


def filtertrue_list(map_func):
    def decorator(*args):
        return [map_func(v) for v in args if v]

    return decorator


def mapping_list(map_func):
    def decorator(*args):
        return map(map_func, args)

    return decorator


def regex_list(pattern):
    re_obj = re.compile(pattern)

    def decorator(value):
        return re_obj.findall(value)

    return decorator


def single_good(*funcs):
    def decorator(*args):
        goods = [func(args[i])
                 for i, func in enumerate(funcs[:-1])]

        weight = funcs[-1](args[-1])

        return {
            'weight': weight,
            'goods': [tuple(goods)],
            'weights': [weight],
        }

    return decorator


def none_good(value):
    weight = int(value)

    return {
        'weight': weight,
        'goods': [],
        'weights': [weight],
    }


def multi_good(keys):
    def decorator(*args):
        good_dict = {}
        weight = 0
        weights = []
        goods = []

        for i, value in enumerate(args):
            if not value:
                continue

            good_dict[keys[i][0]] = keys[i][1](value)

        for key, value in good_dict.iteritems():
            if key != 'none':
                for g in value['goods']:
                    if type(g) not in (list, tuple):
                        goods.append((key, (g,)))
                    else:
                        goods.append((key, g))
            else:
                goods.extend(((key, value['goods']),))

            for w in value['weights']:
                weights.append(weight + w)

            weight += value['weight']

        if not goods:
            return None

        return {
             'weight': weight,
             'weights': weights,
             'goods': goods
            }

    return decorator


def multi_good_item(item):
    good, weight = item

    return (tuple(map(int, good.split(','))), int(weight))


def multi_good_weight_item(item):
    good, weight = item
    good_list = good.split(',')
    good_list.append(weight)
    return (tuple(map(int, good_list)), int(weight))


def good_list(pattern, map_func=None):
    re_obj = re.compile(pattern)

    def decorator(value):
        weight = 0
        weights = []
        goods = []

        for v in re_obj.findall(value):
            if map_func:
                g, w = map_func(v)
            else:
                g, w = map(int, v)

            weight += w
            weights.append(weight)
            goods.append(g)


        if not goods:
            return None

        return {
            'weight': weight,
            'weights': weights,
            'goods': goods,
        }

    return decorator


def multi_good_list(pattern, keys):
    sub_obj = good_list(pattern)

    def decorator(*args):
        weight = 0
        weights = []
        goods = []

        for key, sub_goods in ((keys[i], sub_obj(value)) \
                           for i, value in enumerate(args)):

            for w, g in itertools.izip(sub_goods['weights'], sub_goods['goods']):
                goods.append((key, g))
                weights.append((weight + w))

            weight += sub_goods['weight']

        return {
             'weight': weight,
             'weights': weights,
             'goods': goods,
            }

    return decorator


def index_int(value):
    return int(value) - 1 # index begin 0


def kind_list(num, names):
    def decorator(*args):
        obj = []
        step = len(names)
        length = len(args) / step
        base = 0
        slen = step

        for i in xrange(0, len(args), step):
            item = {}
            x1, x2 = args[i:slen]

            item[names[0][0]] = names[0][1](x1)
            item[names[1][0]] = names[1][1](x2)

            slen += step

            obj.append(item)

        return obj

    return decorator


def kind_dict(groups, keys):
    def decorator(*args):
        length = len(args)
        obj = {}

        for i, group in ((i, args[i * groups: i * groups + groups]) \
                      for i in xrange(length / groups)):
            sub_obj = {}

            for j, key in enumerate(keys[i][1]):
                if key[1]:
                    sub_obj[key[0]] = key[1](group[j])
                else:
                    sub_obj[key[0]] = group[j]

            obj[keys[i][0]] = sub_obj

        return obj

    return decorator


def list_join(delimiter):
    def decorator(*args):
        return delimiter.join(map(str, args))
    return decorator


def group2format(keys):
    def decorator(*args):
        weight = 0
        weights = []
        goods = []
        for i, (key, func) in enumerate(keys):
            if func:
                attr = func(args[i])
            else:
                attr = args[i]
            weight += attr[-1]
            weights.append(weight)
            goods.append(attr)
        if not goods:
            return None

        return {
            'weight': weight,
            'weights': weights,
            'goods': goods,
            }

    return decorator


def group2dict(keys):
    def decorator(*args):
        obj = {}

        for i, (key, func) in enumerate(keys):
            if func:
                obj[key] = func(args[i])
            else:
                obj[key] = args[i]

        return obj

    return decorator


def liststr2dict(value):
    return dict(eval('[%s]' % value))


def group_dict_list(pattren):
    def decorator(value):
        obj = {}
        data = pattren.findall(value)

        for key, val in data:
            if key in obj:
                obj[int(key)] += map(int, val.split(','))
            else:
                obj[int(key)] = map(int, val.split(','))

        return obj

    return decorator


def key_mapping(seq, keys):
    fields = {}
    for i, field in enumerate(seq):
        if field in keys:
            fields[field] = i

    return fields


def ascii_str(encoding='utf-8'):
    def decorator(value):
        return unicode(value, encoding)

    return decorator


def hashmap_value(key_func, value_func):
    def decorator(seq, lines):
        obj = {}

        for key, value in (row[0:2] for row in lines if any(row)):
            obj[key_func(key)] = value_func(value)

        return obj

    return decorator


def icon(ext='_i'):
    def decorator(image):
        return image + ext

    return decorator


def second2frame(value):
    return int(float(value) * 10)


def value2bool(value):
    try:
        return bool(int(value))
    except ValueError:
        return False


def percent(base):
    def decorator(value):
        return base + (float(value) * 0.01)

    return decorator

