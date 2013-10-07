# coding:utf-8


def announcement(env):
    """ 获取最新公告

    Args:
       env: 运行环境
    """
    announce_app = env.import_app('announce')

    return {
        'announcements': announce_app.recv_announcement(env)
    }
