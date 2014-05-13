import time
from pyuo.oeuo import UO
from pyuo.manager import Loop
from .macro import use_item
import gevent


def wait_for_target(timeout=None):
    if timeout:
        started = time.time()
    while not UO.TargCurs:
        gevent.sleep(.1)
        if timeout:
            if time.time() - started > timeout:
                return False
    return True

def use_on(id_, target, timeout=None):
    use_item(id_)
    result = wait_for_target(timeout)
    if result:
        UO.LTargetID = target
        UO.Macro(23, 0)
        return True
    else:
        return False






