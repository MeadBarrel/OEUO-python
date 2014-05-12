import pygtk
pygtk.require20()
import gtk, gobject
import wx
from pyuo.manager import Loop
from time import sleep

WIDTH = 100
HEIGHT = 20

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None, style=wx.BORDER_NONE|wx.STAY_ON_TOP|wx.TRANSPARENT_WINDOW)

class Script(object):
    name = 'progress_bar'

    def __init__(self):
        self.frame = Frame()
        self.frame.SetSizeWH(0, 0)
        self.frame.SetAutoLayout(True)
        self.panel = wx.Panel(self.frame, size=(0,0))
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.bars = {}

    def add_bar(self, name, color, callback):
        self.bars[name] = (color, callback, 0)
        self.arrange()

    def arrange(self):
        width, height = WIDTH, HEIGHT * len(self.bars)
        #self.frame.SetSizeWH(width, height)
        #self.panel.SetSizeWH(width, height)
        self.frame.Layout()
        self.panel.SetSize((width, height))
        self.frame.SetSize((width, height))
        #self.panel.SetSize((width, height))
        #self.frame.SetSize((width, height))
        print "ARRANGED"
        #print(width, height)
        #print self

    def on_paint(self, event):
        #event.Skip()
        width, height = WIDTH, HEIGHT * len(self.bars)
        #self.frame.SetSize((width, height))
        dc = wx.PaintDC(self.panel)
        y = 0
        arrange = False
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0, 0, width, height)
        for (name, bar) in self.bars.items():
            color, callback, prev = bar
            width = int(callback() * WIDTH)
#            if prev == width:
#                continue
            self.bars[name] = color, callback, width
            dc.SetBrush(color)
            dc.DrawRectangle(0, y, width, HEIGHT)
            y += HEIGHT
            if width <= 0:
                del self.bars[name]
                arrange = True
        if arrange:
            self.arrange()


    def execute(self):
        self.panel.Show()
        self.frame.Show()
        while True:
            self.panel.Refresh()
            sleep(.5)



class Script_old(object):
    name = 'progress_bar'

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False )
        self.window.set_border_width(0)
        self.window.resize(WIDTH, 0)
        self.area = gtk.DrawingArea()
        self.area.set_size_request(WIDTH, 200)
        self.handle = self.window.get_window()
        self.window.add(self.area)
        self.window.show()
        self.area.show()
        self.bars = {}

    def add_bar(self, name, color, callback):
        self.area.set_size_request(WIDTH, HEIGHT)
        self.bars[name] = (color, callback)
        self.arrange()

    def arrange(self):
        width, height = WIDTH, HEIGHT * len(self.bars)
        self.window.resize(WIDTH, HEIGHT * len(self.bars))
        self.area.set_size_request(width, height)

    def update(self):
        y = 0
        style = self.area.get_style()
        gc = self.style.fg_gc[gtk.STATE_NORMAL]
        resize = False
        for name, bar in self.bars.items():
            color, callback = bar
            width = int(callback() * WIDTH)
            self.area.get_colormap().alloc(color)
            new_y = y + HEIGHT
            self.area.window.draw_rectangle(gc, True, 0, y, width, new_y)
            y = new_y
            if width <= 0:
                del self.bars[name]
                resize = True
        if resize:
            self.arrange()

    def callback(self):
        print "EYSEYSUYEUSA"
        self.window.set_keep_above(True)
        gobject.timeout_add_seconds(1, self.callback)

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def free(self):
        self.destroy(self.window)

    def on_begin(self):
        gobject.timeout_add_seconds(1, self.callback)
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
