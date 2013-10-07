# coding: utf-8
import os
import imp
import sys

cache_stage = {}
STAGE_PATH = [os.path.abspath(os.path.dirname(__file__))]

def get_polt(script_name):
    """ 获取剧情脚本模块

    Args:
       script_name: 剧情脚本名称
    
    Returns:
       剧情脚本模块
    """

    polt = cache_stage.get(script_name)

    if not polt:
        polt = imp.load_module(script_name, 
                               *imp.find_module(script_name, STAGE_PATH))
        cache_stage[script_name] = sys.modules.pop(script_name)

    return polt
