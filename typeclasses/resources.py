"""
Resources are objects that are used in the creation of items within the game they come in the following forms:
  resource nodes; nodes that are harvestable to acquire raw resources through mining, lumbering, or skinning
    
    mining nodes come in two categories, surface deposits and mines:
       surface nodes have a small finite amount of harvestable metals and/or gems 
       mines  are deeper complex systems that follow viens and have a large amount of harvestable metals and/gems
    
    lumber nodes come in two categories, single trees and tree copses:
        single trees have a small finite amount of harvestable logs.
        copses have a large finite amount of harvestable logs and are rarer.
        
    skinning node are a special category
      Animals, produce a small amount of harvestable hide if successful 

"""


import time
from typeclasses.objects import Object
from random import randint
from commands.command import MuxCommand
from evennia.prototypes.spawner import spawn
from evennia import utils, CmdSet


class ResourceNode(Object):

    def at_object_creation(self):
        super(ResourceNode, self).at_object_creation()
        self.locks.add("get:false()")
        self.get_err_msg = None
        self.db.amt = randint(3,12)
        self.db.type = None
        self.db.proto = None


    def at_harvest(self):
        if self.db.amt > 0:
            spawn(self.db.proto)[0]
            self.db.amt -= 1
        else:
            self.delete()


class Resource(Object):
    def at_object_creation(self):
        super(Resource, self).at_object_creation()
        self.db.type = None
        self.db.hardness = None
        self.db.value = None
        self.db.weight = None


ARID = {}
TEMPERATE = {}
POLAR = {}
TROPICAL = {}
MEDITERRANEAN = {}
TUNDRA = {}


class CmdSurvey(MuxCommand):
    def func(self):
        caller = self.caller
        wilderness = caller.location.db.wilderness
        srv_last = caller.location.db.srv_last
        tr = self.caller.traits

        if not wilderness:
            caller.msg("You must be in the wilderness to use this command.")
            return

        if srv_last and time.time() - srv_last < 5 * 60:
            caller.msg("this area has been surveyed recently.")
            return

        caller.msg(" you begin to survey the area for any usable resources.")
        caller.location.msg_contents(
            "{actor} begins to survey the land for usable resources.",
            mapping=dict(actor=caller),
            exclude=caller)
        tr.SP.current -= 20
        caller.location.db.srv_last = time.time()
        utils.delay(10, callback= self.survey)

    def survey(self):
        caller = self.caller
        sk = caller.skills
        chance = randint(1, 100)
        success = 10 + sk.SRV.actual
        climate =  caller.location.db.climate

        if chance <= success:
            caller.msg("surveying the land you discover a")
            if "arid" in climate:
               spawn(ARID)
            if "mediterranean" in climate:
                spawn(MEDITERRANEAN)
            if "polar" in climate:
                spawn(POLAR)
            if "temperate" in climate:
                spawn(TEMPERATE)
            if "tropical" in climate:
                spawn(TROPICAL)
            if "tundra" in climate:
                spawn(TUNDRA)


class CmdMine(MuxCommand):
    def func(self):
        caller = self.caller
        tr = caller.traits
        last_mine = caller.db.last_mine
        tool = "Mining Pick"
        deposit = 0
        # search for target in our equip
        equipped_items = [i[1] for i in caller.equip if i[1]]
        obj = caller.search(
            args,
            candidates=equipped_items,
            nofound_string=_EQUIP_ERRMSG.format(args))

        if tool not in caller.equip.wield:
            caller.msg("You are not wielding the proper tool to mine.")
            return

        if not deposit in caller.location:
            caller.msg("there is no minable deposits present.")
            return

        if last_mine and time.time() - last_mine < 60:
            caller.msg("you may not mine that fast")
            return

        caller.msg("you begin to mine")
        caller.location.msg_contents(
            "{actor} begins to mine a deposit.",
            mapping=dict(actor=caller),
            exclude=caller)
        tr.SP.current -= 10
        caller.db.last_mine = time.time()


class CmdSkin(MuxCommand):
    def func(self):
        caller = self.caller
        tr = caller.traits
        last_skin = caller.db.last_skin
        tool = "Skinning Knife"

        if tool not in wield:
            caller.msg("You are not wielding the proper tool to mine.")
            return

        if not deposit in caller.location:
            caller.msg("there is no minable deposits present.")
            return

        if last_skin and time.time() - last_skin < 60:
            caller.msg("you may not mine that fast")
            return

        caller.msg("you begin to skin an animal")
        caller.location.msg_contents(
            "{actor} begins to skin an animal.",
            mapping=dict(actor=caller),
            exclude=caller)
        tr.SP.current -= 10
        caller.db.last_skin = time.time()


class CmdChop(MuxCommand):
    def func(self):
        caller = self.caller
        tr = caller.traits
        last_chop = caller.db.last_chop
        tool = "Lumber Axe"

        if tool not in wield:
            caller.msg("You are not wielding the proper tool to mine.")
            return

        if not deposit in caller.location:
            caller.msg("there is no minable deposits present.")
            return

        if last_chop and time.time() - last_chop < 60:
            caller.msg("you may not mine that fast")
            return

        caller.msg("you begin to chop a tree for lumber")
        caller.location.msg_contents(
            "{actor} begins to chop a tree for lumber.",
            mapping=dict(actor=caller),
            exclude=caller)
        tr.SP.current -= 10
        caller.db.last_chop = time.time()


class ResourceCmdSet(CmdSet):
    """
    This stores the input command
    """
    key = "General"

    def at_cmdset_creation(self):
        """called once at creation"""
        self.add(CmdSurvey())
        self.add(CmdMine())
        self.add(CmdSkin())
        self.add(CmdChop())