from time import clock
import gevent
import traceback

class CallInfo(object):
    def __init__(self):
        self.last_clock = 0
        self.total = 0

    def start(self):
        self.last_clock = clock()

    def pause(self):
        self.total = clock() - self.last_clock

    def end(self):
        self.pause()
        return self.total

class ProfiledFunc(object):
    current_call = None

    def __init__(self, func, manager, class_name='unbound'):
        self.func = func
        self.calls = 0
        self.clock_total = 0
        self.class_name = class_name
        self.manager = manager

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    def execute(self, *args, **kwargs):
        old_call = self.__class__.current_call
        self.__class__.current_call = CallInfo()
        self.__class__.current_call.start()
        self.calls += 1
        args_str = ','.join(map(str, args))
        kw_str = ','.join(['%s=%s' % (name, value) for name, value in kwargs.iteritems()])

        old_sleep = self.manager.sleep
        self.manager.sleep = self.sleep
        self.manager.log_debug('START %s -> %s(%s, %s)' % (self.class_name, self.func.__name__, args_str, kw_str))
        try:
            result = self.func(*args, **kwargs)
        except Exception as e:
            self.manager.log_exception(e)
            raise e
        self.clock_total += self.__class__.current_call.end()
        self.manager.log_debug('EXIT %s -> %s(%s, %s)' % (self.class_name, self.func.__name__, args_str, kw_str))
        self.__class__.current_call = old_call
        self.manager.sleep = old_sleep
        return result

    def sleep(self, n=0):
        cls = self.__class__
        this_call = cls.current_call
        this_call.pause()
        self.manager.log_debug('SLEEP %s -> %s' % (self.class_name, self.func.__name__))
        gevent.sleep(n)
        self.manager.log_debug('RESUME %s -> %s' % (self.class_name, self.func.__name__))
        self.manager.sleep = self.sleep
        this_call.start()
        cls.current_call = this_call

