from abc import ABCMeta, abstractmethod
from xml.etree import cElementTree as ElementTree
from pyuo.tools.widgets.item_select import ItemSelectButton, EVT_ITEM_SELECT
from pyuo.tools.items import get_by_id
import wx

from .key_manager import BindError


def bind(name=None, default_keys=None, allow_repeat=False, args=None, kwargs=None):
    def _wraps(method):
        new_bind = KeyBind(method, name, default_keys, allow_repeat, args, kwargs)
        if not hasattr(method, '_binds'):
            setattr(method, '_binds', [])
        getattr(method, '_binds').append(new_bind)
        return method
    return _wraps


def method_bind(name=None, default_keys=None, allow_repeat=False, args=None, kwargs=None):
    def _wraps(method):
        _bind_deco_ = (name, default_keys, allow_repeat, args, kwargs)
        if not hasattr(method, '_bind_deco'):
            method._bind_deco = []
        method._bind_deco.append(_bind_deco_)
        return method
    return _wraps


class KeyBind(object):
    def __init__(self, method, name=None, default_keys=None, allow_repeat=False, args=None, kwargs=None):
        if name is None:
            name = '%s(%s%s)' % (method.__name__, ', '.join(map(str, args or [])),
                                 ', '.join(["%s=%s" % (name, value) for name, value in (kwargs or {}).iteritems()]))
        self.name = name
        self.method = method
        self.args = args or []
        self.kwargs = kwargs or {}
        self.keys = default_keys
        self.allow_repeat = allow_repeat

    def set_keys(self, keys):
        self.keys = keys

    def bind(self, manager):
        if not self.keys:
            raise BindError('Cannot bind to an empty string...')
        self.unbind(manager)
        try:
            manager.key_manager.bind(self)
        except Exception as E:
            raise BindError(E.message)

    def unbind(self, manager):
        if manager.key_manager.get_keys(self):
            manager.key_manager.unbind(self)

    def __call__(self):
        return self.method(*self.args, **self.kwargs)


class SettingError(Exception):
    pass


class Setting(object):
    __metaclass__ = ABCMeta
    _required_type = None
    _default = 0
    _value = None
    wx_control = None

    def __init__(self, name, default=None, on_change=None, group=None, priority=0, relation=None):
        self.__name = name
        self._default = default if default is not None else self._default
        self.group = group or 'Base'
        if not isinstance(self.group, str):
            raise SettingError('group must be string')
        self.priority = priority
        self.on_change = on_change
        self.relation = relation
        self.relations = []
        if relation:
            relation.add_relation(self)

    def change(self):
        if self.on_change is not None:
            self.on_change(self.value)
        if self.relations:
            self.update_relations()

    def update_relations(self):
        pass

    def add_relation(self, other):
        self.relations.append(other)

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        if self._value is None:
            return self._default
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.change()

    def serialize(self, element):
        return str(self.value)

    def unserialize(self, value):
        return self._required_type(value)

    def parse_xml(self, element):
        raise Exception('not implemented for this setting')

    def check_type(self, value):
        return isinstance(value, self._required_type)

    def __set__(self, instance, value):
        if not self.check_type(value):
            raise SettingError()
        if self._value == value:
            return
        self._value = value
        print "Set to %s and now it is %s" %(self._value, self.value)
        if self.on_change:
            self.on_change()
        if self.wx_control:
            self.update_wx()

    def __get__(self, instance, owner):
        return self.value

    @abstractmethod
    def init_wx(self, parent):
        pass

    def update_wx(self):
        self.wx_control.Value = str(self.value)
        self.wx_control.Refresh()

    def update_from_wx(self, event):
        try:
            self.value = self._required_type(self.wx_control.Value)
        except SettingError:
            return

    def enable(self):
        self.wx_control.Enable()

    def disable(self):
        self.wx_control.Disable()

class IntSetting(Setting):
    _required_type = int
    _default = 0
    def __init__(self, name, range=None, *args, **kwargs):
        super(IntSetting, self).__init__(name, *args, **kwargs)
        if range is None:
            self.range = (-0xffffff, 0xffffff)
        else:
            self.range = range

    def update_wx(self):
        self.wx_control.Value = self.value

    def init_wx(self, parent):
        super(IntSetting, self).init_wx(parent)
        self.wx_control = wx.SpinCtrl(parent, value='0')
        self.wx_control.SetRange(*self.range)
        self.wx_control.Bind(wx.EVT_SPINCTRL, self.update_from_wx)
        return self.wx_control

