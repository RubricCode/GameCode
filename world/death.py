"""
Death Module
Controls what happens when a character or NPC character dies
"""
from random import randint
from math import floor
from evennia import CmdSet
from commands.command import MuxCommand
from evennia.utils import delay
from typeclasses.scripts import Script
#from evennia.utils.spawner import spawn

# Scripts


class DeathHandler(Script):
    """ Base script for death mechanics handlers """
    def at_script_creation(self):
        super(DeathHandler, self).at_script_creation()

        self.key = "death_handler_{}".format(self.obj.id)
        self.desc = "handles character death"
        self.interval = 0
        self.repeats = 0
        self.start_delay = False
        self.persistent = True

        self.db.death_step = 0
        self.db.death_cb = None
        # subclasses define the sequence of callbacks
        self.db.death_sequence = ()

    def at_start(self):
        """Parent at_start should be called first in subclasses."""
        self.obj.cmdset.add(DeadCmdSet)
        if len(self.db.death_sequence) > 0 and self.db.death_step > 0:
            delay(3, getattr(self, self.db.death_sequence[self.db.death_step]))

    def at_stop(self):
        self.obj.cmdset.remove(DeadCmdSet)


class CharDeathHandler(DeathHandler):
    """Script that handles death mechanics for Characters"""
    def at_script_creation(self):
        super(CharDeathHandler, self).at_script_creation()
        self.db.death_sequence = ('floating', 'returning', 'pre_revive', 'revive')

    def at_start(self):
        """handles the phases of death"""
        super(CharDeathHandler, self).at_start()
        self.obj.msg("you have died")
        self.obj.location.msg_contents('{character} falls to the ground dead.',
                                       mapping={'character': self.obj},
                                       exclude=self.obj)
        self.obj.traits.XP.current -= int(floor(0.15 * self.obj.traits.XP.current))
        corpse_name = 'corpse of %s' % self.obj
        corpse_desc = "A dead body that was once %s in life." % self.obj
        corpse_proto = {'key': corpse_name, "desc": corpse_desc}
        corpse = spawn(corpse_proto)[0]
        corpse.location = self.obj.location
        for i in self.obj.equip:
            self.obj.equip.remove(i)
        for i in self.obj.contents:
            dest_chance = randint(1, 100)
            if dest_chance <= 15:
                i.delete()
            else:
                i.move_to(corpse, quiet=True)

        void = self.obj.search('Void', global_search=True)
        self.obj.move_to(void, quiet=True, move_hooks=False)
        delay(20, getattr(self, self.db.death_sequence[self.db.death_step]))

    def floating(self):
        self.obj.msg('Your awareness blinks back into existence briefly as you float in the darkness of the void.')
        self.db.death_step += 1
        delay(12, getattr(self, self.db.death_sequence[self.db.death_step]))

    def returning(self):
        if self.obj.db.permadeath is False:
            self.obj.msg(
                "You feel a quickening in your energy as you feel pulled towards the |mSpirit Realm|n."
            )
            spiritrealm = self.obj.search('Spirit Realm', global_search=True)
            spiritrealm.msg_contents(
                'A sudden roar fills the realm as the the surface of the |/'
                'purple pool becomes agitated, spattering droplets into the air |/')

            self.db.death_step += 1
            delay(8, getattr(self, self.db.death_sequence[self.db.death_step]))
        else:
            self.obj.msg(
                "you feel a rending of your spirit as you are pulled towards the |mRealm of Eternal Death|n.")
            eternaldeath = self.obj.search('Realm of Eternal Death', global_search=True)
            eternaldeath.msg_contents(
                'a cacophony of sound interupts the silence, heralding the arrival of another soul forever damned'
            )
            self.db.death_step += 1
            delay(8, getattr(self, self.db.death_sequence[self.db.death_step]))

    def pre_revive(self):
        if self.obj.db.permadeath is False:
            self.obj.msg(
                'A blinding light flashes before you and you feel your body lurch forward onto |/'
                'smooth ground. Your senses reel from the disorienting ordeal of your return.')
            spiritrealm = self.obj.search('Spirit Realm', global_search=True)
            spiritrealm.msg_contents(
                'More and more purple droplets arise in a column from the roiling waters, glowing|/'
                'ever brighter. Without warning, the column erupts in a blinding flash of light.|/'
                'When your sight returns, the figure of {character} lays curled up on the ground |/'
                'looking confused and disoriented.',
                mapping=dict(character=self.obj),
                exclude=self.obj)
            delay(10, getattr(self, self.db.death_sequence[self.db.death_step]))
        else:
            self.obj.msg(
                "Shadows flicker and dance around you cutting and tearing at your soul as |/"
                " you collapse onto the ground of this hellish landscape. Your ears ring |/"
                "from the deafening sound of your return.")
            eternaldeath = self.obj.search('Realm of Eternal Death', global_search=True)
            eternaldeath.msg_contents(
                'The sound of thunder echoes and lightning flashes throughout the realm |/'
                'as a vicious tear rips open in in the air, otherworldly flame licking |/ '
                'at its edges angrily. The figure of {character} plummets from the sky |/ '
                'and collapses in a heap onto the cracked and broken landscape',
                mapping = dict(character=self.obj),
                exclude = self.obj)
            delay(10, getattr(self, self.db.death_sequence[self.db.death_step]))

    def revive(self):
        if self.obj.db.permadeath is False:
            self.obj.traits.HP.fill_gauge()
            self.obj.traits.SP.fill_gauge()
            self.obj.traits.EP.fill_gauge()
            spiritrealm = self.obj.search('Spirit Realm', global_search=True)
            self.obj.move_to(spiritrealm, quiet=True, move_hooks=False)
            self.stop()

        else:
            self.obj.traits.HP.fill_gauge()
            self.obj.traits.SP.fill_gauge()
            self.obj.traits.EP.fill_gauge()
            eternaldeath = self.obj.search('Realm of Eternal Death', global_search=True)
            self.obj.move_to(eternaldeath, quiet=True, move_hooks=False)
            self.stop()

