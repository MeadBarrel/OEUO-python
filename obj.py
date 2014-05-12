import pygtk
pygtk.require20()
import gtk, gobject
#from ctypes import windll


#SetWindowPos = windll.user32.SetWindowPos


class HelloWorld(object):
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False )
        self.window.set_border_width(0)
        self.handle = self.window.get_window()

        self.button = gtk.Button(u"click me".encode('cp1251'))
        self.button.connect("clicked", self.hello, None)
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.window.add(self.button)
        self.button.show()
        self.window.show()
        gobject.timeout_add_seconds(1, self.callback)

    def callback(self):
        print 'ok'
        self.window.set_keep_above(True)
        #SetWindowPos(self.handle, -1, 0, 0, 0, 0, 0x0001)
        gobject.timeout_add_seconds(1, self.callback)

    def hello(self, widget, data=None):
        print u"Hello, world".encode('cp1251')
        self.destroy(self.window)

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()