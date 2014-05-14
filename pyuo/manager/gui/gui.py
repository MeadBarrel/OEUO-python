from .settings_panel import SettingsPanel
import wx

class GUIFrame(wx.Frame):
    def __init__(self, manager):
        self.manager = manager
        super(GUIFrame, self).__init__(None, size=(720,260), style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
        #super(GUIFrame, self).__init__(None, size=(720,260))
        self.main_panel = wx.Panel(self, size=(720, 260))
        self.box = wx.BoxSizer()
        self.settings_panel = SettingsPanel(manager, self.main_panel, -1)
        self.box.Add(self.settings_panel, 1, wx.EXPAND|wx.ALL)
        self.main_panel.SetSizer(self.box)
        self.box.Fit(self.main_panel)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event=None):
        self.manager.stop()
        event.Skip()

    def on_resize(self, event=None):
        event.Skip()
        print self.box.GetSizeTuple()
        print self.settings_panel.GetSizeTuple()
        pass
        #self.Layout()
        #self.box.Fit(self.main_panel)


    def update_settings_panel(self):
        self.settings_panel.update()