class NPCDeathHandler(DeathHandler):
    """
    Script that handles death mechanics for Non player characters.
    """
    def at_script_creation(self):
        super(NPCDeathHandler,self).at_script_creation()
        self.db.death_sequence = ('storage','revive')

    def at_start(self):
        """Handles the 'phases' of death"""
        super(NPCDeathHandler,self).at_start()
        self.obj.location.msg_contents('{character} falls dead at your feet',
                                       mapping={'character':self.obj},
                                       exclude=self.obj)

        delay(2, getattr(self,self.db.death_sequence[self.db.death_step]))

    def storage(self):
        #make the corpse and move the npc away.
        corpse_name = 'corpse of %s' % self.obj
        corpse_desc = "A dead body that was once %s in life." % self.obj
        corpse_proto = {'key': corpse_name, "desc": corpse_desc}
        corpse = spawn(corpse_proto)[0]
        corpse.location = self.obj.location
        for i in self.obj.equip:
            self.obj.equip.remove(i)
        for i in self.obj.contents:
            dest_chance = randint(1, 100)
            if dest_chance <= 15:
                i.delete()
            else:
                i.move_to(corpse, quiet=True)
        storage = self.obj.search('Storage', global_search=True)
        self.obj.move_to(storage, quiet=True, move_hooks=False)
        self.db.death_step += 1
        delay(10 * randint(1,12) + 30, getattr(self,self.db.death_sequence[self.db.death_step]))

    def revive(self):
        """Reveive the Dead NPC"""
        self.obj.traits.HP.fill_gauge()
        self.obj.traits.HP.fill_gauge()
        self.obj.traits.HP.fill_gauge()
        self.obj.move_to(self.obj.home)
        self.stop()

class DeadCmdSet(CmdSet):
    key = "death_cmdset"
    mergetype = "Replace"
    priority = 100
    no_exits = True
    no_objs = True

    def at_cmdset_creation(self):
        self.add(CmdPray)
        self.add(CmdDeadHelp)


class CmdPray(MuxCommand):
    """ 
    Pray to the diety of your choice to be resurrected.
    
    Usage: pray <diety>
    """
    key = 'pray'
    lock = 'cmd:all(),attr(permadeath, False)'
    def func(self):
        caller = self.caller
        arg = self.args.strip().lower()
        if not arg in ('atheist','helotyr','sarthoar', 'aphea'):
            caller.msg(' you need to either pray <deity> or pray <atheist>')
        if 'atheist' in arg:
            if caller.db.Nation == 'Kingdom':
                caller.move_to(caller.home)
            elif caller.db.Nation == 'Empire':
                caller.move_to(caller.home)
            elif caller.db.Nation == 'Caliphate':
                caller.move_to(caller.home)
        if 'helotyr' in arg:
            if caller.db.Nation == 'Kingdom':
                caller.move_to()
            elif caller.db.Nation == 'Empire':
                caller.move_to()
            elif caller.db.Nation == 'Caliphate':
                caller.move_to()
        if 'sarthoar' in arg:
            if caller.db.Nation == 'Kingdom':
                caller.move_to()
            elif caller.db.Nation == 'Empire':
                caller.move_to()
            elif caller.db.Nation == 'Caliphate':
                caller.move_to()
        if 'aphea' in arg:
            if caller.db.Nation == 'Kingdom':
                caller.move_to()
            elif caller.db.Nation == 'Empire':
                caller.move_to()
            elif caller.db.Nation == 'Caliphate':
                caller.move_to()


class CmdDeadHelp(MuxCommand):
    """help command when dead"""
    key = 'help'
    lock = 'cmd:all()'

    def func(self):
        self.caller.msg('|r YOU ARE DEAD|n')
        self.caller.msg('Your character has died, probably in some horrible way. |/'
                        'If you are in the Spirit Realm, you can pray to the deity |/'
                        'of your choice to be resurrected. If however you ended up in |/'
                        'the Realm of Eternal Death, ask for staff to assist you in the |/'
                        'retirement process.' )