# coding: utf-8

class BaseHelper(object):
    def finish(self):
        raise NotImplementedError

    def frame(self):
        raise NotImplementedError

    def rel(self):
        pass

    def on_finish(self):
        return True
