# coding: utf-8

from __future__ import with_statement

import os
import csv
import logging

from . import trans
from .transfer import CONFIG_MAPPING


def import_file(filename, mapping):
    """解析单个csv文件

    Args:
        filename: csv文件路径
        mapping: 配置映射关系

    Returns:
        解析后的配置内容
    """
    config = {}

    with open(filename, 'rb') as _fp:
        try:
            fp = csv.reader(_fp)
            row = fp.next()

            if callable(mapping):  # special
                return mapping(row, fp)

            trans_map = trans.group_keys(row, mapping)

            for row in fp:
                if not any(row):
                    continue

                item = {}

                for name, factory in trans_map.iteritems():
                    try:
                        item[name] = trans.trans_field(factory, row)
                    except Exception, e:
                        print name
                        logging.info("%s \t %s" % (name, e))
                        raise

                pk = item.pop('pk')

                config[pk] = item

            return config
        except Exception, e:
            print 'filename:', filename
            print 'line_num:', fp.line_num
            print 'row:', row
            raise e


def static_import(env, filepath, save=True):
    """批量导入csv文件

    Args:
        env: 运行环境
        filepath: csv文件目录
        save: 是否直接保存
    """
    from transfer import FILE_CONFIGS
    from transfer import CONFIG_MAPPING

    config_app = env.import_app('config')

    for filename, config_keys in FILE_CONFIGS.iteritems():
        realfile = os.path.join(filepath, '%s.csv' % filename)

        if os.path.exists(realfile):
            for name in config_keys:
                value = import_file(realfile, CONFIG_MAPPING[name])
                if save:
                    config_app.set_config(env, name, value)


if __name__ == '__main__':
    filename = r'E:\mini_dota\cehua\csv\map_stage.csv'
    # filename = '/Users/zhangjames/Work/rekoo/cehua/导入CSV/map_info.csv'
    print import_file(filename, CONFIG_MAPPING['chapter_stage'])


