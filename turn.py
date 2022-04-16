from moveClass import *
from monsterClass import * 
from damageCalc import *


def botBattle(user, userTeam, foe, foeTeam):
    userLeft, foeLeft = userTeam[-1], foeTeam[-1]
    while userLeft != 0 and foeLeft != 0:
        if user.fainted == True:
            user = switch(user, userTeam)
        elif foe.fainted == True:
            foe = switch(foe, foeTeam)
        while user.fainted != True and foe.fainted != True:
            userAttacked, foeAttacked = True, True
            foeChoice = random.randint(0, 4) #random AI choice
            if foeChoice == 4 and foe:
                newFoe = switch(foe, foeTeam)
                foeAttacked = False
                foe = newFoe
            print(f"What will {user.name} do?")
            for moveSlot in user.moveset:
                print(moveSlot, end = ' ')
            print()
            userChoice = int(input("Pick attack 0 - 3 or press 4 to switch: ")) #user input
            if userChoice == 4:
                newUser = switch(user, userTeam) 
                userAttacked = False
                user = newUser
            if foe.finalStats["SPE"] > user.finalStats["SPE"]:
                moveOrder = [(foe, foeAttacked), (user, userAttacked)]
            else:
                moveOrder = [(user, userAttacked), (foe, foeAttacked)]
            for switchCheck in moveOrder: #check for switches
                if switchCheck[1] == False:
                    moveOrder.remove(switchCheck)
            if len(moveOrder) == 2:
                if moveNames[user.moveset[userChoice]].priority > moveNames[foe.moveset[foeChoice]].priority: #priority check
                    moveOrder[::-1]
            for attackerData in moveOrder:
                attacker = attackerData[0]
                if attacker.fainted == True:
                    continue
                if attacker == user:
                    defender = foe
                    defenderLeft = foeLeft
                    attackerMove = moveNames[user.moveset[userChoice]]
                else:
                    defender = user
                    defenderLeft = userLeft
                    attackerMove = moveNames[foe.moveset[foeChoice]]
                attackSequence(attacker, defender, attackerMove)
                if defender.fainted == True:
                    defenderLeft -= 1
                print()
    if userLeft == 0:
        print("AI wins!")
    else:
        print("User wins!")
            
def switch(currentMon, team):
    if team[-1] == 0:
        print("You have no Pokemon to switch to!")
        return currentMon
    print("Here's your team")
    teamNameMap = dict()
    for teamMon in team:
        if type(teamMon) == int:
            continue
        if teamMon.fainted == True:
            print(teamMon.name + "(fainted)")
        else:
            print(teamMon.name)
        teamNameMap[teamMon.name] = teamMon
    while True:
        newMonName = input("Pick a member to switch in: ")
        while newMonName not in teamNameMap:
            newMonName = input(f"{newMonName} is not on your team! Pick a member to switch in: ")
        newMon = teamNameMap[newMonName]
        if newMon.fainted == True:
            newMonName = input(f"{newMon.name} has no energy left to battle! Pick a member to switch in: ")
        elif newMon == currentMon:
            newMonName = print("You can't cancel a switch! Pick a member to switch in: ")
        else:
            break
    print(f"{newMon.name} has switched in!")
    return newMon

userTeam = [thugger, alder, 2]
foeTeam = [lance, blunder, 2]

botBattle(userTeam[0], userTeam, foeTeam[0], foeTeam)
