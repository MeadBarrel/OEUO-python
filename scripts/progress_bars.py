import pygtk
pygtk.require20()
import wx
import gevent

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
        self.frame.Layout()
        self.panel.SetSize((width, height))
        self.frame.SetSize((width, height))

    def on_paint(self, event):
        width, height = WIDTH, HEIGHT * len(self.bars)
        dc = wx.PaintDC(self.panel)
        y = 0
        arrange = False
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0, 0, width, height)
        for (name, bar) in self.bars.items():
            color, callback, prev = bar
            width = int(callback() * WIDTH)
            self.bars[name] = color, callback, width
            dc.SetBrush(color)
            dc.DrawRectangle(0, y, width, HEIGHT)
            y += HEIGHT
            if width <= 0:
                del self.bars[name]
                arrange = True
        if arrange:
            self.arrange()


    def on_begin(self):
        self.panel.Show()
        self.frame.Show()

        while True:
            self.frame.Refresh()
            self.panel.Refresh()
            gevent.sleep(.5)


