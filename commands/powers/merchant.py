import time
from evennia import create_object, utils, CmdSet, create_script
from world.contents.crafting.recipes import RECIPES
from world.contents.crafting.materials import MATERIALS
from commands.command import MuxCommand
from evennia.prototypes.spawner import spawn
from math import floor
from evennia import create_object, utils, CmdSet, create_script
from commands import power
from random import randint
from evennia.utils.evform import EvForm
from world.rulebook import d_roll


class MerchantCmdSet(CmdSet):
    """
    This stores the input command
    """
    key = "commands"

    def at_cmdset_creation(self):
        """called once at creation"""
        self.add(power.CmdPower())
        self.add(CmdForge())


empire_list = ()
caliphate_list = ()
kingdom_list = ()
weapon_list = ("battleaxe", "club", "dagger", "flail", "handaxe", "heavymace", "heavypick", "kama", "katana",
               "longsword", "lighthammer", "lightmace", "lightpick", "morningstar", "nageyari", "nunchaku", "rapier",
               "sai", "scimitar", "sickle", "spear", "shortspear", "shortsword", "tanto", "trident", "wakazashi",
               "warfan", "warhammer", "whip", "yari", "bastardsword", "dietsuchi", "falchion", "heavyflail", "glaive",
               "greataxe", "greatclub", "greatsword", "guisarme", "halberd", "kawanaga", "kusarigama", "lance",
               "longspear", "lucernehammer", "manrikigusari", "maul", "nagimaki", "naginata", "nodachi", "ono",
               "quarterstaff", "ransuer", "scythe", "tetsubo")

armor_list = ("robe", "paddedarmor", "leatherarmor", "studdedleather", "chainshirt", "hidearmor", "scalemail",
              "chainmail", "breastplate", "splintmail", "bandedmail", "halfplate", "fullplate", "leatherscale",
              "brigandine", "lamellar", "oyoroi", "ringmail", "helm", "shield", "gloves", "boots", "bracers", "belt")


