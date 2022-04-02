"""
Primary module for guilds within Mercadia
"""
from evennia.server.sessionhandler import SESSIONS
from world.traitcalcs import abilitymodifiers
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

general_guilds = ("Peon", "Peasant", "Servant", "Slave", "Conscript", "Commoner")


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
    chp1 = roll_max(guild.health_roll)
    chp2 = abilitymodifiers[character.traits.CON.value]
    csp1 = roll_max('1d20')
    csp2 = (abilitymodifiers[traits.INT.value] + abilitymodifiers[traits.WIS.value])
    character.db.guild = guild.name
    character.cmdset.add(guild.cmd_set_add, permanent=True)
    character.traits.HP.base += (chp1 + chp2)
    character.traits.SP.base += (csp1 + csp2)
    character.db.faith = guild.faith
    character.db.devotion = guild.devotion
    character.traits.MAB.base = guild.bab[character.traits.LVL.value]
    character.traits.RAB.base = guild.bab[character.traits.LVL.value]
    character.traits.UAB.base = guild.bab[character.traits.LVL.value]
    character.traits.FORT.base = guild.fsave[character.traits.LVL.value]
    character.traits.REFL.base = guild.rsave[character.traits.LVL.value]
    character.traits.WILL.base = guild.wsave[character.traits.LVL.value]

    for key, kwargs in guild.skills.items():
        if character.traits.key:
            character.traits.key.base += 1
        else:
            character.traits.add(key, **kwargs)

    character.msg('You join the {} guild.'.format(guild.name))
    message = '{} joins the {} guild.'.format(character, guild.name)
    SESSIONS.announce_all(message)

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
        self.faith = None
        self.devotion = None
        self.bab = None
        self.fsave = None
        self.rsave = None
        self.wsave = None


class Peon(Guild):
    def __init__(self):
        super(Peon, self).__init__()
        self.name = 'Peon'
        self.skills = {
            'SRV': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Survey', 'trait_type': 'static'},
            'MIN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Mining', 'trait_type': 'static'},
            'FOR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Forestry', 'trait_type': 'static'},
            'SKN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Skinning', 'trait_type': 'static'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = G_BAB
        self.fsave = G_FSAVE
        self.rsave = G_RSAVE
        self.wsave = G_WSAVE


class Peasant(Guild):
    def __init__(self):
        super(Peasant, self).__init__()
        self.name = 'Peasant'
        self.skills = {
            'SRV': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Survey', 'trait_type': 'static'},
            'MIN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Mining', 'trait_type': 'static'},
            'FOR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Forestry', 'trait_type': 'static'},
            'SKN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Skinning', 'trait_type': 'static'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = G_BAB
        self.fsave = G_FSAVE
        self.rsave = G_RSAVE
        self.wsave = G_WSAVE


class Slave(Guild):
    def __init__(self):
        super(Slave, self).__init__()
        self.name = 'Slave'
        self.skills = {
            'SRV': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Survey', 'trait_type': 'static'},
            'MIN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Mining', 'trait_type': 'static'},
            'FOR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Forestry', 'trait_type': 'static'},
            'SKN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Skinning', 'trait_type': 'static'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = G_BAB
        self.fsave = G_FSAVE
        self.rsave = G_RSAVE
        self.wsave = G_WSAVE


class Servant(Guild):
    def __init__(self):
        super(Servant, self).__init__()
        self.name = 'Servant'
        self.skills = {
            'SRV': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Survey', 'trait_type': 'static'},
            'MIN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Mining', 'trait_type': 'static'},
            'FOR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Forestry', 'trait_type': 'static'},
            'SKN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Skinning', 'trait_type': 'static'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = G_BAB
        self.fsave = G_FSAVE
        self.rsave = G_RSAVE
        self.wsave = G_WSAVE


