import os
from xml.etree import cElementTree as ElementTree
from pyuo.manager.props import Setting, KeyBind
from inspect import isfunction
import traceback
from .profiler import ProfiledFunc
import shutil


class SettingsManagerError(Exception):
    pass


class SettingsManager(object):
    def __init__(self, key_manager):
        self.key_manager = key_manager
        self._binds = []
        self.__prepare_binds()
        self._binds = []
        self.__prepare_binds()

    def fetch_binds(self):
        for name in dir(self):
            attr = getattr(self, name)
            if isinstance(attr, KeyBind):
                yield attr
            elif hasattr(attr, '_binds'):
                for bind in getattr(attr, '_binds'):
                    yield bind
        if hasattr(self, '_binds'):
            for bind in self._binds:
                yield bind

    def find_bind(self, name):
        for bind in self.fetch_binds():
            if bind.name == name:
                return bind
        return None

    @classmethod
    def fetch_settings(cls):
        for name, value in vars(cls).iteritems():
            if isinstance(value, Setting):
                yield(name, value)

    @classmethod
    def get_setting(cls, name):
        return vars(cls)[name]

#    def xml_path(self):
#        base, ext = os.path.splitext(self._path)
#        path, fbase = os.path.split(base)
#        return '%s/saved/%s.xml' % (path, fbase)

    def load_xml(self, path):
        try:
            tree = ElementTree.parse(path)
        except:
            raise SettingsManagerError("Could not parse '%s':%s" % (path, traceback.format_exc()))

        root = tree.getroot()
        settings = root.find('settings')
        prop_objects = dict(self.fetch_settings())
        if settings is not None:
            for setting in settings.findall('setting'):
                name = setting.get('name')
                if not name in prop_objects:
                    continue
                if 'value' in setting.keys():
                    value = setting.get('value')
                    unserialized = prop_objects[name].unserialize(value)
                else:
                    unserialized = prop_objects[name].parse_xml(setting)
                setattr(self, name, unserialized)
        for bind_el in settings.findall('keymap'):
            name = bind_el.get('name')
            keys = bind_el.get('keys')
            bind = self.find_bind(name)
            if not bind:
                continue
            bind.set_keys(keys)
            self.key_manager.bind(bind)



    def save_xml(self, path=None):
        folder = os.path.split(path)[0]
        if not os.path.exists(folder):
            os.makedirs(folder)
        root = ElementTree.Element('root')
        settings = ElementTree.SubElement(root, 'settings')
        for setting_name, setting_value in self.fetch_settings():
            element = ElementTree.SubElement(settings, 'setting')
            element.set('name', setting_name)
            serialized = setting_value.serialize(element)
            if serialized is not None:
                element.set('value', serialized)
        for bind in self.fetch_binds():
            if bind.keys is None:
                continue
            element = ElementTree.SubElement(settings, 'keymap')
            element.set('name', bind.name)
            element.set('keys', bind.keys)
        tree = ElementTree.ElementTree(root)
        tree.write(path, 'utf8')

    def __prepare_binds(self):
        for name in dir(self):
            attr = getattr(self, name)
            if hasattr(attr, '_bind_deco'):
                for bd in attr._bind_deco:
                    self._binds.append(KeyBind(attr, *bd))


class ScriptBase(SettingsManager):
    def __init__(self, manager):
        """
        :type manager manager
        """
        super(ScriptBase, self).__init__(manager.key_manager)
        global mgr
        global UO
        mgr = manager
        UO = mgr.UO
        self.manager = manager
        if self.manager.settings.do_debug:
            self.wrap_methods()
        self.load(manager)

    def wrap_methods(self):
        for name, method in vars(self.__class__).iteritems():
            if name.find('__') == 0 or name in dir(ScriptBase) or not isfunction(method) :
                continue
            func = getattr(self, name)
            pf = ProfiledFunc(func, self.manager, self.__class__.__name__)
            self.manager.add_profiled(pf)
            setattr(self, name, pf)

    @classmethod
    def name(cls):
        if hasattr(cls, 'script_name'):
            return cls.script_name
        else:
            return cls.__name__

    def free(self):
        pass

    def load(self, manager):
        pass

    def main(self):
        pass

