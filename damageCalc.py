from monsterClass import *
from moveClass import *
import random
import decimal

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def attackSequence(attacker, defender, move):
    missThreshold = move.accuracy * 100
    hitCheck = random.randint(1, 100)
    if hitCheck > missThreshold:
        print(f"{attacker.name}'s attack missed!")
        return
    percentBefore = round(defender.currentHP / defender.finalStats["HP"] * 100, 1)
    damage = (((((2 * attacker.level) / 5) + 2) * move.power * (attacker.finalStats[move.uses] / defender.finalStats[move.hits])) / 50) + 2
    if move.type in attacker.types:
        damage *= 1.5
    roll = random.randint(85,100)
    damage = roundHalfUp(damage * roll / 100)
    critChance = random.randint(1, 16)
    if critChance == 1:
        damage = 1.5 * roundHalfUp(damage * 1.5)
    damageBeforeTypes = damage
    for defenseType in defender.types:
        if move.type in resists[defenseType]:
            damage /= 2
        elif move.type in weaknesses[defenseType]:
            damage *= 2
        elif move.type in immunities[defenseType]:
            print(f'{defenseType} types are immune to {move}')
            return 
    defender.currentHP -= damage
    percentDamage = round(damage / defender.finalStats["HP"] * 100, 1)
    if percentDamage > percentBefore:
        percentDamage = percentBefore
    percentAfter = round(defender.currentHP / defender.finalStats["HP"] * 100, 1)
    if percentAfter <= 0:
        percentAfter = 0
    print(f"{attacker.name}'s {move.name} takes {percentDamage}% of {defender.name}'s HP!")
    if critChance == 1:
        print("A critical hit!")
    if damage < damageBeforeTypes:
        print("It's not very effective...")
    elif damage > damageBeforeTypes:
        print("It's super effective!")
    print(f"{defender.name} has {percentAfter}% HP left.")
    if defender.currentHP <= 0:
        print(f"{defender.name} fainted!")
        defender.fainted = True
    return 

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
            return 0, 0
    damages = 0
    for roll in range(85, 101):
        damage = roundHalfUp(damage * roll / 100)
        damages += damage
    averageDamage = roundHalfUp(damage / 16)
    percentDamage = round(averageDamage / defender.finalStats["HP"] * 100, 1)
    return percentDamage

