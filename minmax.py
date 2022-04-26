from turn import *
from damageCalc import *
print("Battle AI")

infinity = 1000 #idk we'll see how this needs to be tweaked, minmaxing is fun cuz the heuristic is subjective

#WRITE HEURISTIC

###############################################################################
#Game state will be represented as a tuple state = (playerTeam, botTeam)
#Where playerTeam and botTeam are copy.deepcopies of the teams sent by app

###############################################################################
#all possible Moves
def allPossibleMoves(team):
    for mon in team:
        mon = team[0]
        possibleMoves = []
        for moveSlot in range(len(mon.moveset)):
            if mon.moveset[moveSlot][1] == 0:
                continue
            else:
                possibleMoves.append(moveSlot)
        for monSlot in range(1, len(team) - 1):
            if team[monSlot].fainted:
                continue
            else:
                possibleMoves.append((4, monSlot))
        return possibleMoves

def allBranches(state):
    playerMoves, botMoves = allPossibleMoves(state[0]), allPossibleMoves(state[1])
    allMoves = []
    for myMove in playerMoves:
        for theirMove in botMoves:
            allMoves.append((myMove, theirMove))
    return allMoves

def allPossibleSwitches(team):
    possibleSwitches = []
    for monSlot in range(1, len(team) - 1):
            if team[monSlot].fainted:
                continue
            else:
                possibleSwitches.append(monSlot)
    return possibleSwitches

###############################################################################
#nondestructive state editing
def botSwitch(team, choice):
    if team[-1] == 0:
        return
    else:
        botMon = team[choice]
        team.remove(botMon)
        team.insert(0, botMon)
    return team

def botAttackSequence(attacker, defender, move):
    missThreshold = move.accuracy * 100
    hitCheck = random.randint(1, 100)
    if hitCheck > missThreshold:
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
    for defenseType in defender.types:
        if move.type in resists[defenseType]:
            damage /= 2
        elif move.type in weaknesses[defenseType]:
            damage *= 2
        elif move.type in immunities[defenseType]:
            return 
    defender.currentHP -= damage
    percentDamage = round(damage / defender.finalStats["HP"] * 100, 1)
    if percentDamage > percentBefore:
        percentDamage = percentBefore
    percentAfter = round(defender.currentHP / defender.finalStats["HP"] * 100, 1)
    if percentAfter <= 0:
        percentAfter = 0
    #print(f"{attacker.name}'s {move.name} takes {percentDamage}% of {defender.name}'s HP! ")
    #print(f" {defender.name} has {percentAfter}% HP left.\n")
    if defender.currentHP <= 0:
        defender.currentHP = 0
        #print(f"{defender.name} fainted!\n")
        defender.fainted = True  

def botTurn(playerTeam, playerChoice, botTeam, botChoice):
    player, bot = playerTeam[0], botTeam[0]
    playerLeft, botLeft = playerTeam[-1], botTeam[-1]
    if playerLeft > 0 and botLeft > 0:
        playerAttacked, botAttacked = True, True
        if type(playerChoice) == tuple:
            botSwitch(playerTeam, playerChoice[1])
            player = playerTeam[0]
            playerAttacked = False
        if type(botChoice) == tuple:
            botSwitch(botTeam, botChoice[1])
            bot = botTeam[0]
            botAttacked = False
        if bot.finalStats["SPE"] > player.finalStats["SPE"]:
            moveOrder = [(bot, botAttacked), (player, playerAttacked)]
        else:
            moveOrder = [(player, playerAttacked), (bot, botAttacked)]
        if moveOrder[1][1] == False:
            moveOrder.pop(1)
        if moveOrder[0][1] == False:
            moveOrder.pop(0)
        if len(moveOrder) == 2: #priority check
            if moveNames[player.moveset[playerChoice][0]].priority > moveNames[bot.moveset[botChoice][0]].priority:
                moveOrder = [(player, playerAttacked), (bot, botAttacked)]
            elif moveNames[bot.moveset[botChoice][0]].priority > moveNames[player.moveset[playerChoice][0]].priority: 
                moveOrder = [(bot, botAttacked), (player, playerAttacked)]
        for attackerData in moveOrder:
            attacker = attackerData[0]
            if attacker.fainted == True:
                continue
            if attacker == player:
                defender = bot
                attackerChoice = playerChoice
            else:
                defender = player
                attackerChoice = botChoice
            botAttackSequence(attacker, defender, moveNames[attacker.moveset[attackerChoice][0]])
            attacker.moveset[attackerChoice][1] -= 1
            if defender.fainted == True:
                if defender == bot:
                    botTeam[-1] -= 1
                else:
                    playerTeam[-1] -= 1
    if playerTeam[0].fainted and playerTeam[-1] > 0:
        switchChoices = allPossibleSwitches(playerTeam)
        bestChoice, bestScore = 1, infinity
        for choice in switchChoices:
            playerTeamCopy, botTeamCopy = copy.deepcopy(playerTeam), copy.deepcopy(botTeam)
            newState = (playerTeamCopy, botTeamCopy)
            newScore = stateEvaluation(newState)
            if newScore < bestScore:
                bestChoice, bestScore = choice, newScore
        botSwitch(playerTeam, bestChoice)
    if botTeam[0].fainted and playerTeam[-1] > 0:
        switchChoices = allPossibleSwitches(playerTeam)
        bestChoice, bestScore = 1, -infinity
        for choice in switchChoices:
            playerTeamCopy, botTeamCopy = copy.deepcopy(playerTeam), copy.deepcopy(botTeam)
            newState = (playerTeamCopy, botTeamCopy)
            newScore = stateEvaluation(newState)
            if newScore > bestScore:
                bestChoice, bestScore = choice, newScore
        botSwitch(botTeam, bestChoice)
    return playerTeam, botTeam
        

