from uo.serpent.props import *
from uo.serpent.script import ScriptBase
from uo import UO, AS, manager
from uo.tools.items import get_items, iter_items_async
from itertools import ifilter
import gevent

class AutoLootScript(ScriptBase):
    script_name = 'Autoloot'

    gold_split_factor = IntSetting('Split gold stacks by', default=1)
    open_corpses_enabled = BoolSetting('Open corpses', group='Features')
    autoloot_delay = FloatSetting('Autoloot delay', default=.05)
    autoloot_enabled = BoolSetting('Enable autoloot', group='Features')
    autoloot_allow_all = BoolSetting('Collect all valuables', group='Rules')
    autoloot_min_value = IntSetting('Minimal item value', default=0, group='Rules')
    autoloot_limit_weight = BoolSetting("Don't allow overweight", default=True, group='Safety')
    autoloot_weight_base = BoolSetting("Use base weight", default=False, group='Safety')
    autoloot_allow_items = ItemKindListSetting("Items to loot (if 'collect all' unchecked)", default={0xeed: 'gold'}, group='Rules', priority=8)
    autoloot_force_items = ItemKindListSetting("Loot even if seems not valuable", default={0xeed: 'gold'}, group='Rules', priority=9)
    autoloot_deny_items = ItemKindListSetting('Never loot', group='Rules', priority=10)
    autoloot_on_keyhold = BoolSetting('Loot only while autoloot key is pressed', group='Crash prevention')
    autoloot_block_rmouse = BoolSetting('Block looting if right mouse button is pressed', default=True, group='Crash prevention')
    loot_bag = ItemSetting('Loot bag', default=[UO.BackpackID, 'Backpack'], group='Bags')
    gold_bag = ItemSetting('Gold bag', default=[UO.BackpackID, 'Backpack'], group='Bags')
    autoloot_disable_in_war = BoolSetting('Disable in war mode', default=False, group='Safety')

    autoloot_hold_pressed = HoldKeysBind('Hold to allow autoloot')

    def load(self):
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
        if self.autoloot_disable_in_war and 'G' in  UO.CharStatus:
            return
        for corpse in self.corpses:
            if corpse not in self.corpses_opened and corpse.distance_to_player <= 2:
                corpse.use()
                self.corpses_opened.add(corpse)

    def allow_loot_item(self, item):
        vc = 'Value calculator' in Manager.scripts.scripts and Manager.scripts.scripts['Value calculator'] or None
        print "TRY LOOT %s" % item.name
        if item.type_ in self.autoloot_force_items:
            print "YEP, it's forced"
            return True
        print 0
        if item.type_ in self.autoloot_deny_items:
            print "nope, it's denied"
            return False
        print 1
        if not self.autoloot_allow_all and not item.type_ not in self.autoloot_allow_items:
            print "Nope, it's not allowed"
            return False
        print 2
        if self.autoloot_limit_weight and (item.properties['Weight'].value or 0) + UO.Weight > UO.MaxWeight:
            print "Nope, it'll cause overweight"
            return False
        print 3
        if self.autoloot_min_value and vc and item.type_:
            print "CHECK VALUE"
            value = vc.calculate_value(item)
            if value < self.autoloot_min_value:
                print "nope, it's value is only", vc
                return False
        return True

    def try_drag(self, item_id, amt):
        if (self.autoloot_hold_pressed or not self.autoloot_on_keyhold) and \
                (not self.manager.key_manager.getkey('RBUTTON') or not self.autoloot_block_rmouse):
            AS.Drag(item_id, amt)
            return True
        return False

    def loot(self):
        if self.autoloot_disable_in_war and 'G' in  UO.CharStatus:
            return
        looted = set()
        if self.autoloot_on_keyhold and not self.autoloot_hold_pressed:
            return
        if self.autoloot_block_rmouse and manager.key_manager.getkey('RBUTTON'):
            return
        for item in ifilter(lambda i: i.cont_id in self.corpses and i.cont_id not in self.corpses_looted, self.items):
            looted.add(item.cont_id)
            if not self.allow_loot_item(item):
                continue
            self.manager.sleep(0)
            is_gold = item.type_ == 0xeed
            dragged = False
            if self.gold_split_factor == 1 or not is_gold:
                dragged = self.try_drag(item.id_, item.stack)
            elif self.gold_split_factor == 0:
                continue
            else:
                dragged = self.try_drag(item.id_, item.stack / self.gold_split_factor)
            self.manager.sleep(.1)
            loot_bag = (self.gold_bag if is_gold else self.loot_bag)
            if dragged:
                AS.DropC(loot_bag)
        self.corpses_looted.update(looted)

    def run_auto_loot(self):
        while True:
            if self.autoloot_enabled:
                self.loot()
            self.manager.sleep(self.autoloot_delay)

    def run_collect(self):
        while True:
            self.collect_items()
            self.manager.sleep(2)

    def run_open_corpses(self):
        while True:
            if self.open_corpses_enabled:
                self.open_corpses()
                self.manager.sleep(self.autoloot_delay)
            else:
                self.manager.sleep(1)

    def main(self):
        self.manager.sleep(0)
        self.manager.spawn(self.run_open_corpses)
        self.manager.spawn(self.run_auto_loot)
        self.run_collect()

