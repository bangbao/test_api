#!/usr/bin/env python
#
# A simple benchmark of tornado's HTTP stack.
# Requires 'ab' to be installed.
#
# Running without profiling:
# demos/benchmark/benchmark.py
# demos/benchmark/benchmark.py --quiet --num_runs=5|grep "Requests per second"
#
# Running with profiling:
#
# python -m cProfile -o /tmp/prof demos/benchmark/benchmark.py
# python -m pstats /tmp/prof
# % sort time
# % stats 20

from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

import wsgi
import random
import signal
import subprocess

# choose a random port to avoid colliding with TIME_WAIT sockets left over
# from previous runs.
define("min_port", type=int, default=8000)
define("max_port", type=int, default=9000)

# Increasing --n without --keepalive will eventually run into problems
# due to TIME_WAIT sockets
define("n", type=int, default=15000)
define("c", type=int, default=25)
define("keepalive", type=bool, default=False)
define("quiet", type=bool, default=False)

# Repeat the entire benchmark this many times (on different ports)
# This gives JITs time to warm up, etc.  Pypy needs 3-5 runs at
# --n=15000 for its JIT to reach full effectiveness
define("num_runs", type=int, default=1)

define("ioloop", type=str, default=None)

def handle_sigchld(sig, frame):
    IOLoop.instance().add_callback(IOLoop.instance().stop)

def main():
    parse_command_line()
    if options.ioloop:
        IOLoop.configure(options.ioloop)
    for i in xrange(options.num_runs):
        run()

def run():
    params = '?/api/?method=adven.fight&user_token=fc253f0e9cd2&members=21_1366705830_1_ZuRk18_1_15&members=21_1366769345_1_ucwojJ_1_14&members=21_1366773923_1_xuqQtm_1_15&members=21_1366768662_1_Gg1Sfy_1_15&members=21_1366705611_8_nseWwd_3_0&members=21_1367476056_1_4Expsf_1_15&members=21_1367032748_1_cyzxGG_1_22&members=null&area=1&chapter=1&stage=15'

    for env_id, (doc_root, short_id) in wsgi.ENVIRONS.iteritems():
        env = wsgi.ShellEnviron.build_env(env_id, doc_root)
        env.set_short_id(short_id)
        wsgi.preloader(env)

    app = wsgi.Application()
    port = random.randrange(options.min_port, options.max_port)
    app.listen(port, address='127.0.0.1')
    signal.signal(signal.SIGCHLD, handle_sigchld)
    args = ["webbench"]
    args.extend(["-t", str(options.n)])
    args.extend(["-c", str(options.c)])
    args.extend(["-f"])
    

    args.append("http://127.0.0.1:%d/%s" % (port, params))
    subprocess.Popen(args)
    IOLoop.instance().start()
    IOLoop.instance().close()
    del IOLoop._instance
    assert not IOLoop.initialized()

if __name__ == '__main__':
    main()
