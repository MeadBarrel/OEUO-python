import time
from pyuo.oeuo import UO
from pyuo.manager import Loop
from .macro import use_item


@Loop()
def wait_for_target(callback, failure=None, timeout=None):
    yield
    print "OK"
    if timeout:
        started = time.time()
    while not UO.TargCurs:
        if timeout:
            if time.time() - started > timeout:
                if failure:
                    failure()
                return
        yield
    callback()

def use_on(id_, target, callback=None, timeout=None, failure=None):
    def _use():
        print "USSSE"
        UO.LTargetID = target
        UO.Macro(23, 0)
        if callback:
            callback()
    use_item(id_)
    wait_for_target(_use, failure, timeout)






