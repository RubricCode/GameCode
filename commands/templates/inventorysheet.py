"""
Character sheet EvForm template.
"""

import re

FORMCHAR = "x"
TABLECHAR = "o"

FORM = """
=-=-=-=-=-=-=-=-|C[ |rInventory |C]|n-=-=-=-=-=-=-=-=-=-=-=-=-o
Wielding:  xxxxAxxxxxx
           xxxxBxxxxxx
           
Armour:    xxxxCxxxxxx
           xxxxDxxxxxx
           xxxxExxxxxx
           xxxxFxxxxxx
           xxxxGxxxxxx
           xxxxHxxxxxx
           xxxxIxxxxxx
           xxxxJxxxxxx
           xxxxKxxxxxx
           
Clothing:  xxxxAxxxxxx
           xxxxAxxxxxx
           xxxxAxxxxxx
           xxxxAxxxxxx
           xxxxAxxxxxx
           xxxxAxxxxxx
           xxxxAxxxxxx
           xxxxAxxxxxx
           xxxxAxxxxxx
Carrying:  ooooooooooo
           ooooooooooo
           ooooooooooo
           ooooooooooo
           oooooDooooo
           ooooooooooo
           ooooooooooo
           ooooooooooo
           ooooooooooo
Wallet  xEx
Weight: xFx/xGx 
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-o
"""
FORM = re.sub(r'\|$', r'', FORM, flags=re.M)