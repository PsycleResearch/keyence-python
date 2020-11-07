import logging
import sys
import time
import threading

import cpppo
logging.basicConfig(**cpppo.log_cfg)

from cpppo.server.enip import poll
from cpppo.server.enip.ab import powerflex_750_series as device

# Device IP in 1st arg, or 'localhost' (run: python -m cpppo.server.enip.poll_test)
hostname = sys.argv[1] if len(sys.argv) > 1 else 'localhost'

params = [
    ('@1/0x1/0x7','SSTRING'), # Device name, should read: NU-EP1
    ('@0x66/0x1/0x0325', 'UINT') # Current value of sensor, should read: distance between fibers
]

def failure(exc):
    failure.string.append(str(exc))

failure.string = []

def process(par, val):
    process.values[par] = val

process.done = False
process.values = {}

poller = threading.Thread(
    target=poll.poll, kwargs={
        'proxy_class':  device,
        'address':      (hostname, 44818),
        'cycle':        0.001,
        'timeout':      0.5,
        'process':      process,
        'failure':      failure,
        'params':       params,
    })

poller.start()

# Monitor the process.values {} and failure.string [] (updated in another Thread)
try:
    while True:
        while process.values:
            par,val = process.values.popitem()
            print("%s: %16s == %r" % (time.ctime(), par, val))
        while failure.string:
            exc = failure.string.pop( 0 )
            print("%s: %s" %(time.ctime(), exc))

        # time.sleep(0.1)
finally:
    process.done = True
    poller.join()