class CmdForge(MuxCommand):
    """
    Spell Name: Forge
       SP Cost: 10
    Coins Cost: Varies depending on recipe
        Syntax: forge <material> <recipe>
   Skills used: forge, weapons, armor

   Description:

     A simple spell that allows a merchant/artisan/trader
   to create either weapons or armor from material components.

   """

    key = "forge"
    locks = "cmd:all()"
    help_category = "commands"

    def func(self):
        args = self.args
        caller = self.caller
        self.recipe = ""
        self.material = ""

        if not args:
            caller.msg("Forge What?")
            return

        if " " in args:
            self.material, self.recipe = self.args.split(" ", 1)

        if self.material not in MATERIALS.keys():
            caller.msg("That is not a valid crafting material.")
            return

        if self.recipe not in RECIPES.keys():
            caller.msg("That is not a valid recipe.")
            return

        item_name = "%s %s" % (self.material.capitalize(), RECIPES.get(self.recipe).get("key"))
        item_aliases = RECIPES.get(self.recipe).get("aliases")
        item_typeclass = RECIPES.get(self.recipe).get("typeclass")
        item_desc = RECIPES.get(self.recipe).get("desc").format(material=self.material, crafter=caller)
        item_weight = RECIPES.get(self.recipe).get("weight") * MATERIALS.get(self.material).get("weight_mod")
        item_value = RECIPES.get(self.recipe).get("value") * MATERIALS.get(self.material).get("value_mod")
        item_damage = RECIPES.get(self.recipe).get("damage_roll")
        item_range = RECIPES.get(self.recipe).get("range")
        item_durability = RECIPES.get(self.recipe).get("durability") * MATERIALS.get(self.material).get("dura_mod")
        item_current = item_durability
        item_hardness = RECIPES.get(self.recipe).get("hardness") * MATERIALS.get(self.material).get("hardness_mod")
        armor_pbonus = RECIPES.get(self.recipe).get("physical_bonus")
        armor_mbonus = RECIPES.get(self.recipe).get("magical_bonus")
        item_color = MATERIALS.get(self.material).get("color_code")

        self.weapon_proto = {
            "key": item_name,
            "color_code": item_color,
            "aliases": item_aliases,
            "typeclass": item_typeclass,
            "desc": item_desc,
            "weight": item_weight,
            "value": item_value,
            "damage_roll": item_damage,
            "range": item_range,
            "durability": item_durability,
            "current": item_current,
            "hardness": item_hardness,
            "location": caller.location
        }

        self.armor_proto = {
            "key": item_name,
            "color_code": item_color,
            "aliases": item_aliases,
            "typeclass": item_typeclass,
            "desc": item_desc,
            "weight": item_weight,
            "value": item_value,
            "durability": item_durability,
            "current": item_current,
            "hardness": item_hardness,
            "physical_bonus": armor_pbonus,
            "magical_bonus": armor_mbonus,
            "location": caller.location
        }

        caller.msg('|511You fire up the forge in preparation to forge a {material} {recipe}.|n'.format(
            material=self.material,
            recipe=RECIPES.get(self.recipe).get("key")))

        caller.location.msg_contents(
            "|511{actor} fires up the forge in preparation to forge a {material} {recipe}.|n",
            mapping=dict(actor=caller,
                         material=self.material,
                         recipe=RECIPES.get(self.recipe).get("key")),
            exclude=caller)

        utils.delay(20, callback=self.forge_one)

    def forge_one(self):
        caller = self.caller
        metal = ("iron", "steel", "mithril", "adamantine", "copper", "bronze", "brass", "silver", "gold")

        wood = ("cedar", "cypress", "fir", "yew", "larch", "pine", "spruce", "acacia", "aldar", "ash", "beech",
                "birch", "cherry", "ebony", "elm", "ironwood", "mahogany", "maple", "oak", "poplar", "walnut",
                "willow", "zingana", "leafweave")

        if self.material in metal:

            if "steel" in self.material:
                caller.msg("|511You begin smelting a usable {material} bar from iron ore and some coal.|n".format(
                    material=self.material))
                caller.location.msg_contents(
                    "|511{actor} begins smelting a usable {material} bar from iron ore and coal.|n",
                    mapping=dict(actor=caller,
                                 material=self.material),
                    exclude=caller)
            elif "brass" in self.material:
                caller.msg("|511You begin smelting a usable {material} bar from copper and zinc ores.|n".format(
                    material=self.material))
                caller.location.msg_contents(
                    "|511{actor} begins smelting a usable {material} bar from copper and zinc ores.|n",
                    mapping=dict(actor=caller,
                                 material=self.material),
                    exclude=caller)
            elif "bronze" in self.material:
                caller.msg("|511You begin smelting a usable {material} bar from copper and tin ores.|n".format(
                    material=self.material))
                caller.location.msg_contents(
                    "|511{actor} begins smelting a usable {material} bar from copper and tin ores.|n",
                    mapping=dict(actor=caller,
                                 material=self.material),
                    exclude=caller)
            else:

                caller.msg('|511You begin smelting the {material} ore into a usable bar for forging at the smelter.|n'
                           .format(material=self.material))

                caller.location.msg_contents(
                    "|511{actor} begins smelting the {material} ore into a usable bar for forging at the smelter.|n",
                    mapping=dict(actor=caller,
                                 material=self.material),
                    exclude=caller)

        elif self.material in wood:

            caller.msg('|511You begin milling the {material} log into a usable board at the mill table.|n'.format(
                material=self.material))

            caller.location.msg_contents(
                "|511{actor} begins milling a {material} log into a usable board at the mill table.|n",
                mapping=dict(actor=caller,
                             material=self.material),
                exclude=caller)

        utils.delay(20, callback=self.forge_two)

    def forge_two(self):
        caller = self.caller
        metal = ("iron", "steel", "mithril", "adamantine", "copper", "bronze", "brass", "silver", "gold")

        wood = ("cedar", "cypress", "fir", "yew", "larch", "pine", "spruce", "acacia", "aldar", "ash", "beech",
                "birch", "cherry", "ebony", "elm", "ironwood", "mahogany", "maple", "oak", "poplar", "walnut",
                "willow", "zingana", "leafweave")

        if self.material in metal:
            caller.msg('|511You take the {material} bar and start forging a {recipe} at the anvil.|n'.format(
                material=self.material,
                recipe=RECIPES.get(self.recipe).get("key")))

            caller.location.msg_contents(
                "|511{actor} takes the {material} bar and starts forging it into a {recipe} at the anvil.|n",
                mapping=dict(actor=caller,
                             material=self.material,
                             recipe=RECIPES.get(self.recipe).get("key")),
                exclude=caller)

        elif self.material in wood:
            caller.msg('|511You begin carving the {material} board into a {recipe} at the workbench.|n'.format(
                material=self.material,
                recipe=RECIPES.get(self.recipe).get("key")))

            caller.location.msg_contents(
                "|511{actor} begins carving a {material} board into a {recipe} at the workbench.|n",
                mapping=dict(actor=caller,
                             material=self.material,
                             recipe=RECIPES.get(self.recipe).get("key")),
                exclude=caller)

        utils.delay(20, callback=self.forge_three)

    def forge_three(self):

        if self.recipe in weapon_list:
            spawn(self.weapon_proto)
        elif self.recipe in armor_list:
            spawn(self.armor_proto)

        caller = self.caller
        caller.msg("|511You succeed in forging a {material} {recipe}|n".format(
            material=self.material,
            recipe=RECIPES.get(self.recipe).get("key")))

        caller.location.msg_contents(
            "|511{actor} succeeds in forging a {material}{recipe}|n",
            mapping=dict(actor=caller,
                         material=self.material,
                         recipe=RECIPES.get(self.recipe).get("key")),
            exclude=caller)

        # caller.db.forge_lastcast = time.time()


