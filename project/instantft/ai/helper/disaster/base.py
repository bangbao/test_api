# coding: utf-8

class BaseDisaster(object):
    HURT_FIELD_NAME = 'hurt'

    def frame_update(self, data, hurts):
        """
        """

        for target, hurt in hurts.iteritems():
            obj, filed = {}, []
            obj = data[target].setdefault(self.HURT_FIELD_NAME, obj)
            field = obj.setdefault(self.skill.skill_effect, filed)
            filed.extend(hurt)


    def on_finish(self):
        """
        """
        pass
