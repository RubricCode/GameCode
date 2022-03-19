r"""
Evennia settings file.

The available options are found in the default settings file found
here:

c:\users\larry\mud3\evennia\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Ayacia"

######################################################################
# Game Time setup
######################################################################

# You don't actually have to use this, but it affects the routines in
# evennia.utils.gametime.py and allows for a convenient measure to
# determine the current in-game time. You can of course interpret
# "week", "month" etc as your own in-game time units as desired.

# The time factor dictates if the game world runs faster (timefactor>1)
# or slower (timefactor<1) than the real world.
TIME_FACTOR = 1.0
# The starting point of your game time (the epoch), in seconds.
# In Python a value of 0 means Jan 1 1970 (use negatives for earlier
# start date). This will affect the returns from the utils.gametime
# module. If None, the server's first start-time is used as the epoch.
TIME_GAME_EPOCH = None
# Normally, game time will only increase when the server runs. If this is True,
# game time will not pause when the server reloads or goes offline. This setting
# together with a time factor of 1 should keep the game in sync with
# the real time (add a different epoch to shift time)
TIME_IGNORE_DOWNTIMES = True

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/8.0/interactive/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True

######################################################################
# In-game Channels created from server start
######################################################################

# These are additional channels to offer. Usually, at least 'public'
# should exist. The superuser will automatically be subscribed to all channels
# in this list. New entries will be created on the next reload. But
# removing or updating a same-key channel from this list will NOT automatically
# change/remove it in the game, that needs to be done manually.
DEFAULT_CHANNELS = [
    # public channel
    {
        "key": "OOC",
        "aliases": ("ooc"),
        "desc": "Out of Character Admin discussion",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
	# newbie question channel
    {
		"key": "Question",
		"aliases": 'question',
		"desc": "OOC Channel for New player questions",
		"locks": "control:perm(Admin);listen:all();send:all()",
	},
    # OOC chat channel
	{
		"key": "Chat",
		"aliases": 'chat',
		"desc": "OOC chat channel",
		"locks": "control:perm(Admin);listen:all();send:all()",
	},
]
# Optional channel info (same form as CHANNEL_MUDINFO) for the channel to
# receive connection messages ("<account> has (dis)connected").  While the
# MudInfo channel will also receieve this info, this channel is meant for
# non-staffers.
CHANNEL_CONNECTINFO = None

SEARCH_MULTIMATCH_TEMPLATE = "{name}{aliases}{info} {number}\n"
SEARCH_MULTIMATCH_REGEX = r"(?P<name>.*) (?P<number>[0-9]+)"

######################################################################
# Default Account setup and access
######################################################################

# Different Multisession modes allow a player (=account) to connect to the
# game simultaneously with multiple clients (=sessions). In modes 0,1 there is
# only one character created to the same name as the account at first login.
# In modes 2,3 no default character will be created and the MAX_NR_CHARACTERS
# value (below) defines how many characters the default char_create command
# allow per account.
#  0 - single session, one account, one character, when a new session is
#      connected, the old one is disconnected
#  1 - multiple sessions, one account, one character, each session getting
#      the same data
#  2 - multiple sessions, one account, many characters, one session per
#      character (disconnects multiplets)
#  3 - like mode 2, except multiple sessions can puppet one character, each
#      session getting the same data.
MULTISESSION_MODE = 0
# The maximum number of characters allowed by the default ooc char-creation command
MAX_NR_CHARACTERS = 1

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