class FloatSetting(Setting):
    _required_type = float
    _default = 0.0
    def update_from_wx(self, event):
        try:
            self.value = float(self.wx_control.Value)
            self.wx_control.SetBackgroundColour(wx.WHITE)
        except ValueError:
            self.wx_control.SetBackgroundColour(wx.RED)
        except SettingError:
            self.wx_control.SetBackgroundColour(wx.RED)
        self.wx_control.Refresh()

    def init_wx(self, parent):
        super(FloatSetting, self).init_wx(parent)
        self.wx_control = wx.TextCtrl(parent, value='')
        self.wx_control.Bind(wx.EVT_TEXT, self.update_from_wx)
        return self.wx_control

    def disable(self):
        self.wx_control.Disable()

    def enable(self):
        self.wx_control.Enable()

class StringSetting(Setting):
    _required_type = str
    _default = ''

    def init_wx(self, parent):
        super(StringSetting, self).init_wx(parent)
        self.wx_control = wx.TextCtrl(parent, value='')
        self.wx_control.Bind(wx.EVT_TEXT, self.update_from_wx)
        return self.wx_control

    def disable_wx(self):
        self.wx_control.Disable()

    def enable_wx(self):
        self.wx_control.Enable()


class BoolSetting(Setting):
    _required_type = bool
    _default = False

    def __init__(self, *args, **kwargs):
        super(BoolSetting, self).__init__(*args, **kwargs)
        self.relations = []

    def init_wx(self, parent):
        super(BoolSetting, self).init_wx(parent)
        self.wx_control = wx.CheckBox(parent)
        self.wx_control.Bind(wx.EVT_CHECKBOX, self.update_from_wx)
        return self.wx_control

    def unserialize(self, value):
        return value=="True"

    def update_wx(self):
        self.wx_control.Value = self.value
        self.update_relations()

    def disable(self):
        if self.wx_control:
            self.wx_control.Disable()

    def enable(self):
        if self.wx_control:
            self.wx_control.Enable()

    def update_relations(self):
        for relation in self.relations:
            relation.enable() if self.value else relation.disable()

    def update_from_wx(self, event):
        self.value = self._required_type(self.wx_control.Value)
        if self.value:
            self.update_relations()



class IntListSetting(Setting):
    _required_type = list
    _default = []

    def serialize(self, element):
        for item in self.value:
            subel = ElementTree.SubElement(element, 'item')
            subel.set('value', str(item))

    def unserialize(self, value):
        return None

    def parse_xml(self, element):
        result = []
        for subel in element.findall('item'):
            value = subel.get('value')
            result.append(int(value))
        return result

    def text_modified(self, event):
        event.Skip()
        try:
            int(self.wx_input.Value)
            self.wx_input.SetBackgroundColour(wx.WHITE)
            self.wx_add_button.Enable()
        except ValueError:
            self.wx_add_button.Disable()
            self.wx_input.SetBackgroundColour(wx.RED)
        self.wx_control.Refresh()

    def add_button_pressed(self, event=None):
        if event:
            event.Skip()
        try:
            value = int(self.wx_input.Value)
        except ValueError:
            return
        self.wx_list.Append(self.wx_input.Value)
        self.wx_input.Value = ''
        self.value.append(value)
        self.change()

    def remove_button_pressed(self, event):
        selection = self.wx_list.GetSelection()
        if selection == wx.NOT_FOUND:
            return
        self.wx_list.Delete(selection)
        self.value.pop(selection)

    def item_selected(self, event):
        if self.wx_list.GetSelection() == wx.NOT_FOUND:
            self.wx_remove_button.Disable()
        else:
            self.wx_remove_button.Enable()

    def init_wx(self, parent):
        super(IntListSetting, self).init_wx(parent)
        self.wx_control = wx.Panel(parent)
        self.wx_sizer = wx.FlexGridSizer(cols=1, rows=3)
        self.wx_sizer.AddGrowableCol(0)
        self.wx_list = wx.ListBox(self.wx_control, choices=map(str, self.value))
        self.wx_list.SetMinSize((self.wx_list.MinWidth, 70))
        self.wx_input = wx.TextCtrl(self.wx_control)
        self.wx_add_button = wx.Button(self.wx_control, label='Add')
        self.wx_remove_button = wx.Button(self.wx_control, label='Remove')
        self.wx_sizer.Add(self.wx_list, 1, wx.EXPAND)
        self.wx_sizer.Add(self.wx_input, 1, wx.EXPAND)
        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_sizer.Add(self.wx_add_button, 1, wx.ALIGN_RIGHT)
        self.btn_sizer.Add(self.wx_remove_button, 1, wx.ALIGN_RIGHT)
        self.wx_sizer.Add(self.btn_sizer, 1, wx.EXPAND)
        self.wx_control.SetSizer(self.wx_sizer)
        self.wx_input.Bind(wx.EVT_TEXT, self.text_modified)
        self.wx_add_button.Bind(wx.EVT_BUTTON, self.add_button_pressed)
        self.wx_remove_button.Bind(wx.EVT_BUTTON, self.remove_button_pressed)
        return self.wx_control

