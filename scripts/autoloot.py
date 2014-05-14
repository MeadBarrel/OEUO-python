from pyuo.manager.props import *
from pyuo.manager.script import ScriptBase
from pyuo.oeuo import UO, AS
from pyuo.tools.items import get_items, iter_items_async
from itertools import ifilter
import gevent

class AutoLootScript(ScriptBase):
    gold_split_factor = IntSetting('Split gold stacks by', default=2)
    open_corpses_enabled = BoolSetting('Open corpses', group='Features')
    autoloot_enabled = BoolSetting('Enable autoloot', group='Features')
    autoloot_allow_all = BoolSetting('Collect all valuables', group='Rules')
    autoloot_min_value = IntSetting('Minimal item value', default=0, group='Rules')
    autoloot_limit_weight = BoolSetting("Don't allow overweight", default=True, group='Safety')
    autoloot_weight_base = BoolSetting("Use base weight", default=False, group='Safety')
    autoloot_force_items = ItemKindListSetting("Loot even if seems invaluable", default=[[0xeed, 'gold']], group='Rules', priority=9)
    autoloot_deny_items = ItemKindListSetting('Never loot', group='Rules', priority=10)
    loot_bag = ItemSetting('Loot bag', default=[UO.BackpackID, 'Backpack'], group='Bags')
    gold_bag = ItemSetting('Gold bag', default=[UO.BackpackID, 'Backpack'], group='Bags')

    def load(self, manager):
        self.AS = self.manager.AS
        self.corpses_looted = set()
        self.corpses_opened = set()
        self.items = []
        self.corpses = []

    @method_bind('toggle auto loot')
    def toggle_auto_loot(self):
        self.autoloot_enabled = not self.autoloot_enabled
        UO.SysMessage('Autoloot %sabled' % ('en' if self.autoloot_enabled else 'dis'))

    @method_bind('toggle open corpses')
    def toggle_open_corpses(self):
        self.open_corpses_enabled = not self.open_corpses_enabled
        UO.SysMessage('Open corspes %sabled' % ('en' if self.open_corpses_enabled else 'dis'))

    def collect_items(self):
        self.items = get_items(True)
        self.corpses = set(item for item in self.items if item.type_ == 8198)


    def open_corpses(self):
        if not self.open_corpses_enabled:
            return
        for corpse in self.corpses:
            if corpse not in self.corpses_opened and corpse.distance_to_player <= 2:
                corpse.use()
                self.corpses_opened.add(corpse)

    def loot(self):
        looted = set()
        for item in ifilter(lambda i: i.cont_id in self.corpses and i.cont_id not in self.corpses_looted, self.items):
            looted.add(item.cont_id)
            gevent.sleep(0)
            is_gold = item.type_ == 0xeed
            if self.gold_split_factor == 1 or not is_gold:
                AS.Drag(item.id_, item.stack)
            elif self.gold_split_factor == 0:
                continue
            else:
                AS.Drag(item.id_, item.stack / self.gold_split_factor)
            gevent.sleep(.1)
            loot_bag = (self.gold_bag if is_gold else self.loot_bag) or UO.BackpackID
            AS.DropC(loot_bag)
        self.corpses_looted.update(looted)

    def run_auto_loot(self):
        while True:
            if self.autoloot_enabled:
                self.loot()
            gevent.sleep(.1)

    def run_collect(self):
        while True:
            self.collect_items()
            gevent.sleep(2)

    def run_open_corpses(self):
        while True:
            if self.open_corpses_enabled:
                self.open_corpses()
                gevent.sleep(.1)
            else:
                gevent.sleep(1)

    def main(self):
        gevent.sleep(0)
        gevent.spawn(self.run_open_corpses)
        gevent.spawn(self.run_auto_loot)
        self.run_collect()

