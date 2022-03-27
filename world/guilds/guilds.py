"""
Primary module for guilds within Mercadia
"""

from evennia.server.sessionhandler import SESSIONS
from world.rulebook import roll_max
from evennia.utils import fill
from evennia import Command, CmdSet
from typeclasses.resources import ResourceCmdSet
from typeclasses.readable import Readable
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

martial_guilds = ("Fighter", "Warrior", "Samurai")
divine_guilds = ("Cleric", "SarthoarCleric", "Druid")
agile_guilds = ("Thief", "Assassin", "Monk")
trades_guilds = ("Merchant", "Artisan", "Trader")
arcane_guilds = ("Mage", "Sorcerer", "Shaman")
general_guilds = ("Peon", "Peasant", "Servant", "Slave", "Conscript", "Commoner")
hybrid_guilds = ("Templar", "Ranger", "Harbinger")


class GuildSign(Readable):
    """
    This simple object defines some attributes and
    """

    def at_object_creation(self):
        """
        Called when object is created. We make sure to set the needed
        Attribute.
        """
        super(GuildSign, self).at_object_creation()
        self.db.guild = ""
        # define a command on the object.
        self.cmdset.add(JoinGuildCmdSet, permanent=True)


class JoinGuildCmdSet(CmdSet):
    """
    This cmdset is used in character generation areas.
    """

    key = "JoinGuild"

    def at_cmdset_creation(self):
        """this is called at initialization"""
        self.add(CmdGuildJoin())


class CmdGuildJoin(Command):
    """This is the command string that will assign a Guild onto a character,
     and the cooresponding command set."""

    key = "join"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        guild = self.obj.db.guild.strip().lower()
        tr = caller.traits

        if caller.db.guild is None:
            caller.msg("Something went wrong in character creation. please contact an Admin!")
            return
        elif caller.db.guild not in general_guilds:
            caller.msg("You are already a member of an adventuring guild. You must first leave your old guild first.")
            return
        else:
            answer = yield "Are you sure you want to join this guild? All experience will be reset and you will lose " \
                           "all currency in your bank and wallet. "
            if answer not in ('yes', 'y', 'no', 'n'):
                answer = yield "please answer Yes or No"
            if answer.strip().lower() in ("yes", "y"):
                tr.XP.base = 0
                caller.db.wallet = 0
                caller.db.bank = 0
                apply_guild(caller, guild)
                initial_stats(caller)

            else:
                caller.msg("Need message here")


class GuildException(Exception):
    """Base exception class for races module."""

    def __init__(self, msg):
        self.msg = msg


def load_guild(guild):
    """Returns an instance of the named guild class.
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
    character.cmdset.add(guild.cmd_set_add, permanent=True)

    character.msg('You join the {} guild.'.format(guild.name))
    message = '{} joins the {} guild.'.format(character, guild.name)
    SESSIONS.announce_all(message)

    for key, kwargs in guild.skills.items():
        character.skills.add(key, **kwargs)

    if guild in divine_guilds:
        character.db.faith = guild.faith
        character.db.devotion = guild.devotion


def initial_stats(character):
    guild = character.db.guild
    load_guild(guild)

    character.traits.HP.base += roll_max(guild.health_roll) * character.traits.LVL.actual
    character.traits.SP.base += (character.traits.INT.actual + character.traits.WIS.actual / 2) \
                                * character.traits.LVL.actual

    if guild in melee_guilds:
        bab = F_BAB
        fsave = F_FSAVE
        rsave = F_RSAVE
        wsave = F_WSAVE
    elif guild in divine_guilds:
        bab = C_BAB
        fsave = C_FSAVE
        rsave = C_RSAVE
        wsave = C_WSAVE
    elif guild in agile_guilds:
        bab = R_BAB
        fsave = R_FSAVE
        rsave = R_RSAVE
        wsave = R_WSAVE
    elif guild in arcane_guilds:
        bab = M_BAB
        fsave = M_FSAVE
        rsave = M_RSAVE
        wsave = M_WSAVE
    elif guild in trades_guilds:
        bab = T_BAB
        fsave = T_FSAVE
        rsave = T_RSAVE
        wsave = T_WSAVE
    elif guild in general_guilds:
        bab = G_BAB
        fsave = G_FSAVE
        rsave = G_RSAVE
        wsave = G_WSAVE

    character.traits.MAB.base = bab[character.traits.LVL.actual]
    character.traits.RAB.base = bab[character.traits.LVL.actual]
    character.traits.UAB.base = bab[character.traits.LVL.actual]
    character.traits.FORT.base = fsave[character.traits.LVL.actual]
    character.traits.REFL.base = rsave[character.traits.LVL.actual]
    character.traits.WILL.base = wsave[character.traits.LVL.actual]


"""
def level_up():
    pass
