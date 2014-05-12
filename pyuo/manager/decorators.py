from time import time

class _Loop(object):
    def __init__(self, method, delay=.1):
        self.method = method
        self.delay = delay
        self.stopped = False
        self.last_run = None

    def execute_once(self):
        try:
            next(self.method)
        except StopIteration:
            self.stopped = True
        self.last_run = time()

    def execute(self):
        if self.last_run is None or self.last_run + self.delay <= time():
            self.execute_once()


def Loop(delay=.1):
    def _creates(method):
#        def _invokes(*args, **kwargs):
        def _invokes(*args, **kwargs):
            meth = method(*args, **kwargs)
            print "INVOKING", method
            result = _Loop(meth, delay)
            Manager.run_loop(result)
        return _invokes
    return _creates


def binds(method):
    method._binds = True
    return method
