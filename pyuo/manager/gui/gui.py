from .settings_panel import ObjectsPanel, ObjectBindsPanel, ObjectSettingsPanel
import wx


class WelcomeFrame(wx.Frame):
    def __init__(self, welcome_app):
        self.welcome_app = welcome_app
        self.client_state = False
        self.profiles = welcome_app.profiles
        super(WelcomeFrame, self).__init__(None, title='Sea Serpent', size=(600,400), style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
        self.panel = wx.Panel(self, size=(600,400))
        #self.box = wx.FlexGridSizer(cols=1, rows=3)
        #self.box.AddGrowableRow(1)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.profiles_label = wx.StaticText(self.panel, label='Select profile')
        self.profiles_list = wx.ListBox(self.panel, choices = self.profiles)
        self.run_button = wx.Button(self.panel, label='Run')
        self.run_button.Disable()
        self.box.Add(self.profiles_label, 1, wx.ALIGN_LEFT)
        self.box.Add(self.profiles_list, 100, wx.EXPAND|wx.ALL)
        self.box.Add(self.run_button, 1, wx.EXPAND)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_pressed)
        self.profiles_list.Bind(wx.EVT_LISTBOX, self.on_select_profile)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.panel.SetSizer(self.box)

    def set_client_state(self, state):
        self.client_state = state
        self.update_run_button()

    @property
    def profile_selected(self):
        selection = self.profiles_list.GetSelection()
        if selection == wx.NOT_FOUND:
            return None
        else:
            return self.profiles[selection]

    def update_run_button(self):
        if self.welcome_app.client_state:
            if self.profile_selected is not None:
                self.run_button.SetLabel('Launch')
                self.run_button.Enable()
            else:
                self.run_button.SetLabel('Select profile')
                self.run_button.Disable()
        else:
            self.run_button.SetLabel('Waiting for the client to start')
            self.run_button.Disable()
        self.Refresh()

    def on_close(self, event):
        event.Skip()
        self.welcome_app.on_close()

    def on_run_pressed(self, event):
        event.Skip()
        if self.profile_selected is not None:
            self.welcome_app.run(self.profile_selected)

    def on_select_profile(self, event):
        event.Skip()
        self.update_run_button()


class GUIFrame(wx.Frame):
    def __init__(self, manager):
        self.manager = manager
        super(GUIFrame, self).__init__(None, title='Sea Serpent', size=(720,260), style=wx.STAY_ON_TOP|wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
        self.main_panel = wx.Panel(self, size=(720, 260))
        self.box = wx.BoxSizer()
        self.main_panel.SetSizer(self.box)
        self.notebook_create()
        self.box.Fit(self.main_panel)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def notebook_create(self):
        self.notebook = wx.Notebook(self.main_panel)
        self.box.Add(self.notebook, 1, wx.EXPAND|wx.ALL)
        self.objects_panel = ObjectsPanel(self.manager, self.notebook, -1)
        self.global_settings = ObjectSettingsPanel(self.notebook, self.manager.settings)
        self.global_hotkeys = ObjectBindsPanel(self.notebook, self.manager, self.manager.settings)
        self.notebook.AddPage(self.global_settings, 'Settings')
        self.notebook.AddPage(self.global_hotkeys, 'Hotkeys')
        self.notebook.AddPage(self.objects_panel, 'Scripts')

    def load_all(self):
        self.objects_panel.update()

    def on_close(self, event=None):
        self.manager.return_to_main()
        event.Skip()