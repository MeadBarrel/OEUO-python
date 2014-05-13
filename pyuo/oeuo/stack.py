"""
The library to communicate with uo.dll.
"""

__description__ = "stack.py - uo.dll communication"
__author__ = 'Lai Tash'
__email__ = 'lai.tash@gmail.com'
__license__ = "GPL"


from ctypes import *
from ctypes.wintypes import *


dll = WinDLL('uo')
_dll_version = dll.Version()


dll.GetBoolean.restype = BOOL
dll.GetString.restype = c_char_p
dll.GetDouble.restype = c_double
from threading import Lock


class StackError(Exception):
    pass


class BaseStack(object):
    """Low-level stack representation"""
    def __init__(self):
        self.hnd = dll.Open()
        print self.hnd

    def Close(self):
        dll.Close(self.hnd)
        self.hnd = None

    def _check_index(self, idx):
        if idx > self.GetTop():
            raise IndexError('%d not in stack' % idx)

    def Execute(self):
        return dll.Execute(self.hnd)

    def Query(self):
        return dll.Query(self.hnd)

    def PushNil(self):
        return dll.PushNil(self.hnd)

    def PushBoolean(self, value):
        return dll.PushBoolean(self.hnd, BOOL(bool(value)))

    def PushInteger(self, value):
        return dll.PushInteger(self.hnd, c_int(int(value)))

    def PushDouble(self, value):
        return dll.PushDouble(self.hnd, c_double(float(value)))

    def PushStrRef(self, value):
        """Push a string reference and return the referenced buffer"""
        result = create_string_buffer(str(value))
        dll.PushStrRef(self.hnd, result)
        return result

    def PushStrVal(self, value):
        return dll.PushStrVal(self.hnd, c_char_p(str(value)))

    def GetBoolean(self, idx):
        self._check_index(idx)
        return bool(dll.GetBoolean(self.hnd, idx))

    def GetInteger(self, idx):
        self._check_index(idx)
        return int(dll.GetInteger(self.hnd, idx))

    def GetDouble(self, idx):
        self._check_index(idx)
        return float(dll.GetDouble(self.hnd, idx))

    def GetString(self, idx):
        self._check_index(idx)
        return str(dll.GetString(self.hnd, idx))

    def GetTop(self):
        return dll.GetTop(self.hnd)

    def GetType(self, idx):
        self._check_index(idx)
        return dll.GetType(self.hnd, idx)

    def SetTop(self, idx):
        self._check_index(idx)
        return dll.SetTop(self.hnd, idx)

    def Insert(self, idx):
        self._check_index(idx)
        return dll.Insert(self.hnd, idx)

    def PushValue(self, idx):
        self._check_index(idx)
        return dll.PushValue(self.hnd, idx)

    def Remove(self, idx):
        self._check_index(idx)
        return dll.Remove(self.hnd, idx)

    def Mark(self):
        return dll.Mark(self.hnd)

    def Clean(self):
        return dll.Clean(self.hnd)

    def ListRVars(self):
        return dll.ListRVars(self.hnd)

#    def SetVar(self, vname, vvalue):
#        return dll.SetVar(self.hnd, vname, vvalue)

#    def GetVar(self, vname):
#        return dll.GetVar(self.hnd, vname)

    def GetVarHelp(self, vname):
        return dll.GetVarHelp(self.hnd, vname)

    def GetFeatures(self):
        return dll.GetFeatures(self.hnd)

    def __del__(self):
        if self.hnd is not None:
            if dll is None:
                raise RuntimeError('Dll freed before stack could be closed')
            self.Close()



class Stack(BaseStack):
    def __init__(self):
        super(Stack, self).__init__()
        self.lock = Lock()
        self.vtypes = (
            None,
            self.GetBoolean,
            None,
            self.GetInteger,
            self.GetString
        )

    def _call_old(self, method, *args):
        self.top = 0
        for arg in args:
            self.push(arg)
        print vars(dll)
        err = getattr(dll, method)(self.hnd)
        if err == 0:
            if len(self) == 1: return self[0]
            elif len(self) == 0: return None
            else: return tuple(self)
        else:
            self.top = 0
            self.push('GetError')
            self.push(err)
            assert dll.Query(self.hnd) == 0, 'GetError call failed'
            raise StackError('Error %r while calling %s%r' % (self[0], args[0], tuple(args[1:])))

    def _call(self, method, *args):
        self.top = 0
        self.push(method)
        for arg in args:
            if arg is not None:
                self.push(arg)
        result = self.Execute()
        if not result:
            if len(self) == 1: return self[0]
            elif len(self) == 0: return None
            else: return tuple(self)
        else:
            raise StackError('Error while executing %s (%i)' % (method, result))

    def execute(self, method, *args):
        with self.lock:
            result = self._call(method, *args)
            return result

    def push(self, value):
        if isinstance(value, bool):
            return self.PushBoolean(value)
        elif isinstance(value, int):
            return self.PushInteger(value)
        elif isinstance(value, float):
            return self.PushDouble(value)
        elif isinstance(value, str):
            return self.PushStrVal(value)
        else:
            raise StackError('Cannot push value %s: incompatible type' % value)

    def get_value(self, idx, vtype=None):
        idx = idx + 1
        if idx > self.top:
            raise IndexError('Index %d not on stack' % idx)
        if vtype is None:
            dt = dll.GetType(self.hnd, idx)
            if dt == 0:
                return None
            if dt == 2 or dt > 4:
                raise TypeError('Invalid type: %d' % dt)
            vtype = self.vtypes[dt]
        return vtype(idx)

    def __getitem__(self, item):
        return self.get_value(item)

    @property
    def top(self):
        return dll.GetTop(self.hnd)

    @top.setter
    def top(self, idx):
        dll.SetTop(self.hnd, idx)

    def __len__(self):
        return self.GetTop()


