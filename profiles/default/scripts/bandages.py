from uo.serpent.script import ScriptBase
from uo import UO, AS, manager
from uo.tools.items import ItemFilter
from uo.serpent.props import *
import gevent
import time
import wx

class BandaidsScript(ScriptBase):
    script_name = 'Bandages'

    lh_thres = FloatSetting('Low health bound', default=.4)
    auto = BoolSetting('Auto bandage', default=False)
    watch_journal = BoolSetting('Watch journal', default=True)

    def load(self):
        self.I = 1.0
        self.lhwarn = True
        self.lh_temp_warned = False
        self.continue_auto = True
        self.bandaids = None
        self.current_heal = None
        if 'journal_event' in manager.scripts.scripts:
            strings = ('That being is not damaged',
                       'You apply the bandages, but they barely help.',
                       'You finish applying the bandages'
            )
            manager.scripts.scripts['journal_event'].bind('|'.join(strings), self.inform_red)

    def inform_red(self, line):
        if not self.watch_journal:
            return
        UO.ExMsg(UO.CharID, line, 0, 40)

    @method_bind(name='Toggle auto heal')
    def toggle_auto(self):
        self.auto = not self.auto
        UO.SysMessage('toggled autobandage to %s' % str(self.auto))

    @method_bind(name='Toggle low health warnings')
    def toggle_lowhealth_warning(self):
        self.lhwarn = not self.lhwarn
        UO.SysMessage('toggled low health warnings to %s' % str(self.lhwarn))

    @method_bind(name='Bandage self')
    def bandage_self(self):
        if UO.Hits >= UO.MaxHits:
            UO.ExMsg(UO.CharID, 'You are not damaged')
            return
        if self.bandaids is not None:
            if self.bandaids.use_on(UO.CharID):
                self.do_bandage_self()

    def healing_formula(self, on_self=True):
        result_time = 8
        dex = UO.Dex
        if dex >= 80:
            result_time -= (dex - 80) / 20
        if not on_self:
            result_time /= 2
        return result_time

    def do_bandage_self(self):
        if UO.Hits >= UO.MaxHits:
            UO.SysMessage('You are not damaged')
            return
        time_to_heal = self.healing_formula()
        started = time.time()
        def clb():
            passed = time.time() - started
            return (time_to_heal - passed) / time_to_heal
        self.current_heal = clb
        if 'Progress bars' in Manager.scripts.scripts:
            manager.scripts.scripts['Progress bars'].add_bar('first', wx.GREEN_BRUSH, clb)

    def low_health_warnings(self):
        while True:
            percent = float(UO.Hits) / UO.MaxHits
            if self.lh_temp_warned and percent > self.lh_thres:
                self.lh_temp_warned = False
                continue
            if percent <= self.lh_thres and not self.lh_temp_warned:
                self.lh_temp_warned = True
                self.inform_red('LOW HEALTH')
                continue
            gevent.sleep(.2)

    def auto_bandage_self(self):
        while True:
            gevent.sleep(.2)
            if self.current_heal:
                hv = self.current_heal()
                if hv <= 0: self.current_heal = None
            if UO.Hits >= UO.MaxHits or not self.auto:
                continue
            if not self.current_heal:
                self.bandage_self()

    def begin(self):
        while True:
            self.bandaids = ItemFilter().with_type(0xe21).in_backpack_rec().first()
            gevent.sleep(2)

    def main(self):
        self.manager.sleep(0)
        self.manager.spawn(self.begin)
        self.manager.spawn(self.auto_bandage_self)
        self.low_health_warnings()








