from pyuo.oeuo import UO
from pyuo.manager import Manager, Loop
import gevent
import re

class BindObj(object):
    def __init__(self, regexp, callback):
        self.regexp = re.compile(regexp)
        self.callback = callback

class Script(object):
    name = 'journal_event'

    def __init__(self):
        self.binds = set()
        self.old_ref = 0

    def bind(self, regexp, callback):
        bobj = BindObj(regexp, callback)
        self.binds.add(bobj)

    def on_begin(self):
        self.old_ref, nCont = UO.ScanJournal(self.old_ref)
        while True:
            newRef, nCont = UO.ScanJournal(self.old_ref)
            for line_i in xrange(nCont):
                line, col = UO.GetJournal(line_i)
                for bind in self.binds:
                    if bind.regexp.match(line):
                        bind.callback(line)
            newRef, nCont = UO.ScanJournal(newRef)
            self.old_ref = newRef
            gevent.sleep(.2)



