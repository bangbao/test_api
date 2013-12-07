# coding: utf-8

import time as te
import datetime

MSG = {
    'ID_ERROR': u'请输入正确数据',
    'NO_USER': u'用户不存在',
    'SUCCESS': u'操作成功',
}

def add_panel(uid, mname, field, count, params=None):
    """生成添加ModelList元素的HTML

    Args:
        uid: 用户ID
        field: Model类的属性名称，例如game类的info
        params: 添加时需要的参数

    Returns:
        HTML代码字符串
    """
    param_html = []
    if params:
        for param_info in params:
            name = 'add_%s' % param_info[0]
            param_html.append((u'%s: <input class="addinput"'
                               u'type="text" name="%s" value="%s" />') 
                               % (param_info[1], name, param_info[2]))
    param_str = '&nbsp;&nbsp;'.join(param_html)

    add_html = (u'<table><tr><td><form action="/admin/%s/add/" method="post">%s'
                u'<input type="hidden" name="uid" value="%s" />'
                u'<input type="hidden" name="field" value="%s" />'
                u'&nbsp;&nbsp;<button type="submit" '
                u'onClick="return confirm(\'确定添加吗？\')">添加</button>'
                u'&nbsp;&nbsp;物品数量：%s</form></td><td>'
                u'<form action="/admin/%s/reset/" method="post">'
                u'<input type="hidden" name="uid" value="%s" />'
                u'<input type="hidden" name="field" value="%s" />'
                u'<button class="reset" type="submit" '
                u'onClick="return confirm(\'确定清空吗？\')">清空</button>'
                u'</form></td></tr></table>') \
                % (mname, param_str, uid, field, count, mname, uid, field)

    return add_html

def field_to_form(label, mname):
    """生成ModelDict数据表单页面框架

    Args:
        label: 模块当前属性中文名称
        mname: 模块名

    Returns:
        HTML代码字符串
    """
    def html(context, field):
        """
        Args:
            context: 表单页面主体内容
            field: 当前表单对应的属性的名称
        """

        return (u'<form action="/admin/%s/save/" method="post">'
                u'<table id="mindata">%s</table><other_params_panel>'
                u'<input type="hidden" name="field" value="%s" />'
                u'<button type="submit" '
                u'onClick="return confirm(\'确定保存吗？\')">保存</button></form>'
                u'<form action="/admin/%s/reset/" method="post"><other_params_panel>'
                u'<input type="hidden" name="field" value="%s" />'
                u'<button class="reset" type="submit" '
                u'onClick="return confirm(\'确定重置吗？\')">重置</button></form>'
                u'</form>') % (mname, context, field, mname, field)

    return html

def value_to_form(label):
    """生成ModelDict数据中某一值的HTML

    Args:
        label: 当前字段中文名称

    Returns:
        HTML代码字符串
    """
    def html(value, val):
        """
        Args:
            value: 字段值
            val: 字段名
        """
        if isinstance(value, str):
            try:
                value = value.decode('utf-8')
            except UnicodeDecodeError:
                value = repr(value)
            
        return (u'<tr><td>%s</td>'
                u'<td><input type="" name="%s" value="%s" />' 
                u'</td></tr>') % (label, val, value)

    return html

def value_to_form_time(label):
    """时间数据生成表单

    将time类型的数据转换为(%Y-%m-%d %H:%M:%S)的字符串

    Args:
        label: 当前字段中文名称

    Returns:
        HTML代码字符串
    """

    def html(value, val):
        """
        Args:
            value: 字段值
            val: 字段名
        """

        if not value:
            showtime = ''
        else:
            tmptime = datetime.datetime.fromtimestamp(int(value))
            showtime = tmptime.strftime('%Y-%m-%d %H:%M:%S')

        return (u'<tr><td>%s</td>'
                u'<td><input type="" name="%s" value="%s" /></td>'
                u'</tr>') % (label, val, showtime)

    return html

