import time
from uo.oeuo import UO, AS
from .macro import use_item
import gevent



def wait_for_cursor(timeout=None):
    if timeout:
        started = time.time()
    while not UO.TargCurs:
        gevent.sleep(.1)
        if timeout:
            if time.time() - started > timeout:
                return False
    return True

class TargetObject(object):
    def __init__(self, id_, kind, tile, x, y, z):
        self.id_ = id_
        self.kind = kind
        self.tile = tile
        self.x = x
        self.y = y
        self.z = z

def wait_for_target(timeout=None):
    wait_for_cursor()
    if timeout:
        started = time.time()
    while UO.TargCurs:
        gevent.sleep(.1)
        if timeout:
            if time.time() - started > timeout:
                return False
    return TargetObject(UO.LTargetID, UO.LTargetKind, UO.LTargetTile, UO.LTargetX, UO.LTargetY, UO.LTargetZ)

def request_target(timeout=None, target_kind=1):
    """
    :rtype TargetObject
    """
    UO.LTargetKind = target_kind
    UO.TargCurs = True
    return wait_for_target(timeout)


def use_on(id_, target, timeout=None):
    use_item(id_)
    result = wait_for_cursor(timeout)
    if result:
        UO.LTargetID = target
        UO.Macro(23, 0)
        return True
    else:
        return False






