# coding: utf-8

def to_tableform(config):
    """生成ModelList数据表单页面框架

    Args:
        config: 配置

    Returns:
        模板生成函数
    """
    sort, values = config['sort'], config['values']
    field = config['field']

    if not sort:
        sort = values.keys()

    form_html = form_template(sort, values)

    def html(user):
        """
        Args:
            user: 用户对象

        Returns:
            数据表单
        """
        data = eval('user.%s' % field)

        return form_html % dict(data, uid=user.pk, field=field)

    return html

def form_template(sort, values):
    """
    """
    form_tmp = [(u'<form action="/admin/user/modify/" method="post">'
                 u'<input type="hidden" name="uid" value="%(uid)s"/>'
                 u'<input type="hidden" name="field" value="%(field)s" />'
                 u'<table id="mindata">')]

    for val_key in sort:
        label, show_func, _ = values[val_key]
        one_label = show_func(label, val_key)

        form_tmp.append(one_label)

    form_tmp.append((u'</table>'
                    u'<button type="submit" name="submit" value="modify" '
                    u'onClick="return confirm(\'确定保存吗？\')">保存</button>'
                    u'<button type="submit" name="submit" value="reset" '
                    u'onClick="return confirm(\'确定重置吗？\')">重置</button>'
                    u'</form>'))

    return u''.join(form_tmp)

def value_to_form(label, name):
    """生成ModelDict数据中某一值的HTML

    Args:
        label: 当前字段中文名称
        name: 当前字段key

    Returns:
        HTML代码字符串
    """
    value_format = '%(value)s'.replace('value', name)

    return (u'<tr><td>%s</td>'
            u'<td><input type="text" name="%s" value="%s" />'
            u'</td></tr>') % (label, name, value_format)

