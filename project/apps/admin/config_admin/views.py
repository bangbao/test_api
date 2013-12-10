# coding: utf-8

from __future__ import with_statement
import json

from lib.core.environ import ShellEnviron
from apps import config as config_app
from apps.settings import ENVIRONS
from apps.config.transfer import FILE_CONFIGS, CONFIG_MAPPING
from . import constants


def index(env, config_name='', config_version=None, config_value=None):
    """后台配置首页面
    """
    envs = {}
    for env_id in ENVIRONS:
        envs[env_id] = constants.TEXT.get(env_id, env_id)

    return env.render('admin/config/index.html', {'envs': envs,
                                                  'env_id': env.env.identity,
                                                  'configs': FILE_CONFIGS,
                                                  'game_config': env.game_config,
                                                  'game_configs': {},
                                                  'config_name': config_name,
                                                  'config_version': config_version,
                                                  'config_value': config_value,
                                                })

def show(env):
    """动态显示配置内容
    """
    env_id = env.req.get_argument('env_id')
    config_filename = env.req.get_argument('config_filename')
    new_env = shell_env(env_id)

    config_keys = FILE_CONFIGS[config_filename]
    config_name = config_keys[0]
    config_version = 11111111
    config_value = env.game_config[config_name]

    return json.dumps({
        'config_name': config_name, 
        'config_verison': config_version, 
        'config_value': config_value
    })

def upload(env):
    """上传配置文件

    TODO:
        需根据不同的env_id生成环境，现默认使用当前环境
    """
    env_id = env.req.get_argument('env')
    config_filename = env.req.get_argument('config_filename')
    config_file = env.req.request.files.get('config_file')

    new_env = shell_env(env_id)

    config_keys = FILE_CONFIGS[config_filename]
    filepath = backup_file(config_file)

    for name in config_keys:
        value = config_app.logics.import_file(filepath, CONFIG_MAPPING[name])
        config_app.set_config(new_env, name, value)

    return index(env)

def reloadall(env):
    """重新加载运行环境配置

    TODO:
        需根据不同的env_id生成环境，现默认使用当前环境
    """
    env_id = env.req.get_argument('env')

    new_env = shell_env(env_id)
    config_app.loadall(new_env)

    return index(env)

def backup_file(file_obj):
    """备份并生成配置文件

    tornado 上传文件会自动把文件内容保存在内存里，不会有临时文件

    Args:
        file_obj: tornado的文件对象

    Returns:
        保存的对应文件路径
    """
    filename = file_obj[0]['filename']
    filebody = file_obj[0]['body']
    filepath = filename

    with open(filepath, 'wb') as _fp:
        _fp.write(filebody)

    return filepath

def shell_env(env_id):
    """根据env_id生成一个新的环境对象
    """
    root, short_id = ENVIRONS[env_id]
    env = ShellEnviron.build_env(env_id, document_root=root)
    env.set_short_id(short_id)
    env.set_config_loader(config_app.AppCacheConfig)

    return env


