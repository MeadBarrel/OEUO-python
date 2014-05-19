from uo.manager.script import ScriptBase
import gevent
import re


class BindObj(object):
    def __init__(self, regexp, callback):
        self.regexp = re.compile(regexp)
        self.callback = callback

class JournalScannerScript(ScriptBase):
    script_name = "Journal scanner"

    def load(self, manager):
        """
        :type manager manager
        """
        global UO
        UO = manager.UO
        self.binds = set()
        self.old_ref = 0

    def bind(self, regexp, callback):
        bobj = BindObj(regexp, callback)
        self.binds.add(bobj)

    def scan(self):
            newRef, nCont = UO.ScanJournal(self.old_ref)
            for line_i in xrange(nCont):
                line, col = UO.GetJournal(line_i)
                for bind in self.binds:
                    if bind.regexp.match(line):
                        bind.callback(line)
            self.old_ref, nCont = UO.ScanJournal(newRef)

    def main(self):
        self.old_ref, nCont = UO.ScanJournal(self.old_ref)
        while True:
            self.scan()
            gevent.sleep(.1)



