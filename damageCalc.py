from monsterClass import *
from moveClass import *
import random
import decimal

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def damageCalc(attacker, defender, move):
    damage = (((((2 * attacker.level) / 5) + 2) * move.power * (attacker.finalStats[move.uses] / defender.finalStats[move.hits])) / 50) + 2
    if move.type in attacker.types:
        damage *= 1.5
    for defenseType in defender.types:
        if move.type in resists[defenseType]:
            damage /= 2
        elif move.type in weaknesses[defenseType]:
            damage *= 2
        elif move.type in immunities[defenseType]:
            return 0
    roll = random.randint(85,100)
    damage = roundHalfUp(damage * roll / 100)
    defender.currentHP -= damage
    percentDamage = roundHalfUp(damage / defender.finalStats["HP"] * 100)
    percentRemaining = roundHalfUp(defender.currentHP / defender.finalStats["HP"] * 100)
    print(damage, percentDamage, defender.currentHP, percentRemaining )
    # if defender.currentHP <= 0:
    #     return f'{defender.name} fainted !'
    return(percentDamage, percentRemaining)