###############################################################################
#state evaluation heuristic
def stateEvaluation(newState):
    playerTeam, botTeam = newState[0], newState[1]
    if playerTeam[-1] == 0: #game over states
        return infinity
    elif botTeam[-1] == 0:
        return -infinity
    score = 0
    bot, player = botTeam[0], playerTeam[0]
    monDifference = botTeam[-1] - playerTeam[-1]
    score += (monDifference * 50) #mon difference
    for playerMon in playerTeam[:-1]: #type matchups 
        for playerType in playerMon.types:
            for botType in bot.types:
                if playerType in resists[botType] or botType in weaknesses[playerType]:
                    score += 10
                if playerType in weaknesses[botType] or botType in resists[playerType]:
                    score -= 10
                if playerType in immunities[botType]:
                    score += 20
                elif botType in immunities[playerType]:
                    score -= 20
    for playerMon in playerTeam: #speed checks
        botSpeed, playerSpeed = bot.finalStats["SPE"], player.finalStats["SPE"]
        if botSpeed >= playerSpeed:
            if playerMon == player:
                score += 50
            else:
                score += 10
        else:
            if playerMon == player:
                score -= 50
            else:
                score -= 10
    return score

###############################################################################
#Mr. minmax himself
def minmax(state, depth, max):
    if depth == 0 or state[0][-1] == 0 or state[1][-1] == 0:
        return stateEvaluation(state)
    if max == True:
        bestScore = -infinity
        bestMove = 0
        for move in allBranches(state):
            playerMove, botMove = move[0], move[1]
            playerTeamCopy, botTeamCopy = copy.deepcopy(state[0]), copy.deepcopy(state[1])
            newState = botTurn(playerTeamCopy, playerMove, botTeamCopy, botMove)
            newEval = minmax(newState, depth - 1, False)
            if type(newEval) == tuple:
                newScore = newEval[0]
            else:
                newScore = newEval
            if newScore > bestScore:
                bestScore, bestMove = newScore, botMove
        return bestScore, bestMove
    else:
        bestScore = infinity
        bestMove = 0
        for move in allBranches(state):
            playerMove, botMove = move[0], move[1]
            playerTeamCopy, botTeamCopy = copy.deepcopy(state[0]), copy.deepcopy(state[1])
            newState = [playerTeamCopy, botTeamCopy]
            newState = botTurn(playerTeamCopy, playerMove, botTeamCopy, botMove)
            newEval = minmax(newState, depth - 1, False)
            if type(newEval) == tuple:
                newScore = newEval[0]
            else:
                newScore = newEval
            if newScore > bestScore:
                bestScore, bestMove = newScore, botMove
        return bestScore, bestMove

myTeam, theirTeam = copy.deepcopy(globalUserTeam), copy.deepcopy(globalFoeTeam)
testState = (myTeam, theirTeam)

print(minmax(testState, 3, True))

