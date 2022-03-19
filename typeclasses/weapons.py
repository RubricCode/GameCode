"""
Weapon typeclasses
"""

from typeclasses.items import Equippable


class Weapon(Equippable):
    """
    Typeclass for weapon objects.
    Attributes:
        damage_roll (str): primary damage dice rolled
        handedness (int): indicates single- or double-handed weapon
    """
    slots = ['wield1', 'wield2']
    multi_slot = False

    damage_roll = ""
    crit_mod = 1
    handedness = 1
    range = 'melee'


    def at_object_creation(self):
        super(Weapon, self).at_object_creation()
        self.db.range = self.range
        self.db.damage_roll = self.damage_roll
        self.db.crit_mod = self.crit_mod
        self.db.handedness = self.handedness

    def at_equip(self, character):
        """character.traits.MAB.mod += self.db.damage"""
        pass

    def at_remove(self, character):
        """character.traits.MAB.mod -= self.db.damage"""
        pass


class RangedWeapon(Weapon):
    """
    Typeclass for thrown and single-handed ranged weapon objects.
    Attributes:
        range (int): range of weapon in (units?)
        ammunition Optional(str): type of ammunition used (thrown if None)
    """
    range = 'ranged'
    ammunition = None

    def at_object_creation(self):
        super(RangedWeapon, self).at_object_creation()
        self.db.ammunition = self.ammunition
        self.db.combat_cmdset = 'commands.combat.RangedWeaponCmdSet'

    def at_equip(self, character):
        """character.traits.ATKR.mod += self.db.damage"""
        pass

    def at_remove(self, character):
        """character.traits.ATKR.mod -= self.db.damage"""
        pass

    def get_ammunition_to_fire(self):
        """Checks whether there is proper ammunition and returns one unit."""
        ammunition = [obj for obj in self.location.contents
                      if (obj.is_typeclass('typeclasses.items.Bundlable')
                          or obj.is_typeclass('typeclasses.weapons.RangedWeapon'))
                      and self.db.ammunition in obj.aliases.all()]

        if not ammunition:
            # no individual ammo found, search for bundle
            bundle = [obj for obj in self.location.contents
                      if "bundle {}".format(self.db.ammunition) in obj.aliases.all()
                      and obj.is_typeclass('typeclasses.items.Bundle')]

            if bundle:
                bundle = bundle[0]
                bundle.expand()
                return self.get_ammunition_to_fire()
            else:
                return None
        else:
            return ammunition[0]


class TwoHanded(object):
    """Mixin class for two handed weapons."""
    slots = ['wield1', 'wield2']
    multi_slot = True
    handedness = 2


class TwoHandedWeapon(TwoHanded, Weapon):
    """Typeclass for two-handed melee weapons."""
    pass


class TwoHandedRanged(TwoHanded, RangedWeapon):
    """Typeclass for two-handed ranged weapons."""
    pass
