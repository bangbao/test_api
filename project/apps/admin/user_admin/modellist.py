# coding: utf-8


def to_tableform(config):
    """生成ModelList数据表单页面框架

    Args:
        config: 配置

    Returns:
        模板生成函数
    """
    sort, values = config['sort'], config['values']
    config_key, field = config['config_key'], config['field']

    label_html = label_template(sort, values)
    form_html = form_template(sort, values)

    table = (u'<table id="info"><tr><td><static_panel></td></tr>'
             u'<tr><td><add_panel></td></tr></table>'
             u'<table id="data">%s%s</table>') \
             % (label_html, '%s')

    def html(user):
        """
        Args:
            user: 用户对象

        Returns:
            数据表单
        """
        data = eval('user.%s' % field)
        obj_config = user.env.game_config[config_key]

        table_label = (form_html % dict(obj, pk=pk, field=field,
                                        hname=obj_config[obj.get('cfg_id', pk)]['name'])
                       for pk, obj in data.iteritems())

        context = u''.join(table_label)

        return table % context

    return html


def label_template(sort, values):
    """
    """
    label_tmp = [u'<tr><th>PK</th><th>名称</th>']

    for name in sort:
        one_label = u'<th>%s</th>' % values[name][0]
        label_tmp.append(one_label)

    label_tmp.append(u'<th colspan="2">操作</th></tr>')

    return u''.join(label_tmp)


def form_template(sort, values):
    """
    """
    form_tmp = [(u'<tr><form action="/admin/user/modify/" method="post">'
                 u'<input type="hidden" name="uid" value="%(uid)s"/>'
                 u'<input type="hidden" name="field" value="%(field)s" />'
                 u'<td>%(pk)s<input type="hidden" name="pk" value="%(pk)s"/></td>'
                 u'<td>%(hname)s</td>')]

    for val_key in sort:
        show_func = values[val_key][1]
        one_html = show_func(val_key)

        form_tmp.append(one_html)

    form_tmp.append((u'<td><button type="submit" name="submit" value="modify" '
                     u'onClick="return confirm(\'确定修改吗？\')">修改</button></td>'
                     u'<td><button type="submit" name="submit" value="delete" '
                     u'onClick="return confirm(\'确定删除吗？\')">删除</button></td>'
                     u'</form></tr>'))

    return u''.join(form_tmp)


def one_to_group(name):
    """生成ModelList中某一项的某一个值的HTML

    Args:
        name: 字段名

    Returns:
        HTML代码字符串
    """
    value_format = '%(value)s'.replace('value', name)

    return (u'<td><input class="inp" type="text" name="%s" value="%s" />'
            u'</td>') % (name, value_format)


def one_to_group_no(name):
    """生成ModelList中某一项的某一个值的HTML

    展示数据，无法修改

    Args:
        name: 字段名

    Returns:
        HTML代码字符串
    """
    value_format = '%(value)s'.replace('value', name)

    if name == 'cfg_id':
        return u'<td>%s<input type="hidden" name="%s" value="%s"/></td>' \
                % (value_format, name, value_format)
    else:
        return u'<td>%s</td>' % value_format


