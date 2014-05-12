import pythoncom, pyHook
import win32api, win32con

def onKeyboardEvent(event):
    print 'MessageName:',event.MessageName
    print 'Message:',event.Message
    print 'Time:',event.Time
    print 'Window:',event.Window
    print 'WindowName:',event.WindowName
    print 'Ascii:', event.Ascii, chr(event.Ascii)
    print 'Key:', event.Key
    print 'KeyID:', event.KeyID
    print 'ScanCode:', event.ScanCode
    print 'Extended:', event.Extended
    print 'Injected:', event.Injected
    print 'Alt', event.Alt
    print 'Transition', event.Transition
    print '---'

class KeyManager(object):
    def __init__(self, manager):
        self.manager = manager

    def onMouseEvent(self, event):
        pass

    def onKeyboardEvent(self, event):
        print "YEAHG"
        print event.Ascii
        print event.Key
        print event.KeyID
        raise Exception

    def execute_(self):
        print 'hooked'
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = onKeyboardEvent
        self.hm.HookKeyboard()
        pythoncom.PumpMessages()

    def execute(self):
        while True:
            #spacebar:
#            i = win32api.GetAsyncKeyState(win32con.VK_SPACE)
            i = win32api.GetAsyncKeyState(0x51)
            if i < 0:
                print "spacebar"