class Conscript(Guild):
    def __init__(self):
        super(Conscript, self).__init__()
        self.name = 'Conscript'
        self.skills = {
            'SRV': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Survey', 'trait_type': 'static'},
            'MIN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Mining', 'trait_type': 'static'},
            'FOR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Forestry', 'trait_type': 'static'},
            'SKN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Skinning', 'trait_type': 'static'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = G_BAB
        self.fsave = G_FSAVE
        self.rsave = G_RSAVE
        self.wsave = G_WSAVE


class Commoner(Guild):
    def __init__(self):
        super(Commoner, self).__init__()
        self.name = 'Commoner'
        self.skills = {
            'SRV': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Survey', 'trait_type': 'static'},
            'MIN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Mining', 'trait_type': 'static'},
            'FOR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Forestry', 'trait_type': 'static'},
            'SKN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Skinning', 'trait_type': 'static'}}
        self.health_roll = '1d4'
        self.cmd_set_add = ResourceCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = G_BAB
        self.fsave = G_FSAVE
        self.rsave = G_RSAVE
        self.wsave = G_WSAVE


# Universal Guilds
class Cleric(Guild):
    def __init__(self):
        super(Cleric, self).__init__()
        self.name = 'Helotyr Cleric'
        self.skills = {
            'SPC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spellcraft', 'trait_type': 'static'},
            'SCR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Scrolls', 'trait_type': 'static'},
            'DIV': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Divne Magic', 'trait_type': 'static'},
            'FTH': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Faith', 'trait_type': 'static'},
            'PRE': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Preach', 'trait_type': 'static'},
            'KNW': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Knowledge', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d10'
        self.faith = "Helotyr"
        self.devotion = "Cleric"
        self.cmd_set_add = helotyr.ClericCmdSet
        self.bab = C_BAB
        self.fsave = C_FSAVE
        self.rsave = C_RSAVE
        self.wsave = C_WSAVE


class SarthoarCleric(Guild):
    def __init__(self):
        super(SarthoarCleric, self).__init__()
        self.name = 'Sarthoar Cleric'
        self.skills = {
            'SPC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spellcraft', 'trait_type': 'static'},
            'SCR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Scrolls', 'trait_type': 'static'},
            'INF': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Infernal Magic', 'trait_type': 'static'},
            'FTH': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Faith', 'trait_type': 'static'},
            'PRE': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Preach', 'trait_type': 'static'},
            'KNW': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Knowledge', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d10'
        self.faith = "Sarthoar"
        self.devotion = "Cleric"
        self.cmd_set_add = sarthoar.SarthoarCmdSet
        self.bab = C_BAB
        self.fsave = C_FSAVE
        self.rsave = C_RSAVE
        self.wsave = C_WSAVE


class Druid(Guild):
    def __init__(self):
        super(Druid, self).__init__()
        self.name = 'Druid of Aphrea'
        self.skills = {
            'SPC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spellcraft', 'trait_type': 'static'},
            'SCR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Scrolls', 'trait_type': 'static'},
            'NTR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Nature Magic', 'trait_type': 'static'},
            'FTH': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Faith', 'trait_type': 'static'},
            'PRE': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Preach', 'trait_type': 'static'},
            'KNW': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Knowledge', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d10'
        self.faith = "Aphrea"
        self.devotion = "Cleric"
        self.cmd_set_add = druid.DruidCmdSet
        self.bab = C_BAB
        self.fsave = C_FSAVE
        self.rsave = C_RSAVE
        self.wsave = C_WSAVE


class Templar(Guild):
    def __init__(self):
        super(Templar, self).__init__()
        self.name = 'Templar'
        self.skills = {
            'SPC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spellcraft', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'DIV': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Divne Magic', 'trait_type': 'static'},
            'FTH': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Faith', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armor', 'trait_type': 'static'},
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d10'
        self.faith = "Helotyr"
        self.devotion = "Paladin"
        self.cmd_set_add = templar.TemplarCmdSet
        self.bab = F_BAB
        self.fsave = C_FSAVE
        self.rsave = C_RSAVE
        self.wsave = C_WSAVE


