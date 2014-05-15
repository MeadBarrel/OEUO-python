"""PyOEUO script manager"""
from wx import Timer, EVT_TIMER
from pyuo import app_folder
from pyuo.manager.gui.gui import WelcomeFrame

__author__ = 'Lai Tash'
__email__ = 'lai.tash@gmail.com'
__license__ = "GPL"

from ..oeuo import UO, AS
from threading import Thread
from .props import KeyBind
from .key_manager import KeyBinder, CombinationListener
from .script import ScriptBase, SettingsManager, SettingsManagerError
import os
import wx
import gevent
import traceback
from .gui.gui import GUIFrame
from .props import *
import time
import win32gui

class App(wx.App):
    def MainLoop(self):
        self.keepGoing = True
        evtloop = wx.EventLoop()
        old = wx.EventLoop.GetActive()
        wx.EventLoop.SetActive(evtloop)
        while self.keepGoing:
            gevent.sleep(.1)
            while evtloop.Pending():
                evtloop.Dispatch()
            self.ProcessIdle()
        wx.EventLoop.SetActive(old)

app = App()

class ScriptsManagerError(Exception):
    pass


class ManagerSettings(SettingsManager):
    def __init__(self, manager, key_manager):
        super(ManagerSettings, self).__init__(key_manager)
        self.manager = manager

    cpu_usage_limit_delay = FloatSetting('Limit cpu usage delay', default=.001)
    main_loop_delay = FloatSetting('Main loop delay', default=0)
    client_window_flag = StringSetting('Client window title flag', default='Ultima Online')
    no_input_outside_client = BoolSetting('No input outside client', default=True)

class ScriptsManager(object):
    def __init__(self, manager):
        """
        :type manager _Manager
        """
        self.manager = manager
        self.scripts = {}
        self.tasks = {}

    def load_profile(self, profile):
        self.stop_all()
        self.free_all()
        self.load_scripts(profile)
        self.load_scripts_settings(profile)

    def get_scripts_path(self, profile):
        return os.path.join(self.manager.get_profile_path(profile), 'scripts')

    def load_scripts(self, profile):
        self.manager.log_info('Loading Scripts')
        self.scripts = {}
        #fetch script files
        scripts_path = self.get_scripts_path(profile)
        if not os.path.exists(scripts_path):
            return
        for script_file in (f for f in os.listdir(scripts_path) if os.path.splitext(f)[1]=='.py'):
            abs_path = os.path.join(scripts_path, script_file)
            if not os.path.isfile(abs_path):
                continue
            environment = {'Manager': self.manager, 'Scripts': self}
            try:
                execfile(abs_path, environment)
            except:
                self.manager.log_error(traceback.format_exc())
                continue
            for name, attr in environment.items():
                if isinstance(attr, type) and issubclass(attr, ScriptBase) and attr.__name__.find('Script') == len(attr.__name__) - 6:
                    script_obj = attr
                    script_obj._file_name = script_file
                    self.add_script_obj(script_obj)

    def add_script_obj(self, script_obj):
        if script_obj.name in self.scripts:
            self.manager.log_error("Script %s is already loaded" % script_obj.name)
        instance = script_obj(self.manager)
        self.scripts[script_obj.name()] = instance
        self.manager.log_info('%s loaded' % script_obj.name())

    def save_scripts(self, profile):
        folder = self.manager.get_xml_path(profile)
        if not os.path.exists(folder):
            os.makedirs(folder)
        if os.path.isfile(folder):
            raise ScriptsManagerError('Cannot save into %s: not a folder' % folder)
        for name, script_obj in self.scripts.iteritems():
            xml_name = '%s.xml' % os.path.splitext(script_obj._file_name)[0]
            xml_path = os.path.join(folder, xml_name)
            self.manager.log_info('Saving %s' % xml_path)
            try:
                script_obj.save_xml(xml_path)
            except:
                self.manager.log_warning("Could not save %s, traceback:\n%s" % traceback.format_exc())

    def load_scripts_settings(self, profile):
        folder = self.manager.get_xml_path(profile)
        if not os.path.exists(folder):
            return
        if os.path.isfile(folder):
            raise ScriptsManagerError('%s is not a folder' % folder)
        for name, script_obj in self.scripts.iteritems():
            xml_name = '%s.xml' % os.path.splitext(script_obj._file_name)[0]
            xml_path = os.path.join(folder, xml_name)
            self.manager.log_info("Loading %s" % xml_path)
            try:
                script_obj.load_xml(xml_path)
            except:
                self.manager.log_warning('Could not load settings for %s, traceback:\n%s' % (name, traceback.format_exc()))

    def start_script(self, script_name):
        if not script_name in self.scripts:
            raise ScriptsManagerError('%s not in scripts' % script_name)
        if script_name in self.tasks:
            raise ScriptsManagerError('%s is already running' % script_name)
        self.manager.log_info('Starting %s' % script_name)
        self.tasks[script_name] = gevent.spawn(self.scripts[script_name].main)

    def stop_script(self, script_name):
        if not script_name in self.scripts:
            raise ScriptsManagerError('%s not in scripts' % script_name)
        if not script_name in self.tasks:
            raise ScriptsManagerError('%s is not running' % script_name)
        self.manager.log_info('Stopping %s' % script_name)
        self.tasks[script_name].kill()
        del self.tasks[script_name]

    def stop_all(self):
        for script_name in self.scripts:
            self.stop_script(script_name)

    def start_all(self):
        self.manager.log_info('Starting scripts')
        for script_name in self.scripts:
            self.start_script(script_name)

    def free_all(self):
        for script_obj in self.scripts.values():
            script_obj.free()


