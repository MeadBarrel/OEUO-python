"""PyOEUO script manager"""
from contextlib import contextmanager
from wx import Timer, EVT_TIMER
from uo import app_folder
from uo.serpent.gui.gui import WelcomeFrame


__author__ = 'Lai Tash'
__email__ = 'lai.tash@gmail.com'
__license__ = "GPL"

import uo
UO, AS = uo.UO, uo.AS
from .props import KeyBind
from .key_manager import KeyBinder, CombinationListener
from .script import ScriptBase, SettingsManager, SettingsManagerError
import os
import wx
import gevent
from gevent.pool import Group
import traceback
from .gui.gui import GUIFrame
from .props import *
import time
import win32gui

class App(wx.App):
    """A simple wx.App replacement to work as a greenlet"""
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
    errors_to_client = BoolSetting('Notify errors in client', group='Debugging', priority=0)
    do_debug = BoolSetting('Debug (requires restart)', default=True, group='Debugging', priority=1)
    debug_show_messages = BoolSetting("Show debug messages", default=True, group='Debugging', relation=do_debug, priority=2)
    debug_raise_exceptions = BoolSetting("Raise exceptions", default=False, group='Debugging', priority=3)
    debug_log_exceptions = BoolSetting('Log exceptions', default=True, group='Debugging', priority=4)

class ScriptsManager(object):
    def __init__(self, manager):
        """
        :type manager _Manager
        """
        self.manager = manager
        self.scripts = {}
        self.tasks = {}

    def load_profile(self, profile):
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
            with self.manager.try_exception():
                execfile(abs_path, environment)
            if self.manager.last_exception_state:
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
            with self.manager.try_exception():
                script_obj.save_xml(xml_path)

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
            with self.manager.try_exception():
                script_obj.load_xml(xml_path)

    def start_script(self, script_name):
        if not script_name in self.scripts:
            raise ScriptsManagerError('%s not in scripts' % script_name)
        self.manager.log_info('Starting %s' % script_name)
        self.manager.spawn(self.scripts[script_name].main)

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

    def close(self):
        if self.app.keepGoing:
            self.app.keepGoing = False

    def update(self):
        pass
        #self.gui.update()


class _Manager(object):
    def __init__(self, welcome, folder):
        uo.manager = self
        self.UO = uo.UO
        self.AS = uo.AS
        self.AS_task = None
        self.welcome = welcome
        self.gui = ManagerGUI(self)
        self.key_manager = KeyBinder(self)
        self.scripts = ScriptsManager(self)
        self.folder = folder
        self.main_loop_task = None
        self.keep_going = False
        self.exec_result = -1
        self.tasks = Group()
        self.profiled = []
        self.last_exception_state = False

    @contextmanager
    def try_exception(self):
        try:
            yield
            self.last_exception_state = False
        except Exception as e:
            self.last_exception_state = e
            if self.settings.debug_log_exceptions:
                self.log_exception(traceback.format_exc())
            if self.settings.debug_raise_exceptions:
                raise e

    def sleep(self, n):
        """
        replaced in profiler
        """
        gevent.sleep(n)

    def func_wrap(self, func, *args, **kwargs):
        with self.try_exception():
            func(*args, **kwargs)

    def spawn(self, func, *args, **kwargs):
        task = gevent.spawn(self.func_wrap, func, *args, **kwargs)
        self.tasks.add(task)

    def stop_all_tasks(self):
        self.tasks.kill()

    def add_profiled(self, other):
        self.profiled.append(other)

    def show_profiled(self):
        for profiled in self.profiled:
            print profiled.class_name, profiled.func.__name__, profiled.calls, profiled.clock_total

    def client_has_focus(self):
        wt = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return self.settings.client_window_flag in wt

    def load_profile(self, profile):
        with self.try_exception():
            self.profile = profile
            self.load_settings(profile)
            self.scripts.load_profile(profile)
            self.gui.update()

    def save_profile(self, profile):
        with self.try_exception():
            self.save_settings(profile)
            self.scripts.save_scripts(profile)

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
        with self.try_exception():
            self.save_profile(self.profile)
            self.stop_all_tasks()
            self.scripts.free_all()
            self.AS_task.kill()
            self.keep_going = False
            self.show_profiled()

    def start(self):
        try:
            self.scripts.start_all()
            self.gui.main_loop()
            self.AS_task = gevent.spawn(self.AS.main_loop)
            self.main_loop_task = gevent.spawn(self.main_loop)
        except:
            self.log_error(traceback.format_exc())

    def load_settings(self, profile):
        self.settings = ManagerSettings(self, self.key_manager)
        xml_path = os.path.join(self.get_xml_path(profile), 'settings.xml')
        if not os.path.exists(xml_path):
            return
        self.log_info('Loading global settings')
        with self.try_exception():
            self.settings.load_xml(self.get_settings_xml(profile))

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

    def get_time_string(self):
        return time.ctime(time.time())[11:-5]

    def log_exception(self, exception):
        if self.settings.errors_to_client:
            UO.SysMessage('Error: %s' % str(exception))
        print "\nException: %s\n\n" % traceback.format_exc()

    def log_error(self, message):
        print '\n[%s]ERROR:\n%s\n\n' % (self.get_time_string(), message)

    def log_warning(self, message):
        print 'WARNING: %s\n' % message

    def log_info(self, message):
        print 'INFO: %s\n' % message

    def log_debug(self, message):
        if self.settings.debug_show_messages:
            print '[%s]DEBUG: %s\n' % (self.get_time_string(), message)

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
            with self.try_exception():
                if not UO.CliCnt:
                    self.quit()
                elif not UO.CharName:
                    self.return_to_main()
                if self.client_has_focus() or not self.settings.no_input_outside_client:
                    self.key_manager.execute()


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
