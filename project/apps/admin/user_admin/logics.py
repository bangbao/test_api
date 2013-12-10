# coding: utf-8

from apps.admin.form import Form
from apps.admin import handle
from . import constants


def get_form(user, field):
    """
    """
    form = constants.CONFIG[field]
    return form.show(user)


def userinfo(user, **kwargs):
    """用户基本信息
    """
    user.load_base()
    user.load_all()

    info = {
        'level': user.game.user['level'],
        'exp': user.game.user['exp'],
        'kcoin': user.game.user['kcoin'],
        'gold': user.game.user['gold'],
        'energy': user.game.user['energy'],
        'rank': user.arena.data['rank'],
        'adven': '%(chapter)s-%(stage)s' % user.adven.adven,
    }

    info.update(kwargs)

    return info


