"""PyOEUO script manager"""

__author__ = 'Lai Tash'
__email__ = 'lai.tash@gmail.com'
__license__ = "GPL"

from ..oeuo import UO, AS
from threading import Thread
from .props import KeyBind
from .key_manager import KeyBinder
from .script import ScriptBase
import wx
import gevent
from .gui.gui import GUIFrame


class ScriptThread(Thread):
    def __init__(self, script):
        super(ScriptThread, self).__init__()
        self.script = script
        self.script.thread = self

    def run(self):
        self.script.execute()

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



class _Manager(object):
    def __init__(self):
        self.UO = UO
        self.AS = AS
        self.scripts_loaded = {}
        self.loops = []
        self.key_manager = KeyBinder(self)
        self.app = App()
        self.gui = GUIFrame(self)
        self.main_loop_task = None
        self.scripts_tasks = []
        self.stopped = False
        #self.key_manager = KeyManager(self)

    #def __getattr__(self, item):
    #    if item in self.scripts_loaded:
    #        return self.scripts_loaded[item]

    def show_gui(self):
        self.gui.Show()

    def load(self, abs_path):
        environment = {'UO': UO, 'AS': self.AS, 'Manager': self}
        execfile(abs_path, environment)
        for name, attr in environment.iteritems():
            if isinstance(attr, type) and issubclass(attr, ScriptBase) and attr.__name__.find('Script') == len(attr.__name__) - 6:
                script = attr
                script._path = abs_path
                self.add_script(script)

    def save(self, script):
        if hasattr(script, 'save_xml'):
            script.save_xml()

    def add_script(self, script):
        if script.name in self.scripts_loaded:
            raise("Script %s is already loaded" % script.name)
        instance = script(self)
        self.scripts_loaded[script.name()] = instance

    def run_script(self, script):
        if hasattr(script, 'main'):
            self.scripts_tasks.append(gevent.spawn(script.main))

    def run_all(self):
        for script in self.scripts_loaded.values():
            self.run_script(script)

    def free_all(self):
        for script in self.scripts_loaded.values():
            if hasattr(script, 'free'):
                script.free()

    def stop(self):
        for task in self.scripts_tasks:
            task.kill()
        self.main_loop_task.kill()
        self.action_stack_loop.kill()
        self.app.keepGoing = False
        for script in self.scripts_loaded.values():
            script.save_xml()

    def _run(self):
        bind = KeyBind(self.stop, 'STOP', 'CONTROL+c')
        bind.bind(self)
        self.run_all()
        self.main_loop_task = gevent.spawn(self.main_loop)
        self.action_stack_loop = gevent.spawn(AS.main_loop)
        self.app.MainLoop()

    def run(self):
        self._run()

    def main_loop(self):
        self.show_gui()
        self.gui.update_settings_panel()
        while True:
            try:
                self.key_manager.execute()
            except Exception as E:
                self.free_all()
                raise E
            gevent.sleep(0.1)



