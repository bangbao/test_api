# coding: utf-8

import os
import gc
import time
import psutil
import signal
import logging

from tornado.httpserver import HTTPServer
from tornado.options import define, options
from tornado import ioloop
from tornado import web
from lib.core.environ import ShellEnviron
from apps import settings
from apps.handers import (APIRequestHandler, 
                          AdminRequestHandler, 
                          ChatRequestHandler, 
                          preloader)


define("port", default=58500, help="run on the given port", type=int)
define("debug", default=True, help="run at debug mode", type=bool)
define("maxmem", default=0, help="max memory use, overflow kill by self. (0 unlimit)", type=int)


class Application(web.Application):
    def __init__(self, debug=False):
        handlers = [
            (r"/api/", APIRequestHandler),
            (r"/chat/", ChatRequestHandler),
            (r"/admin.*", AdminRequestHandler),
        ]
        super(Application, self).__init__(handlers, **settings.TORNADO_SETTINGS)


def main():
    for env_id, (doc_root, short_id) in settings.ENVIRONS.iteritems():
        env = ShellEnviron.build_env(env_id, doc_root)
        env.set_short_id(short_id)
        preloader(env)

    #options.parse_command_line()
    #sokets = tornado.netutil.bind_sockets(options.port)
    #tornado.process.fork_processes(0)
    #app = Application(options.debug)
    #server = HTTPServer(app)
    ##server.listen(options.port)
    #server.add_sockets(sokets)
    #process = psutil.Process(os.getpid())

    options.parse_command_line()
    app = Application(options.debug)
    server = HTTPServer(app)
    server.listen(options.port)
    process = psutil.Process(os.getpid())

    def shutdown():
        io_loop = ioloop.IOLoop.instance()
        server.stop()

        def stop_loop():
            timestamp = int(time.time()) + 1
            
            if (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(timestamp, stop_loop)
            else:
                io_loop.stop()

        stop_loop()

    def sig_handler(sig, frame):
        ioloop.IOLoop.instance().add_callback(shutdown)

    def mem_watcher():
        mem_size = process.get_memory_info().rss
        io_loop = ioloop.IOLoop.instance()
        timestamp = int(time.time()) + 10

        if mem_size > options.maxmem:
            logging.info(repr(gc.get_objects()))
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            io_loop.add_timeout(timestamp, mem_watcher)

    if options.maxmem:
        timestamp = int(time.time()) + 10
        ioloop.IOLoop.instance().add_timeout(timestamp, mem_watcher)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


