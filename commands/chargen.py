from evennia.commands import cmdhandler
from evennia.utils import logger
from evennia import Command, CmdSet
from commands.command import MuxCommand
from world.guilds.guilds import apply_guild
from evennia.server.sessionhandler import SESSIONS


class CmdRules(MuxCommand):
    """
    Display and agree to rules.
 
    Usage:
      rules
    """

    key = "rules"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        choice = yield "  Have you read the rules and agree to abide by them (Yes/No)?"
        if not choice in ('yes', 'y', 'no', 'n'):
            choice = yield "please answer Yes or No"
        if choice in ('yes', 'y'):
            caller.msg('You agree to the rules and may now continue To the Kingdom, Caliphate or Empire')
            caller.db.rules = True
        if choice in ('no', 'n'):
            caller.msg('You must read the rules and agree to them before proceeding')
            caller.db.rules = False


class CmdGender(MuxCommand):
    """
    Sets gender on yourself

    Usage:
      choose male||female

    """
    key = "choose"
    locks = "cmd:all()"

    def func(self):
        """
        Implements the command.
        """
        caller = self.caller
        arg = self.args.strip().lower()
        if arg not in ("male", "female"):
            caller.msg("Usage: choose male||female")
            return
        caller.db.gender = arg
        caller.msg("Your gender was set to %s." % arg)


class CmdPassVeil(MuxCommand):
    """
    Moves the character from character creation into the game proper
    
    Usage:
      pass veil
      
    """

    key = "pass veil"
    locks = "cmd:all()"

    def func(self):
        """
        Implements the command
        
        """
        caller = self.caller
        name = caller.name
        gender = caller.db.gender
        race = caller.db.race

        del caller.db.descSet
        del caller.db.backSet
        del caller.db.statSet

        if caller.db.nation == "Kingdom":
            newhome = self.obj.search('', global_search=True)
            caller.home = newhome
            guild = "Peasant"
            apply_guild(caller, guild)
            startloc = self.obj.search('Peasant Cottage', global_search=True)
            self.obj.move_to(startloc, quiet=True, move_hooks=False)

        if caller.db.nation == "Empire":
            newhome = self.obj.search('', global_search=True)
            caller.home = newhome
            guild = "Peon"
            apply_guild(caller, guild)
            startloc = self.obj.search('Peon Quarters', global_search=True)
            self.obj.move_to(startloc, quiet=True, move_hooks=False)

        if caller.db.nation == "Caliphate":
            newhome = self.obj.search('Central Plaza - Sakath', global_search=True)
            caller.home = newhome
            valid_choice = ("servant", "conscript", "slave")
            result = yield "would you like to start as a Servant, conscript or slave?"
            if result not in valid_choice:
                result = yield "please enter servant, conscript or slave"
            if 'servant' in result:
                guild = "Servant"
                apply_guild(caller, guild)
                startloc = self.obj.search('Palace - Servant Office ', global_search=True)
                self.obj.move_to(startloc, quiet=True, move_hooks=False)
                servmsg = " [************--World Crier--************]" \
                          "%s becomes a servant in the Caliph's Palace!" \
                          "[*****************************************]"
                SESSIONS.announce_all(servmsg)

            if 'conscript' in result:
                guild = "Conscript"
                apply_guild(caller, guild)
                startloc = self.obj.search('Warden Office - Conscript Quarters', global_search=True)
                self.obj.move_to(startloc, quiet=True, move_hooks=False)
                consmsg = " [************--World Crier--************]" \
                          "%s is conscripted into the Caliph's Legions!" \
                          "[*****************************************]"
                SESSIONS.announce_all(consmsg)

            if 'slave' in result:
                guild = "Slave"
                apply_guild(caller, guild)
                caller.db.owner = ''
                startloc = self.obj.search('Slave Auction - Slave Pens', global_search=True)
                self.obj.move_to(startloc, quiet=True, move_hooks=False)
                slavemsg = " [************--World Crier--************]" \
                           "%s is bound to a life of slavery in Caliphate city name!" \
                           "[*****************************************]"
                SESSIONS.announce_all(slavemsg)
                choices = ('worker', 'performer', 'teacher', 'gladiator')
                choice = yield 'Select the type of slave. worker, teacher, performer or gladiator'
                if choice not in choices:
                    choice = yield "please enter worker, teacher, performer or gladiator"
                    if 'worker' in choice:
                        message = "|/======================**********=====================|/|/" \
                                  "The Slave Master of Sakath Announces the Sale of|/" \
                                  "a Worker Slave: %s, the %s %s.|/|/" \
                                  "This specimen is strong and built for heavy duty|/" \
                                  "work. Carrying large items or to intimidate your|/" \
                                  "peers, this slave can be found at the slave pens.|/|/" \
                                  "=====================**********=====================|/" % (name, gender, race)
                        SESSIONS.announce_all(message)
                    elif 'teacher' in choice:
                        message = "|/======================**********=====================|/|/" \
                                  "The Slave Master of Sakath Announces the Sale of|/" \
                                  "a Teacher Slave: %s, the %s %s.|/|/" \
                                  "This specimen is strong and built for heavy duty|/" \
                                  "work. Carrying large items or to intimidate your|/" \
                                  "peers, this slave can be found at the slave pens.|/|/" \
                                  "=====================**********=====================|/" % (name, gender, race)
                        SESSIONS.announce_all(message)
                    elif 'performer' in choice:
                        message = "|/======================**********=====================|/|/" \
                                  "The Slave Master of Sakath Announces the Sale of|/" \
                                  "a Performer Slave: %s, the %s %s.|/|/" \
                                  "This specimen is sleek and sensual and trained in|/" \
                                  "the art of dance and music. More specifics about|/" \
                                  "this slave can be found at the slave pens.|/|/" \
                                  "=====================**********=====================|/" % (name, gender, race)
                        SESSIONS.announce_all(message)
                    elif 'gladiator' in choice:
                        message = "|/======================**********=====================|/|/" \
                                  "The Slave Master of Sakath Announces the Sale of|/" \
                                  "a Gladiator Slave: %s, the %s %s.|/|/" \
                                  "This specimen is strong and built for heavy duty|/" \
                                  "work. Carrying large items or to intimidate your|/" \
                                  "peers, this slave can be found at the slave pens.|/|/" \
                                  "=====================**********=====================|/" % (name, gender, race)
                        SESSIONS.announce_all(message)
