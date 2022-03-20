"""
Primary module for guilds within Mercadia
"""

from evennia.server.sessionhandler import SESSIONS
from world.rulebook import roll_max
from evennia.utils import fill
from evennia import Command
from typeclasses.resources import ResourceCmdSet
from commands.powers import artisan, assassin, fighter, mage, merchant, \
    monk, samurai, shaman, sorcerer, thief, trader, warrior, helotyr, \
    templar, sarthoar, harbinger, druid, ranger

# Melee Type Bases
F_BAB = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
         16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

F_FSAVE = [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,
           10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17]

F_RSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

F_WSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

# Divine Caster Type Bases
C_BAB = [0, 0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9, 10, 10,
         11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18]

C_FSAVE = [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,
           10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17]

C_RSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

C_WSAVE = [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,
           10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17]

# Agile Type Bases
R_BAB = [0, 0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9, 10, 11,
         12, 12, 13, 14, 15, 15, 16, 17, 18, 18, 19, 20, 21, 21, 22]

R_FSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

R_RSAVE = [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,
           10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17]

R_WSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

# Trades Type Bases
T_BAB = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7,
         8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15]

T_FSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

T_RSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

T_WSAVE = [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,
           10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17]

# Arcane Caster Type Bases
M_BAB = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7,
         8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15]

M_FSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

M_RSAVE = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
           5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10]

M_WSAVE = [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,
           10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17]

# General Type Bases
G_BAB = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5]

G_FSAVE = [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]

G_RSAVE = [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]

G_WSAVE = [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]

all_guilds = ("Peon", "Peasant", "Servant", "Slave", "Conscript", "Commoner", "Fighter", "Mage", "Thief", "Cleric",
              "Templar", "SarthoarCleric", "Druid", "Harbinger", "Ranger", "Warrior", "Sorcerer", "Assassin", "Samurai",
              "Shaman", "Monk", "Merchant", "Artisan", "Trader")


class CmdGuildJoin(Command):
    """This is the command string that will assign a Guild onto a character,
     and the cooresponding command set."""

    key = "join"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        guild = self.args.strip().lower

        apply_guild(caller, guild)


class GuildException(Exception):
    """Base exception class for races module."""

    def __init__(self, msg):
        self.msg = msg


def load_guild(guild):
    """Returns an instance of the named race class.
    Args:
        guild(str): case-insensitive name of Guild to load
    Returns:
        (guild): instance of the appropriate subclass of `Guild`
    """

    guild = guild.strip().capitalize()

    if guild in all_guilds:
        return globals()[guild]()
    else:
        raise GuildException("Invalid guild specified.")


def apply_guild(character, guild):
    """Causes a Character to "have" a named guild.
    Args: 
        character: the character object having a guild
        guild (str, guild): the name of the guild to apply
    """
    if isinstance(guild, Guild):
        guild = guild.name

    guild = load_guild(guild)

    character.db.guild = guild.name
    character.message('You join the {} guild.'.format(guild.name))
    message = "%s shouts \"%s\"" % (self.caller.name, self.args)
    SESSIONS.announce_all(message)


class Guild(object):
    """Base guild class containing default values for all traits."""

    def __init__(self, character):
        self.name = None
        self.skills = {}
        self.health_roll = None


