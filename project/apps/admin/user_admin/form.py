# coding: utf-8

import modeldict
import modellist


class ModelDictForm(object):
    """
    """
    type = 'dict'

    def __init__(self, config):
        """
        """
        self.type = 'dict'
        self.config = config
        self.field = config['field']
        self.values = config['values']
        self.sort = config['sort']

        self.show = modeldict.to_tableform(self.config)

    def formdata(self, req, data):
        """整理ModelDict数据
        """
        changes = {}

        for name, (_, _, val_func) in self.values.iteritems():

            if val_func:
                value = val_func(req, name)

                if value != data[name]:
                    changes[name] = value

        return changes


    def processdata(self, req, field_obj):
        """
        """
        submit = req.get_argument('submit', '')

        if submit == 'reset':
            return self.resetdata(field_obj)

        if submit == 'modify':
            return self.modifydata(req, field_obj)

    def modifydata(self, req, field_obj):
        """
        """
        changes = self.formdata(req, field_obj)

        for name, value in changes.iteritems():
            field_obj[name] = value

        return bool(changes)

    def resetdata(self, field_obj):
        """
        """
        field_obj.reset()

        return True


class ModelListForm(object):
    """
    """
    type = 'list'

    def __init__(self, config):
        """
        """
        self.config = config
        self.field = config['field']
        self.values = config['values']
        self.sort = config['sort']

        self.show = modellist.to_tableform(self.config)

    def formdata(self, req, data):
        """整理ModelList数据
        """

        changes = {}

        for name, (_, _, val_func) in self.values.iteritems():
            if val_func:
                value = val_func(req, name)
                if value != data[name]:
                    changes[name] = value

        return changes

    def processdata(self, req, field_obj):
        """
        """
        submit = req.get_argument('submit', '')

        if submit == 'reset':
            return self.resetdata(field_obj)

        if submit == 'modify':
            return self.modifydata(req, field_obj)

    def adddata(self, req, field_obj):
        """
        """
        pass
    
    def deletedata(self, req, field_obj):
        """
        """
        pass

    def modifydata(self, req, field_obj):
        """
        """
        changes = self.formdata(req, field_obj)

        for name, value in changes.iteritems():
            field_obj[name] = value

        return bool(changes)

    def resetdata(self, field_obj):
        """
        """
        field_obj.reset()

        return True
