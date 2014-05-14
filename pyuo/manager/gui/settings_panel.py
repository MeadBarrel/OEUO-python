import wx
import wx.lib.scrolledpanel as scrolled
from ..props import Setting, KeyBind, BindError

class ObjectBindsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, manager, obj, *args, **kwargs):
        super(ObjectBindsPanel, self).__init__(parent, *args, **kwargs)
        self.obj = obj
        self.binds = []
        self.manager = manager
        self.collect()
        self.init()
        self.populate()
        self.SetupScrolling(False, True)


    def init(self):
        self.sizer = wx.FlexGridSizer(cols=5)
        self.sizer.AddGrowableCol(1, 10)
        self.SetSizer(self.sizer)
        #self.box = wx.BoxSizer(wx.VERTICAL)
        #self.sizer = wx.GridSizer(cols=2, hgap=0, vgap=0)
        #self.box.Add(self.sizer)
        #self.SetSizer(self.box)

    def collect(self):
        self.binds = list(self.obj.fetch_binds())

    def update_bind(self, event, bind, keys, text_box):
        event.Skip()
        try:
            keys = self.manager.key_manager.uniform(keys)
        except BindError:
            dlg = wx.MessageDialog(self, 'Malformed keys', 'oops', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.update()
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
                self.update()
                return
        bind.set_keys(keys)
        bind.bind(self.manager)
        self.update()

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
            self.manager.key_manager.unbind(bind)
        except BindError:
            dlg = wx.MessageBox(self, 'Cannot unbind: bind does not exist', 'ouch', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        self.update()

    def update(self):
        for tb in self.tboxes:
            self.update_tb(*tb)
        self.Refresh()

    def update_tb(self, text_box, bind):
        keys = self.manager.key_manager.get_keys(bind)
        print keys
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
            button_clear = wx.Button(self, label='Clear')
            button_set.Bind(wx.EVT_BUTTON, lambda event, bind=bind, text_box=text_box: self.update_bind(event, bind, text_box.Value, text_box))
            button_clear.Bind(wx.EVT_BUTTON, lambda event, bind=bind, text_box=text_box: self.clear_bind(event, bind, text_box))
            button_set.SetMaxSize((40, button_set.GetMaxHeight()))
            button_clear.SetMaxSize((40, button_clear.GetMaxHeight()))
            self.sizer.Add(static)
            self.sizer.Add(text_box, 10, wx.EXPAND)
            self.sizer.Add(button_set, 1, wx.ALIGN_RIGHT)
            self.sizer.Add(button_clear, 1, wx.ALIGN_RIGHT)
            #snd_sizer = wx.BoxSizer(wx.HORIZONTAL)
            #self.sizer.Add(static, .5, wx.ALIGN_LEFT)
            #snd_sizer.Add(text_box, 5, wx.EXPAND)
            #snd_sizer.Add(button_set, 1)
            #snd_sizer.Add(button_clear, 1)
            #self.sizer.Add(snd_sizer, 1, wx.EXPAND)
            self.sizer.Add((10, 0), 1)



class ScriptSettingsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, obj, *args, **kwargs):
        super(ScriptSettingsPanel, self).__init__(parent, *args, **kwargs)
        self.obj = obj
        self.groups = {}
        self.notebook = wx.Notebook(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.collect()
        self.populate()
        self.SetupScrolling(True, True)

    def update(self):
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
                #group.sizer.Add((10, 0), 1, wx.ALIGN_RIGHT)

        #for name, setting in self.settings.iteritems():
        #    label = wx.StaticText(self, label=setting.name)
        #    control = setting.init_wx(self)
        #    setting.update_wx()
        #    self.base_sizer.Add(label, .5, wx.ALIGN_LEFT)
        #    #self.base_sizer.Add(control, 1, wx.ALIGN_RIGHT|wx.EXPAND)
        #    #self.base_sizer.Add(control, 1, wx.EXPAND)
        #    self.base_sizer.Add(control, 1, wx.EXPAND)
        #    self.base_sizer.Add((10, 0), 1, wx.ALIGN_RIGHT)
        ##self.base_sizer.Add((1,1), 100, wx.EXPAND)

    def on_setting_update(self):
        pass

class ScriptPanel(wx.Panel):
    def __init__(self, parent, script, *args, **kwargs):
        super(ScriptPanel, self).__init__(parent, *args, **kwargs)
        self.manager = parent.manager
        self.script = script
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook = wx.Notebook(self)
        self.settings = ScriptSettingsPanel(self.notebook, self.script)
        self.binds = ObjectBindsPanel(self.notebook, self.manager, self.script)
        self.notebook.AddPage(self.settings, 'Settings')
        self.notebook.AddPage(self.binds, 'Hotkeys')
        self.sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def update(self):
        self.settings.update()
        self.binds.update()

class SettingsPanel(wx.Panel):
    def __init__(self, manager, *args, **kwargs):
        self.scripts = {}
        self.panels = {}
        self.current_script = None
        self.current_settings_panel = None
        self.manager = manager
        super(SettingsPanel, self).__init__(*args, **kwargs)
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
            panel.update()
            panel.Show()
        self.current_settings_panel = panel
        self.sizer.Layout()

    def update(self):
        self.scripts = self.manager.scripts_loaded
        self.current_script = None
        self.current_settings_panel = None
        self.scripts_list.SetItems(self.scripts.keys())
        for name, script in self.scripts.iteritems():
            if not name in self.panels:
#                result = ScriptSettingsPanel(self, script)
                result = ScriptPanel(self, script)
                result.Hide()
                self.panels[name] = result


    def init(self):
        #self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer = wx.FlexGridSizer(rows=1, cols=2)
        self.sizer.AddGrowableCol(1)
        self.sizer.AddGrowableRow(0)
        self.scripts_list = wx.ListBox(self, choices=self.scripts.keys())
        self.scripts_list.SetMinSize((150, 200))
        self.scripts_list.Bind(wx.EVT_LISTBOX, self.update_settings)
        self.sizer.Add(self.scripts_list, 1, wx.EXPAND)
        self.SetSizer(self.sizer)