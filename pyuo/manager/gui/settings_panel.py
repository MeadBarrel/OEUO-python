import wx
import wx.lib.scrolledpanel as scrolled
from ..key_manager import CombinationListener
from ..props import Setting, KeyBind, BindError
import gevent


class PickKeysButton(wx.Button):
    """Button widget, requesting a key combination when pressed. Binds to TextCtrl to show the combination pressed"""

    def __init__(self, textctrl, *args, **kwargs):
        self.textctrl = textctrl
        super(PickKeysButton, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_BUTTON, self.on_pressed)

    def on_pressed(self, event):
        event.Skip()
        old_bg = self.textctrl.GetBackgroundColour()
        self.Refresh()
        gevent.sleep(.2)
        cl = CombinationListener()
        combination = None
        while not combination:
            combination = cl.check_pressed()
            gevent.sleep(0)
        while combination:
            string = '+'.join(combination)
            self.textctrl.Value = string
            gevent.sleep(0)
            combination = cl.check_pressed()
        self.Refresh()


class ObjectBindsPanel(scrolled.ScrolledPanel):
    """SettingsManager key binds panel"""

    def __init__(self, parent, manager, obj, *args, **kwargs):
        """
        :rtype manager _Manager
        :rtype obj SettingsManager
        """
        super(ObjectBindsPanel, self).__init__(parent, *args, **kwargs)
        self.obj = obj
        self.binds = []
        self.manager = manager
        self.sizer = wx.FlexGridSizer(cols=6)
        self.sizer.AddGrowableCol(1)
        self.SetSizer(self.sizer)
        self.collect()
        self.populate()
        self.SetupScrolling(False, True)

    def collect(self):
        """Collect key binds from settings manager"""
        self.binds = list(self.obj.fetch_binds())

    def set_bind(self, event, bind, keys, text_box):
        """Try to set a key bind. Show error dialog on bad formed combination, or yes/no warning if there's already
        a bind for that combination"""
        event.Skip()
        try:
            keys = self.manager.key_manager.uniform(keys)
        except BindError:
            dlg = wx.MessageDialog(self, 'Malformed keys', 'oops', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.update_keys()
            return
        old_bind = self.manager.key_manager.get_bind(keys)
        if old_bind:
            dlg = wx.MessageDialog(self, '[%s] already bound to %s: do you want to replace it?' % (keys, old_bind.name),
                                   'hey...', wx.YES_NO | wx.ICON_WARNING)
            result = dlg.ShowModal()
            accept = result == wx.ID_YES
            if accept:
                self.manager.key_manager.unbind(old_bind)
            else:
                self.update_keys()
                return
        bind.set_keys(keys)
        bind.bind(self.manager)
        self.update_keys()

    def clear_bind(self, event, bind, text_box):
        event.Skip()
        dlg = wx.MessageDialog(self, 'Are you sure you want to remove this bind?', 'hm?', wx.YES_NO | wx.ICON_WARNING)
        accept = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        if not accept:
            return
        text_box.Value = ''
        text_box.SetBackgroundColour(wx.WHITE)
        try:
            bind.clear_keys()
            bind.unbind(self.manager)
        except BindError:
            dlg = wx.MessageBox(self, 'Cannot unbind: bind does not exist', 'ouch', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        self.update_keys()

    def update_keys(self):
        for tb in self.tboxes:
            self.update_tb(*tb)
        self.Refresh()

    def update_tb(self, text_box, bind):
        keys = self.manager.key_manager.get_keys(bind)
        if keys:
            text_box.Value = keys
            text_box.SetBackgroundColour(wx.GREEN)
        else:
            text_box.Value = ''
            text_box.SetBackgroundColour(wx.WHITE)

    def populate(self):
        self.tboxes = []
        for bind in self.binds:
            #box = wx.BoxSizer(wx.HORIZONTAL)
            existing = self.manager.key_manager.get_keys(bind)
            if existing:
                text_box = wx.TextCtrl(self, wx.ID_ANY, value=existing)
                text_box.SetBackgroundColour(wx.GREEN)
            else:
                text_box = wx.TextCtrl(self,wx.ID_ANY, value='')
            self.tboxes.append((text_box, bind))
            static = wx.StaticText(self, label=bind.name)
            button_set = wx.Button(self, label='Set')
            button_pick = PickKeysButton(text_box, self, label='pick')
            button_clear = wx.Button(self, label='Clear')
            button_set.Bind(wx.EVT_BUTTON, lambda event, bind=bind, text_box=text_box: self.set_bind(event, bind, text_box.Value, text_box))
            button_clear.Bind(wx.EVT_BUTTON, lambda event, bind=bind, text_box=text_box: self.clear_bind(event, bind, text_box))
            button_set.SetMaxSize((40, button_set.GetMaxHeight()))
            button_pick.SetMaxSize((40, button_pick.GetMaxHeight()))
            button_clear.SetMaxSize((40, button_clear.GetMaxHeight()))
            self.sizer.Add(static)
            self.sizer.Add(text_box, 10, wx.EXPAND)
            self.sizer.Add(button_set, 1, wx.ALIGN_RIGHT)
            self.sizer.Add(button_pick, 1, wx.ALIGN_RIGHT)
            self.sizer.Add(button_clear, 1, wx.ALIGN_RIGHT)
            self.sizer.Add((10, 0), 1)


class ObjectSettingsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, obj, *args, **kwargs):
        super(ObjectSettingsPanel, self).__init__(parent, *args, **kwargs)
        self.obj = obj
        self.groups = {}
        self.notebook = wx.Notebook(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.collect()
        self.populate()
        self.SetupScrolling(True, True)

    def update_page_values(self):
        page = self.notebook.CurrentPage
        if not page:
            return
        for setting in page.settings.itervalues():
            setting.update_wx()
        self.Refresh()

    def collect(self):
        for name, value in self.obj.fetch_settings():
            if value.group not in self.groups:
                panel = wx.Panel(self.notebook)
                self.groups[value.group] = panel
                panel.sizer = wx.FlexGridSizer(cols=2, vgap=6)
                panel.sizer.AddGrowableCol(1)
                panel.SetSizer(panel.sizer)
                panel.settings = {}
            else:
                panel = self.groups[value.group]
            panel.settings[name] = value

    def populate(self):
        for name, group in self.groups.iteritems():
            self.notebook.AddPage(group, name)
            for setting in sorted(group.settings.itervalues(), key=lambda i: i.priority):
                label = wx.StaticText(group, label=setting.name)
                label.SetMinSize((200, label.MinHeight))
                control = setting.init_wx(group)
                setting.update_wx()
                group.sizer.Add(label, .5, wx.ALIGN_LEFT)
                group.sizer.Add(control, 1, wx.EXPAND)


class ObjectPanel(wx.Panel):
    def __init__(self, parent, script, *args, **kwargs):
        super(ObjectPanel, self).__init__(parent, *args, **kwargs)
        self.manager = parent.manager
        self.script = script
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook = wx.Notebook(self)
        self.settings = ObjectSettingsPanel(self.notebook, self.script)
        self.binds = ObjectBindsPanel(self.notebook, self.manager, self.script)
        self.notebook.AddPage(self.settings, 'Settings')
        self.notebook.AddPage(self.binds, 'Hotkeys')
        self.sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def update_settings(self):
        self.settings.update_page_values()
        self.binds.update_keys()

class ObjectsPanel(wx.Panel):
    def __init__(self, manager, *args, **kwargs):
        self.scripts = {}
        self.panels = {}
        self.current_script = None
        self.current_settings_panel = None
        self.manager = manager
        super(ObjectsPanel, self).__init__(*args, **kwargs)
        self.init()

    def remove_current(self):
        if self.current_settings_panel is not None:
            self.RemoveChild(self.current_settings_panel)
            self.sizer.Remove(self.current_settings_panel)
            self.Layout()

    def update_settings(self, event):
        event.Skip()
        selection = self.scripts_list.GetSelection()
        try:
            panel = self.panels[self.scripts_list.GetString(selection)]
        except:
            panel = None
        if panel == self.current_settings_panel:
            return
        self.sizer.Clear()
        if self.current_settings_panel:
            self.current_settings_panel.Hide()
        self.sizer.Add(self.scripts_list, 1, wx.EXPAND)
        if panel:
            self.sizer.Add(panel, 1, wx.EXPAND)
            panel.update_settings()
            panel.Show()
        self.current_settings_panel = panel
        self.sizer.Layout()

    def update(self):
        self.scripts = self.manager.scripts.scripts
        self.current_script = None
        self.current_settings_panel = None
        self.scripts_list.SetItems(self.scripts.keys())
        for name, script in self.scripts.iteritems():
            if not name in self.panels:
#                result = ScriptSettingsPanel(self, script)
                result = ObjectPanel(self, script)
                result.Hide()
                self.panels[name] = result


    def init(self):
        self.sizer = wx.FlexGridSizer(rows=1, cols=2)
        self.sizer.AddGrowableCol(1)
        self.sizer.AddGrowableRow(0)
        self.scripts_list = wx.ListBox(self, choices=self.scripts.keys())
        self.scripts_list.SetMinSize((150, 200))
        self.scripts_list.Bind(wx.EVT_LISTBOX, self.update_settings)
        self.sizer.Add(self.scripts_list, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
