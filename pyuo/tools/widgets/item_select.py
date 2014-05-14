import wx
import wx.lib.newevent
from pyuo.tools.extensions import request_target
from pyuo.tools.items import Item

ItemSelectEvent, EVT_ITEM_SELECT = wx.lib.newevent.NewEvent()

class ItemSelectButton(wx.Button):
    def __init__(self, parent, *args, **kwargs):
        """
        :type manager manager
        """
        super(ItemSelectButton, self).__init__(parent, *args, **kwargs)
        self.Bind(wx.EVT_BUTTON, self.on_press)

    def on_press(self, event):
        target=request_target()
        print target
        evt = ItemSelectEvent(target=target)
        wx.PostEvent(self, evt)
        event.Skip()




