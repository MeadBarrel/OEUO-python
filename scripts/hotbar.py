from pyuo.oeuo import UO
from pyuo.manager import Manager
from pyuo.manager.script import ScriptBase
import wx

COLUMNS = 12


class HotBarItem(wx.Button):
    def __init__(self):
        super(HotBarItem, self).__init__()


class HotBar(wx.Frame):
    def __init__(self):
        super(HotBar, self).__init__(None)


#class Script(ScriptBase):
#    name = 'hotbars'
#
#    def __init__(self):
#        self.frames = set()