def value_to_form_team(label):
    """以','分隔的字符串数据生成表单

    将数据以','拆分并且分别使用input标签显示

    Args:
        label: 当前字段中文名称

    Returns:
        HTML代码字符串
    """

    def html(value, val):
        """
        Args:
            value: 字段值
            val: 字段名
        """

        val_list = value.split(',')

        count = len(val_list)
        html_str = [u'<tr><td>%s</td><td>' %label]

        for i in range(count):
            key = u'%s_%s' % (val, i)
            block = '' if i == count-1 else '<br/>'
            html_str.append(u'<input type="text" name="%s" value="%s" />%s' \
                            % (key, val_list[i], block))

        hidden_key = '%s_len' %val
        html_str.append(u'<input type="hidden" name="%s" value="%s" /></td></tr>' \
                        % (hidden_key, count))

        return  ''.join(html_str)

    return html

def toint(req, key):
    """接收整型数据

    Args:
        req: RequestHandler对象
        key: 表单对象的name属性，字段名

    Returns:
        整型数据
    """

    return int(req.get_argument(key, 0))

def tostr(req, key):
    """接收字符数据

    Args:
        req: RequestHandler对象
        key: 表单对象的name属性，字段名

    Returns:
        字符串数据
    """

    value = req.get_argument(key, '')

    return value

def totime(req, key):
    """接收并处理时间数据

    将接收到的(%Y-%m-%d %H:%M:%S)时间字符串转换为time格式

    Args:
        req: RequestHandler对象
        key: 表单对象的name属性，字段名

    Returns:
        time类型数据
    """

    value = req.get_argument(key, '')

    if not value:
        realtime = 0
    else:
        tmptime = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        realtime = te.mktime(tmptime.timetuple())

    return realtime

def toteam(req, key):
    """接收并处理以','分隔字符串类型的表单数据

    接收多个input数据并还原到字符串格式

    Args:
        req: RequestHandler对象
        key: 表单对象的name属性，字段名

    Returns:
        字符串数据
    """

    hidden_key = '%s_len' % key
    count = int(req.get_argument(hidden_key, ''))

    val_list = []
    for i in range(count):
        val_key = '%s_%s' % (key, i)
        val_list.append(req.get_argument(val_key, ''))

    return ','.join(val_list)

def group_field_to_form(label, labels, sort):
    """生成ModelList数据表单页面框架

    Args:
        label: 模块当前属性中文名称
        labels: 字段中文名称字典
        sort: 字段名排序集合

    Returns:
        HTML代码字符串
    """

    def html(context, field):
        """
        Args:
            context: 表单页面主体内容
            field: 当前表单对应的属性的名称
        """

        label_html = ''
        if context:
            #处理表头
            label_tmp = [u'<tr><th>PK</th><th>名称</th>']

            for val_key in sort:
                one_label = u'<th>%s</th>' % labels[val_key]
                label_tmp.append(one_label)

            label_tmp.append(u'<th colspan="2">操作</th></tr>')
            label_html = u''.join(label_tmp)

        return (u'<table id="info"><tr><td><static_panel></td></tr>'
                u'<tr><td><add_panel></td></tr></table>'
                u'<table id="data">%s%s</table>'
                u'<input type="hidden" name="field" value="%s"/>') \
                % (label_html, context, field)

    return html

