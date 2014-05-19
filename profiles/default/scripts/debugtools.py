from uo.oeuo import UO, AS
from uo.serpent.script import ScriptBase
from uo.serpent.props import *
from uo.tools.items import get_by_id
from uo.tools.extensions import request_target
from uo.tools.items import *
from uo import manager
import wx

class DebugToolsScript(ScriptBase):
    script_name = "Debug tools"

    def t1(self):
        UO.SysMessage('PRESSED')

    def t2(self):
        UO.SysMessage('RELEASED')

    def main(self):
        while True:
            UO.SysMessage(str(manager))
            manager.sleep(1)

    def load(self):
        b = KeyBind(self.t1, self.t2)
        b.set_keys('p')
        b.bind(manager)

    @method_bind('freeze character')
    def freeze_char(self):
        if not 'A' not in UO.CharStatus:
            UO.CharStatus += 'A'

    @method_bind('unfreeze character')
    def unfreeze_char(self):
        UO.CharStatus = UO.CharStatus.replace('A', '')

    @method_bind('test_fail')
    def test_fail(self):
        for i in xrange(10):
            use_item(111111)
            AS.Drag(11111)


    @method_bind('Get item info')
    def get_item_info(self):
        target = request_target()
        item = get_by_id(target.id_)
        if item is None:
            print "no item found"
        else:
            print item.full_string()