class Peon(Guild):
    def __init__(self, character):
        super(Peon, self).__init__(character)
        self.name = 'Peon'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        character.cmdset.add(ResourceCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = G_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = G_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = G_WSAVE[character.traits.LVL.actual]


class Peasant(Guild):
    def __init__(self, character):
        super(Peasant, self).__init__(character)
        self.name = 'Peasant'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        character.cmdset.add(ResourceCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = G_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = G_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = G_WSAVE[character.traits.LVL.actual]


class Slave(Guild):
    def __init__(self, character):
        super(Slave, self).__init__(character)
        self.name = 'Slave'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        character.cmdset.add(ResourceCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.LVL.actual = 10
        character.traits.HP.base += roll_max(self.health_roll) * character.traits.LVL.actual
        character.traits.SP.base += (character.traits.INT.actual + character.traits.WIS.actual / 2) \
                                    * character.traits.LVL.actual
        character.traits.MAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = G_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = G_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = G_WSAVE[character.traits.LVL.actual]


class Servant(Guild):
    def __init__(self, character):
        super(Servant, self).__init__(character)
        self.name = 'Servant'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        character.cmdset.add(ResourceCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.LVL.actual = 10
        character.traits.HP.base += roll_max(self.health_roll) * character.traits.LVL.actual
        character.traits.SP.base += (character.traits.INT.actual + character.traits.WIS.actual / 2) \
                                    * character.traits.LVL.actual
        character.traits.MAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = G_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = G_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = G_WSAVE[character.traits.LVL.actual]


class Conscript(Guild):
    def __init__(self, character):
        super(Conscript, self).__init__(character)
        self.name = 'Conscript'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        character.cmdset.add(ResourceCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.LVL.actual = 10
        character.traits.HP.base += roll_max(self.health_roll) * character.traits.LVL.actual
        character.traits.SP.base += (character.traits.INT.actual + character.traits.WIS.actual / 2) \
                                    * character.traits.LVL.actual
        character.traits.MAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = G_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = G_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = G_WSAVE[character.traits.LVL.actual]


class Commoner(Guild):
    def __init__(self, character):
        super(Commoner, self).__init__(character)
        self.name = 'Commoner'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        character.cmdset.add(ResourceCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = G_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = G_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = G_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = G_WSAVE[character.traits.LVL.actual]


# Universal Guilds
class Cleric(Guild):
    def __init__(self, character):
        super(Cleric, self).__init__(character)
        self.name = 'Cleric of Helotyr'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'SCR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Scrolls'},
            'DIV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Divine Magic'},
            'FAI': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Faith'},
            'PRE': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Preach'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d10'
        character.db.faith = "Helotyr"
        character.db.devotion = "Cleric"
        character.cmdset.add(helotyr.LightCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = C_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = C_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = C_WSAVE[character.traits.LVL.actual]


class SarthoarCleric(Guild):
    def __init__(self, character):
        super(SarthoarCleric, self).__init__(character)
        self.name = 'Cleric of Sarthoar'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'SCR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Scrolls'},
            'INF': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Infernal Magic'},
            'FAI': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Faith'},
            'PRE': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Preach'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d10'
        character.db.faith = "Sarthoar"
        character.db.devotion = "Cleric"
        character.cmdset.add(sarthoar.SarthCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = C_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = C_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = C_WSAVE[character.traits.LVL.actual]


class Druid(Guild):
    def __init__(self, character):
        super(Druid, self).__init__(character)
        self.name = 'Druid of Aphrea'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'SCR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Scrolls'},
            'NAT': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Nature Magic'},
            'FAI': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Faith'},
            'PRE': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Preach'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d10'
        character.db.faith = "Aphrea"
        character.db.devotion = "Cleric"
        character.cmdset.add(druid.DruidCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = C_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = C_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = C_WSAVE[character.traits.LVL.actual]


class Templar(Guild):
    def __init__(self, character):
        super(Templar, self).__init__(character)
        self.name = 'Templar'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'DIV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Divine Magic'},
            'FAI': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Faith'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armor'},
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d10'
        character.db.faith = ""
        character.db.devotion = "Paladin"
        character.cmdset.add(templar.LightCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = C_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = C_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = C_WSAVE[character.traits.LVL.actual]


class Harbinger(Guild):
    def __init__(self, character):
        super(Harbinger, self).__init__(character)
        self.name = 'Harbinger'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'INF': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Infernal Magic'},
            'FAI': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Faith'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armor'},
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d10'
        character.db.faith = "Sarthoar"
        character.db.devotion = "Paladin"
        character.cmdset.add(harbinger.DarkCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = C_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = C_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = C_WSAVE[character.traits.LVL.actual]


class Ranger(Guild):
    def __init__(self, character):
        super(Ranger, self).__init__(character)
        self.name = 'Ranger'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'NAT': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Nature Magic'},
            'FAI': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Faith'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armor'},
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d10'
        character.db.faith = "Aphrea"
        character.db.devotion = "Paladin"
        character.cmdset.add(ranger.RangCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = C_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = C_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = C_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = C_WSAVE[character.traits.LVL.actual]


# Kingdom Guilds
class Fighter(Guild):
    def __init__(self, character):
        super(Fighter, self).__init__(character)
        self.name = 'Fighter'
        self.skills = {
            'DOD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Dodge'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'LDR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Leadership'},
            'SHD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Shields'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armor'},
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d12'
        character.cmdset.add(fighter.FightCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = F_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = F_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = F_WSAVE[character.traits.LVL.actual]


class Mage(Guild):
    def __init__(self, character):
        super(Mage, self).__init__(character)
        self.name = 'Mage'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'WND': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Wands'},
            'SCR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Scrolls'},
            'ELE': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Elemental Magic'},
            'WRD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Wards'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d6'
        character.cmdset.add(mage.MageCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = M_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = M_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = M_WSAVE[character.traits.LVL.actual]


class Merchant(Guild):
    def __init__(self, character):
        super(Merchant, self).__init__(character)
        self.name = 'Merchant'
        self.skills = {
            'REP': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Repair'},
            'FRG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Forge'},
            'LDR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Leadership'},
            'ORG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Organization'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'NEG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Negotiation'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d6'
        character.cmdset.add(merchant.MerchCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = T_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = T_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = T_WSAVE[character.traits.LVL.actual]


class Thief(Guild):
    def __init__(self, character):
        super(Thief, self).__init__(character)
        self.name = 'Thief'
        self.skills = {
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'DOD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Dodge'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armors'},
            'SNK': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Sneak'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
            'HID': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Hide'},
        }
        self.health_roll = '1d8'
        character.cmdset.add(thief.ThiefCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = R_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = R_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = R_WSAVE[character.traits.LVL.actual]


# Caliphate Guilds
class Warrior(Guild):
    def __init__(self, character):
        super(Warrior, self).__init__(character)
        self.name = 'Warrior'
        self.skills = {
            'DOD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Dodge'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'LDR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Leadership'},
            'SHD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Shields'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armor'},
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d12'
        character.cmdset.add(warrior.WarrCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = F_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = F_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = F_WSAVE[character.traits.LVL.actual]


class Sorcerer(Guild):
    def __init__(self, character):
        super(Sorcerer, self).__init__(character)
        self.name = 'Sorcerer'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'WND': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Wands'},
            'SCR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Scrolls'},
            'NEC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Necro Magic'},
            'WRD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Wards'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d6'
        character.cmdset.add(sorcerer.SorcCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = M_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = M_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = M_WSAVE[character.traits.LVL.actual]


class Trader(Guild):
    def __init__(self, character):
        super(Trader, self).__init__(character)
        self.name = 'Trader'
        self.skills = {
            'REP': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Repair'},
            'FRG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Forge'},
            'LDR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Leadership'},
            'ORG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Organization'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'NEG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Negotiation'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d6'
        character.cmdset.add(trader.TradeCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = T_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = T_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = T_WSAVE[character.traits.LVL.actual]


class Assassin(Guild):
    def __init__(self, character):
        super(Assassin, self).__init__(character)
        self.name = 'Assassin'
        self.skills = {
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'DOD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Dodge'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armors'},
            'SNK': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Sneak'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
            'HID': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Hide'},
        }
        self.health_roll = '1d8'
        character.cmdset.add(assassin.ASSNCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = R_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = R_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = R_WSAVE[character.traits.LVL.actual]


# Empire Guilds
class Samurai(Guild):
    def __init__(self, character):
        super(Samurai, self).__init__(character)
        self.name = 'Samurai'
        self.skills = {
            'DOD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Dodge'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'LDR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Leadership'},
            'SHD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Shields'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armor'},
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d12'
        character.cmdset.add(samurai.SamuCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = F_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = F_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = F_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = F_WSAVE[character.traits.LVL.actual]


class Shaman(Guild):
    def __init__(self, character):
        super(Shaman, self).__init__(character)
        self.name = 'Shaman'
        self.skills = {
            'SPC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spellcraft'},
            'WND': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Wands'},
            'SCR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Scrolls'},
            'SPI': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Spirit Magic'},
            'WRD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Wards'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d6'
        character.cmdset.add(shaman.ShamCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = M_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = M_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = M_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = M_WSAVE[character.traits.LVL.actual]


class Artisan(Guild):
    def __init__(self, character):
        super(Artisan, self).__init__(character)
        self.name = 'Artisan'
        self.skills = {
            'REP': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Repair'},
            'FRG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Forge'},
            'LDR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Leadership'},
            'ORG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Organization'},
            'KNO': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Knowledge'},
            'NEG': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Negotiation'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
        }
        self.health_roll = '1d6'
        character.cmdset.add(artisan.ArtCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = T_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = T_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = T_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = T_WSAVE[character.traits.LVL.actual]


class Monk(Guild):
    def __init__(self, character):
        super(Monk, self).__init__(character)
        self.name = 'Monk'
        self.skills = {
            'MAR': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Martial'},
            'DOD': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Dodge'},
            'WPN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Weapons'},
            'ARM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Armors'},
            'SNK': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Sneak'},
            'FOC': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Focus'},
            'DIS': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Discipline'},
            'HID': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Hide'},
        }
        self.health_roll = '1d8'
        character.cmdset.add(monk.MonkCmdSet, permanent=True)
        for key, kwargs in self.skills.items():
            character.skills.add(key, **kwargs)
            return
        character.traits.MAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.RAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.UAB.base = R_BAB[character.traits.LVL.actual]
        character.traits.FORT.base = R_FSAVE[character.traits.LVL.actual]
        character.traits.REFL.base = R_RSAVE[character.traits.LVL.actual]
        character.traits.WILL.base = R_WSAVE[character.traits.LVL.actual]