"""
if tr.SP.current < 10:
    caller.msg("You don't have enough power to cast this spell")
    return

if lastcast and time.time() - lastcast < 3 * 60:
    caller.msg("You cannot forge another item yet")
    return

tr.SP.current -= 10

has_smelter = any([x for x in self.caller.location.contents if x.tags.has("smelter")])

"""


class CmdSmelt(MuxCommand):
    """
    Spell Name: Smelt
       SP Cost: 10
    Coins Cost: Varies depending on recipe
        Syntax: smelt <material>
   Skills used: forge, weapons, armor

   Description:

     A simple spell that allows a merchant/artisan/trader
   to smelt raw ore into usable material components.
   """

    key = "smelt"
    locks = "cmd:all()"
    help_category = "commands"

    def func(self):
        material = self.args
        caller = self.caller

        if not material:
            caller.msg("Smelt What?")
            return

        item_name = "%s ingot" % (self.material.capitalize())
        item_aliases = RECIPES.get(self.recipe).get("aliases")
        item_typeclass = typeclasses.resources.Resource
        item_desc = MATERIALS.get(self.recipe).get("desc_bar").format(material=self.material, crafter=caller)
        item_weight = MATERIALS.get(self.material).get("weight")
        item_value = MATERIALS.get(self.material).get("value")
        item_color = MATERIALS.get(self.material).get("color_code")

        self.ingot_proto = {
            "key": item_name,
            "color_code": item_color,
            "aliases": item_aliases,
            "typeclass": item_typeclass,
            "desc": item_desc,
            "weight": item_weight,
            "value": item_value,
            "durability": item_durability,
            "current": item_current,
            "hardness": item_hardness,
            "location": caller.location
        }

        caller.msg('|511You fire up the smelter in preparation to smelt a {material} ingot.|n'.format(
            material=self.material, ))

        caller.location.msg_contents(
            "|511{actor} fires up the smelter in preparation to smelt a {material} ingot.|n",
            mapping=dict(actor=caller,
                         material=self.material,
                         ),
            exclude=caller)

        utils.delay(20, callback=self.smelt_one)

    def smelt_one(self):
        caller = self.caller
        material = self.args
        metal = ("iron", "steel", "mithril", "adamantine", "copper", "bronze", "brass", "silver", "gold")

        if material in metal:

            if "steel" in material:
                caller.msg("|511You begin smelting a usable {material} ingot from iron ore and some coal.|n".format(
                    material=material))
                caller.location.msg_contents(
                    "|511{actor} begins smelting a usable {material} ingot from iron ore and coal.|n",
                    mapping=dict(actor=caller,
                                 material=material),
                    exclude=caller)
            elif "brass" in material:
                caller.msg("|511You begin smelting a usable {material} ingot from copper and zinc ores.|n".format(
                    material=material))
                caller.location.msg_contents(
                    "|511{actor} begins smelting a usable {material} ingot from copper and zinc ores.|n",
                    mapping=dict(actor=caller,
                                 material=material),
                    exclude=caller)
            elif "bronze" in material:
                caller.msg("|511You begin smelting a usable {material} ingot from copper and tin ores.|n".format(
                    material=material))
                caller.location.msg_contents(
                    "|511{actor} begins smelting a usable {material} ingot from copper and tin ores.|n",
                    mapping=dict(actor=caller,
                                 material=material),
                    exclude=caller)
            else:

                caller.msg('|511You begin smelting the {material} ore into a usable ingot for forging at the smelter.|n'
                           .format(material=material))

                caller.location.msg_contents(
                    "|511{actor} begins smelting the {material} ore into a usable ingot for forging at the smelter.|n",
                    mapping=dict(actor=caller,
                                 material=material),
                    exclude=caller)

            utils.delay(20, callback=self.smelt_two)

    def smelt_two(self):
        caller = self.caller
        material = self.args
        metal = ("iron", "adamantine")

        if material in metal:
            caller.msg("|511You finish smelting an {material} ingot.|n".format(
                material=material))
            caller.location.msg_contents(
                "|511{actor} finishes smelting an {material} ingot.|n",
                mapping=dict(actor=caller,
                             material=material),
                exclude=caller)
        else:
            caller.msg("|511You finish smelting a {material} ingot.|n".format(
                material=material))
            caller.location.msg_contents(
                "|511{actor} finishes smelting a {material} ingot.|n",
                mapping=dict(actor=caller,
                             material=material),
                exclude=caller)

        spawn(self.ingot_proto)