class Harbinger(Guild):
    def __init__(self):
        super(Harbinger, self).__init__()
        self.name = 'Harbinger'
        self.skills = {
            'SPC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spellcraft', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'INF': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Infernal Magic', 'trait_type': 'static'},
            'FTH': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Faith', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armor', 'trait_type': 'static'},
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d10'
        self.faith = "Sarthoar"
        self.devotion = "Paladin"
        self.cmd_set_add = harbinger.HarbingerCmdSet
        self.bab = F_BAB
        self.fsave = C_FSAVE
        self.rsave = C_RSAVE
        self.wsave = C_WSAVE


class Ranger(Guild):
    def __init__(self):
        super(Ranger, self).__init__()
        self.name = 'Ranger'
        self.skills = {
            'SPC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spellcraft', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'NTR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Nature Magic', 'trait_type': 'static'},
            'FTH': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Faith', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armor', 'trait_type': 'static'},
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d10'
        self.faith = "Aphrea"
        self.devotion = "Paladin"
        self.cmd_set_add = ranger.RangerCmdSet
        self.bab = F_BAB
        self.fsave = C_FSAVE
        self.rsave = C_RSAVE
        self.wsave = C_WSAVE


# Kingdom Guilds
class Fighter(Guild):
    def __init__(self):
        super(Fighter, self).__init__()
        self.name = 'Fighter'
        self.skills = {
            'DOD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Dodge', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'LDR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Leadership', 'trait_type': 'static'},
            'SHD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Shields', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armor', 'trait_type': 'static'},
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d12'
        self.cmd_set_add = fighter.FighterCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = F_BAB
        self.fsave = F_FSAVE
        self.rsave = F_RSAVE
        self.wsave = F_WSAVE


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
        self.faith = ""
        self.devotion = ""
        self.bab = M_BAB
        self.fsave = M_FSAVE
        self.rsave = M_RSAVE
        self.wsave = M_WSAVE


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
        self.faith = ""
        self.devotion = ""
        self.bab = T_BAB
        self.fsave = T_FSAVE
        self.rsave = T_RSAVE
        self.wsave = T_WSAVE


class Thief(Guild):
    def __init__(self):
        super(Thief, self).__init__()
        self.name = 'Thief'
        self.skills = {
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'DOD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Dodge', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armors', 'trait_type': 'static'},
            'SNK': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Sneak', 'trait_type': 'static'},
            'HID': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Hide', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d8'
        self.cmd_set_add = thief.ThiefCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = R_BAB
        self.fsave = R_FSAVE
        self.rsave = R_RSAVE
        self.wsave = R_WSAVE


# Caliphate Guilds
class Warrior(Guild):
    def __init__(self):
        super(Warrior, self).__init__()
        self.name = 'Warrior'
        self.skills = {
            'DOD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Dodge', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'LDR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Leadership', 'trait_type': 'static'},
            'SHD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Shields', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armor', 'trait_type': 'static'},
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d12'
        self.cmd_set_add = warrior.WarriorCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = F_BAB
        self.fsave = F_FSAVE
        self.rsave = F_RSAVE
        self.wsave = F_WSAVE


class Sorcerer(Guild):
    def __init__(self):
        super(Sorcerer, self).__init__()
        self.name = 'Sorcerer'
        self.skills = {
            'SPC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spellcraft', 'trait_type': 'static'},
            'WND': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Wands', 'trait_type': 'static'},
            'SCR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Scrolls', 'trait_type': 'static'},
            'NEC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Necromancy Magic', 'trait_type': 'static'},
            'WRD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Wards', 'trait_type': 'static'},
            'KNW': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Knowledge', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d6'
        self.cmd_set_add = sorcerer.SorcererCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = M_BAB
        self.fsave = M_FSAVE
        self.rsave = M_RSAVE
        self.wsave = M_WSAVE


