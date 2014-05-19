from uo.oeuo import UO, AS
from uo.manager.props import *
from uo.manager.script import ScriptBase
from uo.tools.extensions import request_target
from uo.tools.items import get_by_id
import gevent
import time

class ToolsScript(ScriptBase):
    script_name = 'Tools'
    keep_hiding = BoolSetting('Hide items', default=True)
    hide_item_list = ItemObjListSetting('Items to hide', default={})
    hide_delay = FloatSetting('Hide delay', default=.3)

    def load(self, manager):
        self.update()

    def do_hide_item(self, id_):
        UO.HideItem(id_)

    def update(self):
        for item_id in self.hide_item_list:
            gevent.sleep(self.hide_delay)
            self.do_hide_item(item_id)

    @method_bind('Show config')
    def show_config(self):
        UO.Macro(9, 0)

    @method_bind('Hide item')
    def hide_item(self):
        target = request_target()
        if target:
            id_ = target.id_
        else:
            return
        name = get_by_id(id_, ).name
        self.do_hide_item(id_)
        if id_ not in self.hide_item_list:
            self.hide_item_list[id_] = name

    def main(self):
        return
        while True:
            if self.keep_hiding:
                self.update()
            gevent.sleep(2)

