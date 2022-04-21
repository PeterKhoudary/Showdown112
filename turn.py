from moveClass import *
from monsterClass import * 
from damageCalc import *
import time 

def botBattle(user, userTeam, foe, foeTeam):
    userLeft, foeLeft = userTeam[-1], foeTeam[-1]
    while userLeft != 0 and foeLeft != 0:
        print(f'user mons = {userLeft}, bot mons = {foeLeft}')
        if user.fainted == True:
            user = switch(user, userTeam)
        elif foe.fainted == True:
            foe = switch(foe, foeTeam, True)
        while user.fainted != True and foe.fainted != True:
            userAttacked, foeAttacked = True, True
            # foeChoice = random.randint(0, 4) #random AI choice
            # while foeChoice == 4 and foeTeam[-1] == 1:
            #     foeChoice = random.randint(0, 4)
            # if foeChoice == 4:
            #     newFoe = switch(foe, foeTeam, True) 
            #     foeAttacked = False
            #     foe = newFoe
            print(f"What will {user.name} do?")
            for moveSlot in user.moveset:
                print(moveSlot[0], end = '   ')
            print()
            userChoice = int(input("Pick attack 0 - 3 or press 4 to switch: ")) #user input
            while userChoice == 4 and userTeam[-1] == 1:
                userChoice = input("You have no remaining Pokemon! /n Choose an attack: ")
            if userChoice == 4:
                newUser = switch(user, userTeam) 
                userAttacked = False
                user = newUser
            foeChoice = random.randint(0, 4) #random AI choice
            while foeChoice == 4 and foeTeam[-1] == 1:
                foeChoice = random.randint(0, 4)
            if foeChoice == 4:
                newFoe = switch(foe, foeTeam, True) 
                foeAttacked = False
                foe = newFoe
            if foe.finalStats["SPE"] > user.finalStats["SPE"]:
                moveOrder = [(foe, foeAttacked), (user, userAttacked)]
            else:
                moveOrder = [(user, userAttacked), (foe, foeAttacked)]
            for switchCheck in moveOrder: #check for switches
                if switchCheck[1] == False:
                    moveOrder.remove(switchCheck)
            if len(moveOrder) == 2: #priority check
                if moveNames[user.moveset[userChoice][0]].priority > moveNames[foe.moveset[foeChoice][0]].priority:
                    moveOrder = [(user, userAttacked), (foe, foeAttacked)]
                elif moveNames[foe.moveset[foeChoice][0]].priority > moveNames[user.moveset[userChoice][0]].priority: 
                    moveOrder = [(foe, foeAttacked), (user, userAttacked)]
            for attackerData in moveOrder:
                attacker = attackerData[0]
                if attacker.fainted == True:
                    continue
                if attacker == user:
                    defender = foe
                    attackerChoice = userChoice
                else:
                    defender = user
                    attackerChoice = foeChoice
                attackSequence(attacker, defender, moveNames[attacker.moveset[attackerChoice][0]])
                attacker.moveset[attackerChoice][1] -= 1
                if defender.fainted == True:
                    if defender == foe:
                        foeTeam[-1] -= 1
                    else:
                        userTeam[-1] -= 1
                userLeft, foeLeft = userTeam[-1], foeTeam[-1]
                print()
    if userLeft == 0:
        print("AI wins!")
    else:
        print("User wins!")
            
def switch(currentMon, team, bot = False):
    if bot:
        botChoice = random.randint(0, len(team) - 2)
        botMon = team[botChoice]
        while botMon == currentMon or botMon.fainted == True:
            botChoice = random.randint(0, len(team) - 2)
            botMon = team[botChoice]
        print(f"{botMon.name} has switched in!")
        print()
        return botMon
    print("Here's your team")
    teamNameMap = dict()
    for teamMon in team:
        if type(teamMon) == int:
            continue
        if teamMon.fainted == True:
            print(teamMon.name + " (fainted)")
        else:
            print(teamMon.name)
        teamNameMap[teamMon.name] = teamMon
    foundMon = False
    while foundMon == False:
        newMonName = input("Pick a member to switch in: ")
        newMon = teamNameMap[newMonName]
        if newMonName not in teamNameMap:
            print(f"{newMonName} is not on your team!")
        elif newMon.fainted == True:
            print(f"{newMon.name} has no energy left to battle!")
        elif newMon == currentMon:
            print("You can't cancel a switch!")
        else:
            foundMon = True
    team.remove(currentMon)
    team.insert(0, currentMon)
    print(f"{newMon.name} has switched in!")
    print()
    return newMon

foeTeam = [thugger, lance, 2]
userTeam = [alder, blunder, 2]

#botBattle(userTeam[0], userTeam, foeTeam[0], foeTeam)
