from pyuo.oeuo import UO, AS
from pyuo.manager.script import ScriptBase
from pyuo.manager.props import *
from pyuo.tools.items import get_by_id
from pyuo.tools.extensions import request_target
from pyuo.tools.items import *
import wx

class DebugToolsScript(ScriptBase):
    script_name = "Debug tools"

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

