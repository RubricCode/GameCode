"""
Character trait-related commands
"""
from world import rulebook
from commands.command import MuxCommand
from evennia import CmdSet
from evennia.utils.evform import EvForm


class CharTraitCmdSet(CmdSet):
    key = "chartrait_cmdset"
    priority = 1

    def at_cmdset_creation(self):
        """Populate CmdSet"""
        self.add(CmdSheet())
        self.add(CmdWealth())
        self.add(CmdVitals())
        self.add(CmdLevel())


class CmdSheet(MuxCommand):
    """
    view character status
    Usage:
      sheet

    """
    key = "sheet"
    aliases = ["sh"]
    locks = "cmd:all()"

    def func(self):
        """
        Handle displaying status.
        """
        # make sure the char has traits - only possible for superuser
        if len(self.caller.traits.all) == 0:
            return

        form = EvForm('commands.templates.charsheet', align='l')
        tr = self.caller.traits
        fields = {
            'A': self.caller.name,
            'B': self.caller.db.race,
            'C': self.caller.db.gender,
            'D': self.caller.db.guild,
            'E': self.caller.db.clan,
            'F': self.caller.db.title,
            'G': tr.LVL.actual,
            'H': self.caller.db.faith,
            'I': self.caller.db.devotion,
            'J': self.caller.db.nation,
            'K': self.caller.db.background,
            'L': tr.STR.actual,
            'M': tr.DEX.actual,
            'N': tr.CON.actual,
            'O': tr.INT.actual,
            'P': tr.WIS.actual,
            'Q': tr.CHA.actual,
            'R': tr.XP.actual,
            'S': tr.ENC.actual,
            'T': tr.ENC.max,
            'U': tr.HP.actual,
            'V': tr.HP.max,
            'W': tr.SP.actual,
            'X': tr.SP.max,
            'Y': tr.EP.actual,
            'Z': tr.EP.max,
        }
        form.map({k: self._format_trait_val(v) for k, v in fields.items()})

        self.caller.msg(form)

    def _format_trait_val(self, val):
        """Format trait values as bright white."""
        return "|w{}|n".format(val)


class CmdWealth(MuxCommand):
    """
    view character skills
    Usage:
      wealth
    Displays the Total wealth of your character.
    """
    key = "wealth"
    aliases = ["wea", "we"]
    locks = "cmd:all()"
    arg_regex = r"\s.+|"

    def func(self):
        bank = self.caller.db.bank
        wallet = self.caller.db.wallet
        wealth_message = """
Your money in Royals:
Bank Wealth    : {bank}
Carried Wealth : {wallet}
Total Wealth   : {total} """.format(
            bank="\n\t  ".join([str(bank)]),
            wallet="\n\t  ".join([str(wallet)]),
            total="\n\t  ".join([str(bank + wallet)]))
        self.caller.msg(wealth_message)


class CmdVitals(MuxCommand):
    """
    view the characters current and actual health, spellpower and endurance traits
    Usage:
      vitals
    Displays the characters vital traits
    """
    key = "vitals"
    aliases = ["vp", "hp"]
    locks = "cmd:all()"

    def func(self):
        tr = self.caller.traits
        self.caller.msg("|CHP: %s/%s SP: %s/%s EP: %s/%s" % (tr.HP.actual, tr.HP.max, tr.SP.actual,
                                                             tr.SP.max, tr.EP.actual, tr.EP.max))


class CmdLevel(MuxCommand):
    """
    view the experience points and coin amount required to advance to the next level
    Usage: 
      Level
    Displays the requirements for advancing to the next level
    """

    key = 'level'
    aliases = ['lvl', 'lv']
    locks = 'cmd:all()'

    def func(self):
        bank = self.caller.db.bank
        wallet = self.caller.db.wallet
        total = bank + wallet
        tr = self.caller.traits
        lvl = str(tr.LVL.actual + 1)
        xp1 = rulebook.LEVEL[lvl]['xp']
        coin1 = rulebook.LEVEL[lvl]['coins']
        xp2 = rulebook.LEVEL[lvl]['xp'] - tr.XP.actual
        coin2 = rulebook.LEVEL[lvl]['coins'] - total

        if xp2 <= 0 and coin2 <= 0:
            self.caller.msg("|yYou Are Ready To Advance!|/"
                            "|MLEVEL %s ADVANCEMENT|/"
                            "Advancement will cost %s Experience and %s coins|/"
                            "|CYou will need %s more Experience and %s more coins" % (lvl, xp1, coin1, xp2, coin2))
        else:
            self.caller.msg("|MLEVEL %s ADVANCEMENT|/"
                            "Advancement will cost %s Experience and %s coins|/"
                            "|CYou will need %s more Experience and %s more coins" % (lvl, xp1, coin1, xp2, coin2))
