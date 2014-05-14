from pyuo.oeuo import UO, AS
from pyuo.manager.script import ScriptBase
from pyuo.manager.props import *
from pyuo.tools.items import get_by_id
from pyuo.tools.extensions import request_target
import wx

class DebugToolsScript(ScriptBase):
    @method_bind('Get item info')
    def get_item_info(self):
        target = request_target()
        item = get_by_id(target.id_)
        if item is None:
            print "no item found"
        else:
            print item.full_string()

