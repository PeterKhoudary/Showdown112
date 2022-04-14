from moveClass import *
from monsterClass import * 
from damageCalc import *

def turn(user, foe):
    if user.finalStats["SPE"] > foe.finalStats["SPE"]:
        moveOrder = [user, foe]
    else:
        moveOrder = [foe, user]
    for attacker in moveOrder:
        if attacker == moveOrder[0]: defender = moveOrder[1]
        else: defender = moveOrder[0]
        print("Here is your moveset:")
        print(attacker.moveset)
        moveName = input("What attack will you choose? ")
        taken, left = damageCalc(attacker, defender, moveNames[moveName])
        print(f"{attacker}'s {moveName} takes {taken}% of {defender}'s life! {defender} has {left}% left.")
turn(lance, alder)


