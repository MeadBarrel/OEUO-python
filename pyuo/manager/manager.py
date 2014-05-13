"""PyOEUO script manager"""

__author__ = 'Lai Tash'
__email__ = 'lai.tash@gmail.com'
__license__ = "GPL"

from ..oeuo import UO
from .script import Script
from threading import Thread
from time import time, sleep
from string import ascii_lowercase
from .key_codes import codes
from itertools import imap
import wx
import gevent
import win32api, win32con


class ScriptThread(Thread):
    def __init__(self, script):
        super(ScriptThread, self).__init__()
        self.script = script
        self.script.thread = self

    def run(self):
        self.script.execute()


class KeyBinder(object):
    keys_list = set(codes.keys())

    def __init__(self, manager):
        self.manager = manager
        self.keys = {key: None for key in self.keys_list}
        self.binds = {}

    def uniform(self, keys_string):
        keys = [key.strip() for key in keys_string.split('+')]
        for key in keys:
            if key not in self.keys_list:
                raise Exception("Cannot bind [%s]: %s is unknown" % key)
        keys.sort()
        return '+'.join(keys)


    def bind(self, keys_string, method):
        keys_string = self.uniform(keys_string)
        self.binds[keys_string] = method

    def has_bind(self, method):
        return method in self.binds.itervalues()

    def get_bind(self, method):
        for key, meth in self.binds.iteritems():
            if meth is method:
                return key

    def remove_bind(self, method):
        if not self.has_bind(method):
            return
        for key, meth in self.binds.items():
            if meth is method:
                del self.binds[key]

    def getkey_int(self, key_int):
        i = win32api.GetAsyncKeyState(key_int)
        return i < 0

    def getkey(self, key):
        key_int = codes[key]
        return self.getkey_int(key_int)

    def execute(self):
        for (keys, method) in self.binds.iteritems():
            keys = keys.split('+')
            if all(imap(self.getkey, keys)):
                gevent.spawn(method)


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
        self.uo = UO
        self.scripts_loaded = {}
        self.loops = []
        self.key_manager = KeyBinder(self)
        self.app = App()
        #self.key_manager = KeyManager(self)

    def __getattr__(self, item):
        if item in self.scripts_loaded:
            return self.scripts_loaded[item]

    def execute_method(self, method):
        method()

    def load(self, abs_path):
        environment = {'UO': UO, 'Manager': self}
        execfile(abs_path, environment)
        if 'Script' in environment:
            script = environment['Script']
            if not hasattr(script, 'name'):
                script.name = script.__class__.__name__
        else:
            script = Script()
            if 'execute' in environment:
                script.execute = environment['execute']
            script.name = environment['name']
        self.add_script(script)

    def add_script(self, script):
        if script.name in self.scripts_loaded:
            raise("Script %s is already loaded" % script.name)
        self.scripts_loaded[script.name] = script()

    def run_script(self, script):
        if hasattr(script, 'on_begin'):
            gevent.spawn(script.on_begin)
        if hasattr(script, 'execute'):
            Thread(target=script.execute).start()
#            thread = ScriptThread(script)
#            thread.start()

    def run_all(self):
        for script in self.scripts_loaded.values():
            self.run_script(script)

    def run_loop(self, loop_method):
        self.loops.append(loop_method)

    def execute_loops(self):
        for loop in self.loops:
            loop.execute()
        self.loops = [loop for loop in self.loops if not loop.stopped]

    def free_all(self):
        for script in self.scripts_loaded.values():
            if hasattr(script, 'free'):
                script.free()

    def stop(self):
        raise Exception('STOP')

    def _run(self):
        self.key_manager.bind("CONTROL+c", self.stop)
        self.run_all()
        gevent.spawn(self.main_loop)
        self.app.MainLoop()
        #Thread(target=self.app.MainLoop).start()
        #self.main_loop()
        #Thread(target=self.run_all).start()
        #self.main_loop()

        #Thread(target=self.main_loop).start()
        #self.run_all()
        #gevent.spawn(self.main_loop)

        #Thread(target=self.app.MainLoop).start()
        #self.main_loop()

    def run(self):
        self._run()
    #    gevent.spawn(self._run)

    def main_loop(self):
        while True:
            try:
                self.key_manager.execute()
                #self.execute_loops()
            except Exception as E:
                self.free_all()
                raise E
            gevent.sleep(0.1)



