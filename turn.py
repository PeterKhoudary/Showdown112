from moveClass import *
from monsterClass import * 
from damageCalc import *

def turn(user, foe):
    while user.fainted == False and foe.fainted == False:
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
            taken, left = damageOutput(attacker, defender, moveNames[moveName])
            print(f"{attacker}'s {moveName} takes {taken}% of {defender}'s life! {defender} has {left}% left.")
            if left <= 0:
                print(f'{defender} has run out of energy to battle! {attacker} wins!')
                defender.fainted = True
                break
turn(thugger, blunder)