class ManagerGUI(object):
    def __init__(self, manager):
        self.app = app
        self.manager = manager

    def main_loop(self):
        self.manager.log_info('starting main loop')
        self.gui = GUIFrame(self.manager)
        self.gui.load_all()
        self.gui.Show()

    def hide(self):
        self.gui.Hide()
        self.gui.Destroy()
        #if self.app.keepGoing:
        #    self.app.keepGoing = False

    def close(self):
        if self.app.keepGoing:
            self.app.keepGoing = False

    def update(self):
        pass
        #self.gui.update()

class _Manager(object):
    def __init__(self, welcome, folder):
        self.UO = UO
        self.AS = AS
        self.welcome = welcome
        self.gui = ManagerGUI(self)
        self.key_manager = KeyBinder(self)
        self.scripts = ScriptsManager(self)
        self.folder = folder
        self.main_loop_task = None
        self.keep_going = False
        self.exec_result = -1

    def client_has_focus(self):
        wt = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return self.settings.client_window_flag in wt

    def load_profile(self, profile):
        try:
            self.profile = profile
            self.load_settings(profile)
            self.scripts.load_profile(profile)
            self.gui.update()
        except:
            self.log_error(traceback.format_exc())

    def save_profile(self, profile):
        try:
            self.save_settings(profile)
            self.scripts.save_scripts(profile)
        except:
            self.log_error(traceback.format_exc())

    def switch_profile(self, profile):
        self.stop()
        self.load_profile(profile)

    def return_to_main(self):
        self.stop()
        self.gui.hide()
        self.welcome.gui.Show()

    def quit(self):
        self.stop()
        self.gui.close()
        self.exec_result = 1

    def stop(self):
        try:
            self.save_profile(self.profile)
            self.scripts.stop_all()
            self.scripts.free_all()
            self.keep_going = False
        except:
            self.log_error(traceback.format_exc())

    def start(self):
        try:
            self.scripts.start_all()
            self.gui.main_loop()
            self.main_loop_task = gevent.spawn(self.main_loop)
        except:
            self.log_error(traceback.format_exc())

    def load_settings(self, profile):
        self.settings = ManagerSettings(self, self.key_manager)
        xml_path = os.path.join(self.get_xml_path(profile), 'settings.xml')
        if not os.path.exists(xml_path):
            return
        self.log_info('Loading global settings')
        try:
            self.settings.load_xml(self.get_settings_xml(profile))
        except:
            self.log_error('Could not load settings, exception:\n %s' % traceback.format_exc())

    def save_settings(self, profile):
        folder = self.get_profile_path(profile)
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                self.log_error('Could not save global settings: unable to create folder')
                return
        xml_path = os.path.join(folder, 'settings.xml')
        self.log_info('Saving global settings')
        try:
            self.settings.save_xml(self.get_settings_xml(profile))
        except:
            self.log_error('Could not save global settings, exception:\n %s' % traceback.format_exc())

    def log_error(self, message):
        print 'ERROR:\n%s\n\n' % message

    def log_warning(self, message):
        print 'WARNING: %s\n\n' % message

    def log_info(self, message):
        print 'INFO: %s\n\n' % message

    def get_profile_path(self, profile):
        return os.path.join(self.folder, 'profiles', profile)

    def get_xml_path(self, profile):
        return os.path.join(self.get_profile_path(profile), 'saved')

    def get_settings_xml(self, profile):
        return os.path.join(self.get_xml_path(profile), 'global.xml')

    def main_loop(self):
        self.log_info('Starting main loop')
        self.keep_going = True
        listener = CombinationListener()
        while self.keep_going:
            self.client_has_focus()
            gevent.sleep(self.settings.main_loop_delay)
            if self.settings.cpu_usage_limit_delay:
                time.sleep(self.settings.cpu_usage_limit_delay)
            try:
                if not UO.CliCnt:
                    self.quit()
                elif not UO.CharName:
                    self.return_to_main()
                if self.client_has_focus() or not self.settings.no_input_outside_client:
                    self.key_manager.execute()
            except:
                self.log_error(traceback.format_exc())


class WelcomeScreen(object):
    def __init__(self):
        self.profiles = filter(lambda f: not os.path.isfile(f), os.listdir(os.path.join(app_folder, 'profiles')))
        self.app = app
        self.gui = WelcomeFrame(self)
        self.timer = Timer(self.gui, 1)
        self.timer.Start(30)
        EVT_TIMER(self.gui, 1, self.update_state)

    @property
    def client_state(self):
        return bool(UO.CliCnt)

    def update_state(self, event):
        self.gui.update_run_button()

    def main(self):
        self.gui.Show()
        gevent.spawn(self.app.MainLoop())

    def on_close(self):
        self.app.keepGoing = False

    def run(self, profile):
        self.gui.Hide()
        manager = _Manager(self, app_folder)
        UO.set_client(1)
        manager.load_profile(profile)
        manager.start()