class ItemSetting(Setting):
    _required_type = list
    _default = [0,'unknown']

    def __get__(self, instance, owner):
        return super(ItemSetting, self).__get__(instance, owner)[0]

    def item_picked(self, event):
        event.Skip()
        id_ = event.target.id_
        if id_ is not None:
            if self.value[0] == id_:
                return
            item = get_by_id(id_)
            name = item.name
            self.value = [id_, name]
            self.update_wx()

    def update_wx(self):
        print "UPDATE %s" % str(self.value)
        self.wx_label.LabelText = '%i (%s)' % tuple(self.value)

    def serialize(self, element):
        element.set('item_id', str(self.value[0]))
        element.set('item_name', self.value[1])

    def unserialize(self, value):
        return None

    def parse_xml(self, element):
        id_ = element.get('item_id')
        name = element.get('item_name')
        return [int(id_), name]

    def init_wx(self, parent):
        super(ItemSetting, self).__init__(parent)
        self.wx_control = wx.Panel(parent)
        self.wx_sizer = wx.FlexGridSizer(rows=1, cols=2)
        self.wx_sizer.AddGrowableCol(0)
        self.wx_label = wx.StaticText(self.wx_control)
        self.wx_label.ForegroundColour = wx.GREEN
        self.wx_label.BackgroundColour = wx.BLACK
        self.wx_pick_button = ItemSelectButton(self.wx_control, label='Pick')
        self.wx_pick_button.Bind(EVT_ITEM_SELECT, self.item_picked)
        self.wx_sizer.Add(self.wx_label, 1, wx.EXPAND)
        self.wx_sizer.Add(self.wx_pick_button)
        self.wx_control.SetSizer(self.wx_sizer)
        return self.wx_control


class ItemObjListSetting(Setting):
    _required_type = dict
    _default = {}

    def __set__(self, instance, value):
        if not self.check_type(value):
            raise SettingError()
        if self._value and self._value.keys() == value.keys():
            return
        super(ItemObjListSetting, self).__set__(instance, value)

    def item_picked(self, event):
        event.Skip()
        id_ = event.target.id_
        if id_ in self.value:
            return
        item = get_by_id(id_)
        if item is not None:
            name = item.name
            self.value[id_] = name
            self.wx_list.Append([str(id_), name])
            self.change()

    def serialize(self, element):
        for item, name in self.value.iteritems():
            subel = ElementTree.SubElement(element, 'item')
            subel.set('value', str(item))
            subel.set('name', str(name))

    def unserialize(self, value):
        return None

    def parse_xml(self, element):
        result = {}
        for subel in element.findall('item'):
            value = subel.get('value')
            name = subel.get('name')
            result[int(value)] = name
        return result

    def remove_button_pressed(self, event):
        cnt = self.wx_list.GetSelectedItemCount()
        if cnt == 0:
            return
        index = self.wx_list.GetFirstSelected()
        selection = [index]
        while len(selection) != cnt:
            index = self.wx_list.GetNextSelected(index)
            selection.append(index)
        for selected in selection:
            self.value.pop(int(self.wx_list.GetItem(selected, 0).GetText()))
            self.wx_list.DeleteItem(selected)

    def item_selected(self, event):
        if self.wx_list.GetSelectedItemCount() == 0:
            self.wx_remove_button.Disable()
        else:
            self.wx_remove_button.Enable()

    def update_wx(self):
        self.wx_list.ClearAll()
        self.wx_list.InsertColumn(0, 'id', width=100)
        self.wx_list.InsertColumn(1, 'name', wx.LIST_FORMAT_RIGHT)
        for value, name in self.value.iteritems():
            self.wx_list.Append([str(value), name])
        self.wx_control.Refresh()

    def init_wx(self, parent):
        super(ItemObjListSetting, self).init_wx(parent)
        self.wx_control = wx.Panel(parent)
        self.wx_sizer = wx.FlexGridSizer(cols=1, rows=2)
        self.wx_sizer.AddGrowableCol(0)
        self.wx_list = wx.ListCtrl(self.wx_control, style=wx.LC_REPORT)
        self.wx_list.InsertColumn(0, 'id', width=100)
        self.wx_list.InsertColumn(1, 'name', wx.LIST_FORMAT_RIGHT)
        self.wx_list.SetMinSize((self.wx_list.MinWidth, 70))
        self.wx_list.Bind(wx.EVT_LISTBOX, self.item_selected)
        self.pick_item_button = ItemSelectButton(self.wx_control, label='Pick')
        self.pick_item_button.Bind(EVT_ITEM_SELECT, self.item_picked)
        self.wx_remove_button = wx.Button(self.wx_control, label='Remove')
        self.wx_sizer.Add(self.wx_list, 1, wx.EXPAND)
        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_sizer.Add(self.pick_item_button, 2, wx.EXPAND)
        self.btn_sizer.Add(self.wx_remove_button, 1, wx.ALIGN_RIGHT)
        self.wx_sizer.Add(self.btn_sizer, 1, wx.EXPAND)
        self.wx_control.SetSizer(self.wx_sizer)
        self.wx_remove_button.Bind(wx.EVT_BUTTON, self.remove_button_pressed)
        return self.wx_control


