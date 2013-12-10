# coding: utf-8

import re
import time
import datetime

from lib.db.fields import ModelDict
from lib.db.fields import ModelList
from apps import config as config_app


class Form(object):
    """后台表单类
    
    输出后台功能的HTML表单，以及处理表单数据
    支持ModelDict和ModelList类型。
    
    Attributes：
        field: Model类的属性名称，例如game类的info
        field_obj: Model类的属性对象。
        config: 后台功能的相关配置。
        req: RequestHandler对象
    """
    def __init__(self, env, field, field_obj, config, req=None):
        self.env = env
        self.field = field
        self.field_obj = field_obj
        self.config = config
        self.req = req
        
    def show(self):
        """输出HTML表单
        
        Returns:
            HTML代码字符串
        """
        field = self.field
        config = self.config[field]
        data = self.field_obj

        html_list = []
        if config['type'] == 'list':
            #ModelList类型
            field_config = config_app.get_config(self.env, config['cname'])
            info_config = self.config[field].get('info', {})
            used_set = data.pop('used_set', [])

            for pk, one in data.iteritems():
                if used_set and pk in used_set:
                    one['used_st'] = True
                else:
                    one['used_st'] = False
                group_html = config['group'][0](pk, one, field_config, info_config)
                html_list.append(group_html)

        else:
            #ModelDict类型
            for val in config['values']:
                value = data[val]
                val_html = config["values"][val][0](value, val)
                html_list.append(val_html)
                    
        context = ''.join(html_list)

        return config['desc'](context, field)
    
    def mdictdata(self):
        """整理ModelDict数据
        
        接收表单数据，并整理成符合当前ModelDict对象的dict
        dict中增加一个changed值来标示是否有数据修改
        
        Retruns:
            表单数据的字典
        """
        data = self.field_obj
        config = self.config[self.field]
        
        changed = False
        value_dict = {}
        for val in config['values']:
            
            value = config['values'][val][1](self.req, val)
            value_dict[val] = value
            
            if not changed and value != data[val]:
                changed = True
                
        value_dict['form_changed'] = changed
            
        return value_dict
        
        
    def mlistdata(self):
        """整理ModelList数据
        
        接收表单数据，并整理成符合当前ModelList对象的Dict
        
        Returns:
            pk: 当前表单对应的主键
            mdata: 当前表单对应的数据的字典
            changed: 是否有值修改
        """
        pk = self.req.get_argument('pk', '')

        if pk.isdigit():
            pk = int(pk)

        data = self.field_obj[pk]
        config = self.config[self.field]

        mdata = config['group'][1](self.req)

        changed = False
        for key, value in mdata.iteritems():
            if value != data[key]:
                changed = True
                break
        
        return pk, mdata, changed
    
        
