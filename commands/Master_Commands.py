import time
from math import floor
from evennia import create_object, utils, CmdSet, create_script
from commands.command import MuxCommand
from commands import power


class CmdDismiss(MuxCommand):
    """
     Command Name:Expel
         Syntax: Expel <target>
    Skills used: none

    Description:

    A command to dismiss a member from your guild permanently.
    this command should only be used under the most dire of circumstances.
    Abuse will not be tolerated.

    """

    key = "expel"
    locks = "cmd:attr(title,master) or attr(title,assistant)"
    help_category = ""

    def func(self):
        caller = self.caller
        arg = self.args.strip().lower()
        target = self.caller.search(self.args)

        if caller.db.guild != target.db.guild:
            caller.msg("%s is not a member of your guild." % arg)
            return

        target.db.guild = "serf"
        target.cmdset.remove(bgpowers.UrchinCmdSet)
        caller.msg("You have dismissed %s from your guild ." % target)


class CmdExile(MuxCommand):
    """
     Command Name:Expel
         Syntax: Expel <target>
    Skills used: none

    Description:

    A command to dismiss a member from your guild permanently.
    this command should only be used under the most dire of circumstances.
    Abuse will not be tolerated.

    """

    key = "expel"
    locks = "cmd:attr(title,master) or attr(title,assistant)"
    help_category = ""

    def func(self):
        caller = self.caller
        arg = self.args.strip().lower()
        target = self.caller.search(self.args)

        if caller.db.guild != target.db.guild:
            caller.msg("%s is not a member of your guild." % arg)
            return

        target.db.guild = "serf"
        target.cmdset.remove(bgpowers.UrchinCmdSet)
        caller.msg("You have dismissed %s from your guild ." % target)


class CmdQuietMind(MuxCommand):
    """
     Command Name:Expel
         Syntax: Expel <target>
    Skills used: none

    Description:

    A command to dismiss a member from your guild permanently.
    this command should only be used under the most dire of circumstances.
    Abuse will not be tolerated.

    """

    key = "expel"
    locks = "cmd:attr(title,master) or attr(title,assistant)"
    help_category = ""

    def func(self):
        caller = self.caller
        arg = self.args.strip().lower()
        target = self.caller.search(self.args)

        if caller.db.guild != target.db.guild:
            caller.msg("%s is not a member of your guild." % arg)
            return

        target.db.guild = "serf"
        target.cmdset.remove(bgpowers.UrchinCmdSet)
        caller.msg("You have dismissed %s from your guild ." % target)


class CmdPromote(MuxCommand):
    """
     Command Name:Expel
         Syntax: Expel <target>
    Skills used: none

    Description:

    A command to dismiss a member from your guild permanently.
    this command should only be used under the most dire of circumstances.
    Abuse will not be tolerated.

    """

    key = "expel"
    locks = "cmd:attr(title,master) or attr(title,assistant)"
    help_category = ""

    def func(self):
        caller = self.caller
        arg = self.args.strip().lower()
        target = self.caller.search(self.args)

        if caller.db.guild != target.db.guild:
            caller.msg("%s is not a member of your guild." % arg)
            return

        target.db.guild = "serf"
        target.cmdset.remove(bgpowers.UrchinCmdSet)
        caller.msg("You have dismissed %s from your guild ." % target)


class CmdDemote(MuxCommand):
    """
     Command Name:Expel
         Syntax: Expel <target>
    Skills used: none

    Description:

    A command to dismiss a member from your guild permanently.
    this command should only be used under the most dire of circumstances.
    Abuse will not be tolerated.

    """

    key = "expel"
    locks = "cmd:attr(title,master) or attr(title,assistant)"
    help_category = ""

    def func(self):
        caller = self.caller
        arg = self.args.strip().lower()
        target = self.caller.search(self.args)

        if caller.db.guild != target.db.guild:
            caller.msg("%s is not a member of your guild." % arg)
            return

        target.db.guild = "serf"
        target.cmdset.remove(bgpowers.UrchinCmdSet)
        caller.msg("You have dismissed %s from your guild ." % target)