class ItemKindListSetting(ItemObjListSetting):

    def item_picked(self, event):
        event.Skip()
        id = event.target.id_
        item = get_by_id(id)
        if item is not None:
            if item.type_ in self.value:
                return
            name = item.name
            type_ = item.type_
            self.value[type_] = name
            self.wx_list.Append([str(type_), name])
            self.change()

    def update_wx(self):
        self.wx_list.ClearAll()
        self.wx_list.InsertColumn(0, 'type', width=100)
        self.wx_list.InsertColumn(1, 'name', wx.LIST_FORMAT_RIGHT)
        for value, name in self.value.iteritems():
            self.wx_list.Append([str(value), name])
        self.wx_control.Refresh()

class StrListSetting(Setting):
    _required_type = list
    _default = []

    def add_button_pressed(self, event):
        event.Skip()
        value = self.wx_input.Value
        self.wx_list.Append(self.wx_input.Value)
        self.value.append(value)
        self.change()

    def serialize(self, element):
        for item in self.value:
            subel = ElementTree.SubElement(element, 'item')
            subel.set('value', item)

    def unserialize(self, value):
        return None

    def parse_xml(self, element):
        result = []
        for subel in element.findall('item'):
            value = subel.get('value')
            result.append(value)
        return result

    def update_wx(self):
        self.wx_list.Clear()
        self.wx_list.AppendItems(self.value)
        self.wx_control.Refresh()

    def remove_button_pressed(self, event):
        event.Skip()
        selection = self.wx_list.GetSelection()
        if selection == wx.NOT_FOUND:
            return
        self.wx_list.Delete(selection)
        self.value.pop(selection)

    def item_selected(self, event):
        if self.wx_list.GetSelection() == wx.NOT_FOUND:
            self.wx_remove_button.Disable()
        else:
            self.wx_remove_button.Enable()


    def init_wx(self, parent):
        super(StrListSetting, self).init_wx(parent)
        self.wx_control = wx.Panel(parent)
        self.wx_sizer = wx.FlexGridSizer(cols=1, rows=3)
        self.wx_sizer.AddGrowableCol(0)
        self.wx_list = wx.ListBox(self.wx_control, choices=self.value)
        self.wx_list.SetMinSize((self.wx_list.MinWidth, 70))
        self.wx_input = wx.TextCtrl(self.wx_control)
        self.wx_add_button = wx.Button(self.wx_control, label='Add')
        self.wx_remove_button = wx.Button(self.wx_control, label='Remove')
        self.wx_sizer.Add(self.wx_list, 1, wx.EXPAND)
        self.wx_sizer.Add(self.wx_input, 1, wx.EXPAND)
        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_sizer.Add(self.wx_add_button, 1, wx.ALIGN_RIGHT)
        self.btn_sizer.Add(self.wx_remove_button, 1, wx.ALIGN_RIGHT)
        self.wx_sizer.Add(self.btn_sizer, 1, wx.EXPAND)
        self.wx_control.SetSizer(self.wx_sizer)
        self.wx_add_button.Bind(wx.EVT_BUTTON, self.add_button_pressed)
        self.wx_remove_button.Bind(wx.EVT_BUTTON, self.remove_button_pressed)
        self.wx_list.Bind(wx.EVT_LISTBOX, self.item_selected)
        return self.wx_control