"""


class Guild(object):
    """Base guild class containing default values for all traits."""

    def __init__(self):
        self.name = None
        self.skills = {}
        self.health_roll = None
        self.cmd_set_add = None


class Peon(Guild):
    def __init__(self):
        super(Peon, self).__init__()
        self.name = 'Peon'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet


#        for key, kwargs in self.skills.items():
#            character.skills.add(key, **kwargs)
#            return


class Peasant(Guild):
    def __init__(self):
        super(Peasant, self).__init__()
        self.name = 'Peasant'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Slave(Guild):
    def __init__(self):
        super(Slave, self).__init__()
        self.name = 'Slave'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Servant(Guild):
    def __init__(self):
        super(Servant, self).__init__()
        self.name = 'Servant'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Conscript(Guild):
    def __init__(self):
        super(Conscript, self).__init__()
        self.name = 'Conscript'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Commoner(Guild):
    def __init__(self):
        super(Commoner, self).__init__()
        self.name = 'Commoner'
        self.skills = {
            'SRV': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Survey'},
            'MIN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Mining'},
            'LUM': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Lumbering'},
            'SKN': {'type': 'static', 'base': 1, 'mod': 0, 'name': 'Skinning'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


# Universal Guilds
class Cleric(Guild):
    def __init__(self):
        super(Cleric, self).__init__()
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
        self.faith = "Helotyr"
        self.devotion = "Cleric"
        self.cmd_set_add = helotyr.ClericCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class SarthoarCleric(Guild):
    def __init__(self):
        super(SarthoarCleric, self).__init__()
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
        self.faith = "Sarthoar"
        self.devotion = "Cleric"
        self.cmd_set_add = sarthoar.SarthoarCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Druid(Guild):
    def __init__(self):
        super(Druid, self).__init__()
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
        self.faith = "Aphrea"
        self.devotion = "Cleric"
        self.cmd_set_add = druid.DruidCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Templar(Guild):
    def __init__(self):
        super(Templar, self).__init__()
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
        self.faith = ""
        self.devotion = "Paladin"
        self.cmd_set_add = templar.TemplarCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Harbinger(Guild):
    def __init__(self):
        super(Harbinger, self).__init__()
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
        self.faith = "Sarthoar"
        self.devotion = "Paladin"
        self.cmd_set_add = harbinger.HarbingerCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Ranger(Guild):
    def __init__(self):
        super(Ranger, self).__init__()
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
        self.faith = "Aphrea"
        self.devotion = "Paladin"
        self.cmd_set_add = ranger.RangerCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


# Kingdom Guilds
class Fighter(Guild):
    def __init__(self):
        super(Fighter, self).__init__()
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
        self.cmd_set_add = fighter.FighterCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Mage(Guild):
    def __init__(self):
        super(Mage, self).__init__()
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
        self.cmd_set_add = mage.MageCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Merchant(Guild):
    def __init__(self):
        super(Merchant, self).__init__()
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
        self.cmd_set_add = merchant.MerchantCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Thief(Guild):
    def __init__(self):
        super(Thief, self).__init__()
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
        self.cmd_set_add = thief.ThiefCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


# Caliphate Guilds
class Warrior(Guild):
    def __init__(self):
        super(Warrior, self).__init__()
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
        self.cmd_set_add = warrior.WarriorCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Sorcerer(Guild):
    def __init__(self):
        super(Sorcerer, self).__init__()
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
        self.cmd_set_add = sorcerer.SorcererCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Trader(Guild):
    def __init__(self):
        super(Trader, self).__init__()
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
        self.cmd_set_add = trader.TraderCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Assassin(Guild):
    def __init__(self):
        super(Assassin, self).__init__()
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
        self.cmd_set_add = assassin.AssassinCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


# Empire Guilds
class Samurai(Guild):
    def __init__(self):
        super(Samurai, self).__init__()
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
        self.cmd_set_add = samurai.SamuraiCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Shaman(Guild):
    def __init__(self):
        super(Shaman, self).__init__()
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
        self.cmd_set_add = shaman.ShamanCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Artisan(Guild):
    def __init__(self):
        super(Artisan, self).__init__()
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
        self.cmd_set_add = artisan.ArtisanCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return


class Monk(Guild):
    def __init__(self):
        super(Monk, self).__init__()
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
        self.cmd_set_add = monk.MonkCmdSet
        #        for key, kwargs in self.skills.items():
        #            character.skills.add(key, **kwargs)
        #            return
