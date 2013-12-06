# coding: utf-8
from tornado.httpserver import HTTPServer
from tornado import ioloop
from tornado import web
from tornado.options import define, options
from lib.core.environ import ShellEnviron
from handers import APIRequestHandler
from handers import AdminRequestHandler
from handers import ChatRequestHandler
from handers import ENVIRONS
from handers import preloader
from handers import TEMPLATE_PATH, STATIC_PATH

import os
import gc
import time
import psutil
import signal
import logging


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
        settings = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            debug=debug,
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    for env_id, (doc_root, short_id) in ENVIRONS.iteritems():
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

