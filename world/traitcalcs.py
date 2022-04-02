PRIMARY_TRAITS = ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA')
ABILITY_MODIFIER_TRAITS = ('STRMOD', 'DEXMOD', 'CONMOD', 'INTMOD', 'WISMOD', 'CHAMOD')
SECONDARY_TRAITS = ('HP', 'SP')
SAVE_ROLLS = ('FORT', 'REFL', 'WILL')
COMBAT_TRAITS = ('ATKM', 'ATKR', 'ATKU', 'PDEF', 'MDEF')
OTHER_TRAITS = ('LVL', 'XP', 'ENC', 'EP')


abilitymodifiers = [0, -5, -4, -4, -3, -3, -2, -2, -1, -1, -0, -0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,
                    10, 10, 11]


def calculate_secondary_traits(traits):
    """
    Calculations for secondary traits
    """
    # secondary traits
    # saves
    traits.FORT.mod = abilitymodifiers[traits.CON.value]
    traits.REFL.mod = abilitymodifiers[traits.DEX.value]
    traits.WILL.mod = abilitymodifiers[traits.WIS.value]
    # combat
    traits.MAB.mod = abilitymodifiers[traits.STR.value]
    traits.FAB.mod = abilitymodifiers[traits.DEX.value]
    traits.RAB.mod = abilitymodifiers[traits.DEX.value]
    traits.UAB.mod = abilitymodifiers[traits.DEX.value]
    # misc
    traits.PDEF.mod = abilitymodifiers[traits.DEX.value]
    traits.MDEF.mod = abilitymodifiers[traits.INT.value]
