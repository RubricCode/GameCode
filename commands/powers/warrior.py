import time
from math import floor
from evennia import create_object, utils, CmdSet, create_script
from commands.command import MuxCommand
from commands import power
from random import randint
from evennia.utils.evform import EvForm
from world.rulebook import d_roll
from evennia.prototypes.spawner import spawn


class WarriorCmdSet(CmdSet):
    """
    This stores the input command
    """
    key = "commands"

    def at_cmdset_creation(self):
        """called once at creation"""
        self.add(power.CmdPower())