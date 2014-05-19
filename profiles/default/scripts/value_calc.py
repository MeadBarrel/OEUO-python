from uo.serpent.script import ScriptBase
from uo.serpent.props import *
from uo.tools.items import Item, get_by_id
from uo.tools.extensions import request_target

class ValueCalculatorScript(ScriptBase):
    script_name = 'Value calculator'

    base_value = IntSetting('Base Value', default=1000)
    area_damage_factor = FloatSetting('fArea Damage', default=2, group='Damage')
    balanced_factor = FloatSetting('fBalanced', default=2, group='Properties')
    best_wpn_skill_factor = FloatSetting('fUse Best Weapon Skill', default=2, group='Properties')
    cold_resist_factor = FloatSetting('fCold Resist', default=5, group='Resistances')
    damage_increase_factor = FloatSetting('fDamage Increase', default=100, group='Damage')
    defence_chance_increase_factor = FloatSetting('fDefence Chance Increase', default=100, group='Defense')
    dex_bonus_factor = FloatSetting('fDextierity Bonus', default=10, group='Stats')
    durability_factor = FloatSetting('fDurability', default=1.2, group='Properties')
    energy_resist_factor = FloatSetting('fEnergy Resist', default=5, group='Resistances')
    enhance_potions_factor = FloatSetting('fEnhance Potions', default=100, group='Effects')
    faster_cast_recovery_factor = FloatSetting('fFaster Cast Recovery', default=1000, group='Effects')
    faster_casting_factor = FloatSetting('fFaster Casting', default=1000, group='Effects')
    fire_resist_factor = FloatSetting('fFire Resist', default=5, group='Resistances')
    hit_chance_increase_factor = FloatSetting('fHit Chance Increase', default=3, group='Damage')
    hit_dispel_factor = FloatSetting('fHit Dispel', default=1.2, group='Damage')
    hit_maroow = FloatSetting('fHit Magic Arrow', default=5, group='Damage')
    hit_fireball = FloatSetting('fHit Fireball', default=10, group='Damage')
    hit_lightning = FloatSetting('fHit Lightning', default=15, group='Damage')
    hit_life_leech = FloatSetting('fHit Life Leech', default=4, group='Damage')
    hit_lower_attack = FloatSetting('fHit Lower Attack', default=4, group='Damage')
    hit_lower_defence = FloatSetting('fHit Lower Defence', default=4, group='Damage')
    hit_mana_leech = FloatSetting('fHit Mana Leech', default=4, group='Damage')
    intelligence_bonus = FloatSetting('fIntelligence Bonus', default=10, group='Stats')
    lower_stamina_cost = FloatSetting('fLower Stamina Cost', default=5, group='Effects')
    lower_mana_cost = FloatSetting('fLower Mana Cost', default=20, group='Effects')
    lower_reagent_cost = FloatSetting('fLower Reagent Cost', default=20, group='Effects')
    lower_requirements = FloatSetting('fLower Requirements', default=1.2, group='Properties')
    luck_factor = FloatSetting('fLuck', default=1000, group='Effects')
    mage_armor = FloatSetting('fMage Armor', default=100, group='Properties')
    mana_regen = FloatSetting('fManaRegeneration', default=100, group='Stats')
    phys_resist = FloatSetting('fPhysical Resist', default=8, group='Resistances')
    pois_resist = FloatSetting('fPoison Resist', default=5, group='Resistances')
    water_resist = FloatSetting('fWater Resist', default=5, group='Resistances')
    cold_resist = FloatSetting('fCold Resist', default=5, group='Resistances')
    reflect_phys = FloatSetting('fReflect Physical Damage', default=2, group='Resistances')
    self_repair = FloatSetting('fSelf Repair', default=30, group='Properties')
    spell_channel = FloatSetting('fSpell Channeling', default=100, group='Properties')
    spell_dam_inc = FloatSetting('fSpell Damage Increase', default=20, group='Effects')
    stamina_increase = FloatSetting('fStamina Increase', default=5, group='Stats')
    stamina_regen = FloatSetting('fStamina Regeneration', default=50, group='Stats')
    strenght_bonus = FloatSetting('fStrenght Bonus', default=10, group='Stats')
    swing_speed_inc = FloatSetting('fSwing Speed Increase', default=50, group='Damage')
    velocity_factor = FloatSetting('fVelocity', default=200, group='Properties')

    poison_damage = FloatSetting('fPoison Damage', default=20, group='Damage Type')
    energy_damage = FloatSetting('fEnergy Damage', default=20, group='Damage Type')
    water_damage = FloatSetting('fWater Damage', default=20, group='Damage Type')
    cold_damage = FloatSetting('fCold Damage', default=20, group='Damage Type')
    fire_damage = FloatSetting('fFire Damage', default=20, group='Damage Type')
    phys_damage = FloatSetting('fPhysical Damage', default=10, group='Damage Type')

    #TODO: slayers
    #TODO: skill bonuses
    bushido = FloatSetting('fBushido', default=50, group='Skills')
    tactics = FloatSetting('fTactics', default=30, group='Skills')
    swordsmanship = FloatSetting('fSwordsmanship', default=40, group='Skills')
    archery = FloatSetting('fArchery', default=40, group='Skills')
    magery = FloatSetting('fMagery', default=50, group='Skills')
    eval_int = FloatSetting('fEval Intelligence', default=30, group='Skills')
    anatomy = FloatSetting('fAnatomy', default=30, group='Skills')
    healing = FloatSetting('fHealing', default=50, group='Skills')
    chivalry = FloatSetting('fChivalry', default=50, group='Skills')
    ninjitsu = FloatSetting('fNinjitsu', default=50, group='Skills')
    stealth = FloatSetting('fStealth', default=50, group='Skills')
    hiding = FloatSetting('fHiding', default=50, group='Skills')


    @method_bind('Show item value')
    def show_value(self):
        target = request_target()
        if not target:
            return
        item = get_by_id(target.id_)
        value = self.calculate_value(item)
        print value

    def calculate_value(self, item):
        """
        :type item Item
        """
        result = 0
        props = item.properties
        settings = self.fetch_settings()
        print props.full_string()
        for setting_name, setting in settings:
            if setting.name.find('f') != 0:
                continue
            rest = setting.name[1:]
            if rest in props:
                prop = props[rest]
                value = prop.value
                result += self.base_value + value * setting.value
        return result


