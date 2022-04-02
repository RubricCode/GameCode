"""
Character sheet EvForm template.
"""

import re

FORMCHAR = "x"
TABLECHAR = "o"

FORM = """
=-=-=-=-=-=-=-=-=-=-=-=-|C[ |rCharacter Sheet |C]|n-=-=-=-=-=-=-=-=-=-=-=-=-o
                                                                    ||
Name : xAxxxxxxxx                          |CStrength|n     : xLxx      ||
Race : xBxxxxxxxx                          |CDexterity|n    : xMxx      ||
Sex  : xCxxxxxxxx                          |CConstitution|n : xNxx      ||
Guild: xDxxxxxxxxxxxxxxxxxxx               |CIntelligence|n : xOxx      ||
Clan : xExxxxxxxx                          |CWisdom|n       : xPxx      ||
Title: xFxxxxxxxx                          |CCharisma|n     : xQxx      ||
Level: xGxxxxxxxx                          |CHealth|n       : xUxx(xVxx)||
Faith: xHxxxxxxxx                          |CSpellpower|n   : xWxx(xXxx)||
Devotion: xIxxxxxxxx                       |CEndurance|n    : xYxx(xZxx)||
Nation  : xJxxxxxxxx                       |CExperience|n   : xxRxx     ||
Background: xKxxxxxxxx                     |CEncumbrance|n  : xSxx(xTxx)|| 
                                                                    ||
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-o

"""
FORM = re.sub(r'\|$', r'', FORM, flags=re.M)
