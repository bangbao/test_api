# coding: utf-8

import json
import gevent
import logging
import xmlrpclib
import tornado.web
import tornado.websocket

from collections import defaultdict

from lib.core.handlers.htornado import BaseRequestHandler
from lib.core.environ import Environ
from lib.core.environ import APIEnviron
from lib.core.environ import AdminEnviron
from apps import config as config_app
from apps import public as public_app
from apps.settings import ENVIRONS


def preloader(env):
    """
    """
    public_app.register_lua_sha(env)
    config_app.loadall(env)


def restart_server():
    def restart(addr):
        workers = []
        server = xmlrpclib.Server("http://%s:9001/RPC2" % addr)

        for s in server.supervisor.getAllConfigInfo():
            name = "%(group)s:%(name)s" % s
            server.supervisor.stopProcess("%(group)s:%(name)s" % s)
            server.supervisor.startProcess("%(group)s:%(name)s" % s)

            workers.append("%s--%s" % (addr, name))

        return workers

    jobs = []
    jobs.append(gevent.spawn(restart, 'localhost'))

    gevent.joinall(jobs, timeout=3)

    while not all([job.value for job in jobs]):
        gevent.joinall(jobs, timeout=3)

    return [job.value for job in jobs]


class UserMixIn(object):
    """ user嵌入类

    将get_current_user独立出来方便其它Handler共用
    """
    def get_current_user(self, env):
        """ 获取当前用户对象

        首先验证用户，当用户不能通过验证时，
        尝试登陆操作

        Args:
            env: 运行环境

        Returns:
            用户对象
        """
        user_app = env.import_app('user')

        user = user_app.auth(env, self)

        if not user:
            user = user_app.login(env, self)

        return user


class APIRequestHandler(UserMixIn, BaseRequestHandler):
    """ 统一的API Handler

    全部API处理公共接口
    """
    def initialize(self):
        """ 初始化操作

        创建全局环境和运行环境
        """
        env_id = self.request.headers.get(Environ.ENVIRON_PARAMS_NAME, 
                                          Environ.GLOBAL_ENVIRON)

        if not env_id in ENVIRONS:
            raise tornado.web.HTTPError(403)

        env_root, short_id = ENVIRONS[env_id]

        self.request.headers[Environ.ENVIRON_PARAMS_NAME] = env_id
        self.request.headers[Environ.ENVIRON_DOCUMENT_ROOT_NAME] = env_root

        self.env = APIEnviron.build_env(self, short_id)
        self.env.set_config_loader(config_app.AppCacheConfig)

    def api(self):
        """ API统一调用方法
        """
        try:
            self.write(json.dumps({
                                'data': self.env.api(),
                                'status': self.env.errno,
                                'msg': self.env.msg,
                                'headers': {},
                            }, ensure_ascii=False))
        finally:
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.finish()
            # 手动删除apienviron对象
            del self.env

    def _on_finish(self, response):
        """ API统一调用方法
        """
        self.api()
        logging.info('_on_finish %r' % response)

    def on_finish(self):
        """ 处理异步方法
        """
        for callback in self.env.callbacks:
            callback(self.env)
        
        self.env.finish()

    @tornado.web.asynchronous
    def get(self):
        """ 处理GET请求
        """
        self.api()

    @tornado.web.asynchronous
    def post(self):
        """ 处理POST请求
        """
        self.api()
        #http = tornado.httpclient.AsyncHTTPClient()  
        #http.fetch(self.request, self._on_finish) 


class AdminRequestHandler(BaseRequestHandler):
    """ 后台统一 Handler

    全部后台处理公共接口
    """
    def initialize(self, lookup=None):
        """ 初始化操作

        创建全局环境和运行环境
        """
        self._lookup = lookup
        env_id = self.request.headers.get(Environ.ENVIRON_PARAMS_NAME,
                                          Environ.GLOBAL_ENVIRON)

        if not env_id in ENVIRONS:
            raise tornado.web.HTTPError(403)

        env_root, short_id = ENVIRONS[env_id]

        self.request.headers[Environ.ENVIRON_PARAMS_NAME] = env_id
        self.request.headers[Environ.ENVIRON_DOCUMENT_ROOT_NAME] = env_root

        self.env = AdminEnviron.build_env(self, short_id)
        self.env.set_config_loader(config_app.AppCacheConfig)

    def render_to_response(self):
        """ 渲染模板
        """
        template, data = self.env.api()

        self.render(template, **data)

    @tornado.web.addslash
    def get(self):
        """ 处理GET请求
        """
        self.render_to_response()

    @tornado.web.addslash
    def post(self):
        """ 处理POST请求
        """
        self.render_to_response()


class ChatRequestHandler(UserMixIn, tornado.websocket.WebSocketHandler):
    """ 聊天全局处理操作

    合用WebSocket和Redis的异步链接来响应聊天记录

    Attributes:
       SUBSCRIBE_CHANNELS: 已订阅的频道
       app: 聊天应用
    """
    SUBSCRIBE_CHANNELS = defaultdict(int)
    SUBSCRIBE_PROCESS = defaultdict(bool)

    def initialize(self):
        """ 初始化
        
        创建公共环境和运行环境
        """
        env_id = self.request.headers.get(Environ.ENVIRON_PARAMS_NAME,
                                          Environ.GLOBAL_ENVIRON)

        if not env_id in ENVIRONS:
            raise tornado.web.HTTPError(403)

        env_root, short_id = ENVIRONS[env_id]

        self.request.headers[Environ.ENVIRON_PARAMS_NAME] = env_id
        self.request.headers[Environ.ENVIRON_DOCUMENT_ROOT_NAME] = env_root

        self.env = APIEnviron.build_env(self, short_id)
        self.env.set_config_loader(config_app.AppCacheConfig)
        self.app = self.env.import_app('chat')
        self.listen()

    @tornado.gen.engine
    def listen(self):
        """ 监听Redis频道

        通过 SUBSCRIBE_CHANNELS来控制
        监听事件和处理事件
        """
        self.client = self.app.get_connect(self)
        channel = self.app.get_channel(self)

        if not self.SUBSCRIBE_CHANNELS[channel]:
            yield tornado.gen.Task(self.client.subscribe, self.app.get_channel(self))

            if not self.SUBSCRIBE_PROCESS[channel]:
                self.client.listen(self.message_box)
                self.SUBSCRIBE_PROCESS[channel] = True

        self.SUBSCRIBE_CHANNELS[channel] += 1

    def open(self):
        """ 处理WebSocket打开
        """
        logging.info('socket open')

        self.app.open_connect(self)

    def message_box(self, message):
        """ 整理收信箱

        Args:
           message: 消息对象
        """
        if message.kind == 'message':
            self.app.message(message.body)
        elif message.kind == 'disconnect':
            self.close()

    def on_message(self, message):
        """ 处理客户端推送的消息

        Args:
            message: 消息内容
        """
        logging.info('recv msg %s' % repr(message))

        self.app.send_message(self, message)

    def on_close(self):
        """ 处理链接处理
        """
        logging.info('socket close')

        self.app.close_connect(self)


class TextRequestHandler(APIRequestHandler):
    """ 自由定义返回数据格式

    可以自由定义返回数据格式
    """
    def api(self):
        """ API统一调用方法
        """
        try:
            self.write(str(self.env.api()))
        finally:
            self.finish()
            # 手动删除apienviron对象
            del self.env


if __name__ == "__main__":
    print '1'