def group_to_form(labels, funcs, sort):
    """生成ModelList数据表单主体内容

    Modellist数据中各项的修改、删除操作各使用一个form

    Args:
        label: 模块当前属性中文名称
        funcs: 字段展示及接受处理方法字典
        sort: 字段名排序集合

    Returns:
        HTML代码字符串
    """

    def html(pk, all_data, field_config, info_config):
        """
        Args:
            pk: 主键
            all_data: 字段值得字典
            field_config: 当前模块属性的配置
                          用于显示未存在数据库的信息
            info_config: 说明信息配置
        """

        where = ''
        if 'cfg_id' not in all_data and isinstance(pk, int):
            hname = field_config[pk]['name']

        else:
            hname = field_config[all_data['cfg_id']]['name']
            where = u'title="来源：%s"' % getwhere(pk, info_config)

        used = all_data.pop('used_st') if 'used_st' in all_data else False
        high = u'color:#AE0000;font-weight:bold' if used else ''

        html_tmp = [(u'<tr><form action="/admin/hero/modify/" method="post">'
                    u'<td %s>%s'
                    u'<input type="hidden" name="pk" value="%s" />'
                    u'<other_params_panel>'
                    u'</td><td style="%s">%s</td>') 
                    % (where, pk, pk, high, hname)]

        for val_key in sort:
            show_func = funcs[val_key][0]
            one_html = show_func(val_key)(all_data[val_key])

            html_tmp.append(one_html)

        alow_del = u'disabled="disabled"' if used else ''

        html_tmp.append((u'<td><button type="submit" '
                        u'onClick="return confirm(\'确定修改吗？\')">'
                        u'修改</button></td></form>'
                        u'<form action="/admin/hero/delete/" method="post">'
                        u'<td><input type="hidden" name="pk" value="%s" />'
                        u'<other_params_panel>'
                        u'<button type="submit" %s '
                        u'onClick="return confirm(\'确定删除吗？\')">删除</button>'
                        u'</td></form></tr>') % (pk, alow_del))

        return u''.join(html_tmp)

    return html

def one_to_group(name):
    """生成ModelList中某一项的某一个值的HTML

    Args:
        name: 字段名

    Returns:
        HTML代码字符串
    """

    def html(value):
        """
        Args:
            value: 字段值
        """

        if isinstance(value, str):
            value = value.decode('utf-8')

        return (u'<td><input class="inp" type="text" name="%s" value="%s" />'
                u'</td>') % (name, value)

    return html

def one_to_group_no(name):
    """生成ModelList中某一项的某一个值的HTML

    展示数据，无法修改

    Args:
        name: 字段名

    Returns:
        HTML代码字符串
    """

    def html(value):
        """
        Args:
            value: 字段值
        """

        if isinstance(value, str):
            value = value.decode('utf-8')

        if name == 'cfg_id':
            return u'<td>%s<input type="hidden" name="%s" value="%s"/></td>' \
                    % (value, name, value)
        else:
            return u'<td>%s</td>' % value

    return html

def one_to_gruop_time(name):
    """生成ModelList中某一项的某一个时间值的HTML

    Args:
        name: 字段名

    Returns:
        HTML代码字符串
    """

    def html(value):
        """
        Args:
            value: 字段值
        """

        if not value:
            showtime = ''
        else:
            tmptime = datetime.datetime.fromtimestamp(int(value))
            showtime = tmptime.strftime('%Y-%m-%d %H:%M:%S')

        return (u'<td style="text-align:center">'
                u'<input style="width:160px" type="text" name="%s" value="%s" />'
                u'</td>') % (name, showtime)

    return html

def one_to_gruop_time_no(name):
    """生成ModelList中某一项的某一个时间值的HTML

    展示数据，无法修改

    Args:
        name: 字段名

    Returns:
        HTML代码字符串
    """

    def html(value):
        """
        Args:
            value: 字段值
        """

        if not value:
            showtime = ''
        else:
            tmptime = datetime.datetime.fromtimestamp(int(value))
            showtime = tmptime.strftime('%Y-%m-%d %H:%M:%S')

        return u'<td>%s</td>' % showtime

    return html

def togroup(funcs, sort):
    """接收ModelList莫一项表单数据

    Args:
        funcs: 字段展示及接受处理方法字典
        sort: 字段名排序集合

    Returns:
        字典数据
    """

    def decorator(req):
        data = {}
        for val in sort:
            func = funcs[val][1]
            if func:
                value = funcs[val][1](req, val)
                data[val] = value

        return data

    return decorator

def getwhere(pk, info_config):
    """获得PK对象的来源信息

    Args:
        pk: 对象主键
        info_config: 说明信息配置

    Returns:
        info: 来源说明文字
    """

    import re

    robj = re.search('_\d_\d+$', pk)

    if not robj:
        return u'未知'

    tm_val = robj.group()[1:].split('_')

    type = int(tm_val[0])
    if type == 1:  #来源于关卡
        return u'关卡%s获得' % tm_val[1]

    else:
        detail = info_config.get('from', {}).get('detail', {})
        return detail[type] if detail else type