class Trader(Guild):
    def __init__(self):
        super(Trader, self).__init__()
        self.name = 'Trader'
        self.skills = {
            'REP': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Repair', 'trait_type': 'static'},
            'FRG': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Forge', 'trait_type': 'static'},
            'LDR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Leadersip', 'trait_type': 'static'},
            'ORG': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Organization', 'trait_type': 'static'},
            'NEG': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Negotiation', 'trait_type': 'static'},
            'KNW': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Knowledge', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d6'
        self.cmd_set_add = trader.TraderCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = T_BAB
        self.fsave = T_FSAVE
        self.rsave = T_RSAVE
        self.wsave = T_WSAVE


class Assassin(Guild):
    def __init__(self):
        super(Assassin, self).__init__()
        self.name = 'Assassin'
        self.skills = {
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'DOD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Dodge', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armors', 'trait_type': 'static'},
            'SNK': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Sneak', 'trait_type': 'static'},
            'HID': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Hide', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d8'
        self.cmd_set_add = assassin.AssassinCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = R_BAB
        self.fsave = R_FSAVE
        self.rsave = R_RSAVE
        self.wsave = R_WSAVE


# Empire Guilds
class Samurai(Guild):
    def __init__(self):
        super(Samurai, self).__init__()
        self.name = 'Samurai'
        self.skills = {
            'DOD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Dodge', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'LDR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Leadership', 'trait_type': 'static'},
            'SHD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Shields', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armor', 'trait_type': 'static'},
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d12'
        self.cmd_set_add = samurai.SamuraiCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = F_BAB
        self.fsave = F_FSAVE
        self.rsave = F_RSAVE
        self.wsave = F_WSAVE


class Shaman(Guild):
    def __init__(self):
        super(Shaman, self).__init__()
        self.name = 'Shaman'
        self.skills = {
            'SPC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spellcraft', 'trait_type': 'static'},
            'WND': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Wands', 'trait_type': 'static'},
            'SCR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Scrolls', 'trait_type': 'static'},
            'SPI': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Spirit Magic', 'trait_type': 'static'},
            'WRD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Wards', 'trait_type': 'static'},
            'KNW': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Knowledge', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d6'
        self.cmd_set_add = shaman.ShamanCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = M_BAB
        self.fsave = M_FSAVE
        self.rsave = M_RSAVE
        self.wsave = M_WSAVE


class Artisan(Guild):
    def __init__(self):
        super(Artisan, self).__init__()
        self.name = 'Artisan'
        self.skills = {
            'REP': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Repair', 'trait_type': 'static'},
            'FRG': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Forge', 'trait_type': 'static'},
            'LDR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Leadersip', 'trait_type': 'static'},
            'ORG': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Organization', 'trait_type': 'static'},
            'NEG': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Negotiation', 'trait_type': 'static'},
            'KNW': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Knowledge', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d6'
        self.cmd_set_add = artisan.ArtisanCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = T_BAB
        self.fsave = T_FSAVE
        self.rsave = T_RSAVE
        self.wsave = T_WSAVE


class Monk(Guild):
    def __init__(self):
        super(Monk, self).__init__()
        self.name = 'Monk'
        self.skills = {
            'MAR': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Martial', 'trait_type': 'static'},
            'DOD': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Dodge', 'trait_type': 'static'},
            'WPN': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Weapons', 'trait_type': 'static'},
            'ARM': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Armors', 'trait_type': 'static'},
            'SNK': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Sneak', 'trait_type': 'static'},
            'HID': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Hide', 'trait_type': 'static'},
            'FOC': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Focus', 'trait_type': 'static'},
            'DIS': {'base': 1, 'mod': 0, 'mult': 1, 'name': 'Discipline', 'trait_type': 'static'},
        }
        self.health_roll = '1d8'
        self.cmd_set_add = monk.MonkCmdSet
        self.faith = ""
        self.devotion = ""
        self.bab = R_BAB
        self.fsave = R_FSAVE
        self.rsave = R_RSAVE
        self.wsave = R_WSAVE
