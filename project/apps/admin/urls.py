# coding: utf-8

URL_MAPPING = {
    '/admin/': 'views.main_view',
    '/admin/left/': 'views.left_view',
    '/admin/index/': 'views.index_view',
    '/admin/login/': 'views.login',
    '/admin/config/': 'config_admin.index',
    '/admin/config/upload/': 'config_admin.upload',
    '/admin/config/reload/': 'config_admin.reloadall',

    '/admin/user/': 'user_admin.index',
    '/admin/user/reset/': 'user_admin.reset',

    '/admin/game/': 'game_admin.index',
    '/admin/game/show/': 'game_admin.show',
    '/admin/game/save/': 'game_admin.save',
    '/admin/game/reset/': 'game_admin.reset',

    '/admin/hero/': 'hero_admin.index',
    '/admin/hero/show/': 'hero_admin.show',
    '/admin/hero/save/': 'hero_admin.save',
    '/admin/hero/add/': 'hero_admin.add',
    '/admin/hero/modify/': 'hero_admin.modify',
    '/admin/hero/delete/': 'hero_admin.delete',
    '/admin/hero/reset/': 'hero_admin.reset',
}
