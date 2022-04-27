#The main app. Run this to play!

from cmu_112_graphics import *
from moveClass import *
from monsterClass import *
from minmax import *

###############################################################################
#Variable assignments
def appStarted(app):
    app.mode = "titleMode"
    app.titleImage = app.loadImage("pmd.png")
    app.modeSelectImage = app.loadImage("ocean.png")
    app.teamSelectImage = app.loadImage("shaymins.jpg")
    app.helpSelectImage = app.loadImage("harmonica.jpg")
    app.battleBackground = app.scaleImage(app.loadImage("starlight.png"), 1/4)
    app.pokemonLogo = app.scaleImage(app.loadImage("logo.png"), 1)
    app.monSprites = dict()
    app.monIcons = dict()
    for mon in monNames: #assingns all sprites
        app.monSprites[mon] = dict()
        app.monSprites[mon]["front"] = app.loadImage(mon.upper() + "FRONT.png")
        app.monSprites[mon]["back"] = app.loadImage(mon.upper() + "BACK.png")
        for side in ["front", "back"]:
            app.monSprites[mon][side] = app.scaleImage(app.monSprites[mon][side], 2)
    app.helpMessage = '''This game is point and click. If at any time you wish to exit the current mode, press the "b" key.
                    \nTeam select: Here you pick which teams will be fought with.\nPress the "t" button to toggle which team you are selecting for.
                    \nBattle Mode: Pick your move/switch with a mouse click, and choose your switch with another click. \nIf you decide to cancel your switch, just click the pokemon currently in battle\nIf you press "r" at any time during the battle or on the result screen, the battle state will reset. 
                    \nThe battle state will also reset whenever you return to the mode selection screen.
                    \nEnjoy!'''
    app.choosingFor = True
    app.globalUserTeamName, app.globalUserTeam = teamTuples[0][0], teamTuples[0][1]
    app.globalFoeTeamName, app.globalFoeTeam = teamTuples[1][0], teamTuples[1][1]
    app.userTeam = copy.deepcopy(app.globalUserTeam)
    app.foeTeam = copy.deepcopy(app.globalFoeTeam)
    app.gameOver = False
    app.message = f'What will {app.userTeam[0]} do?'
    app.turnCount = 0
    app.attackChoice = 0
    app.switchChoice = 0
    app.userAttacked = True
    app.winQuote = ''
    app.winImage = app.loadImage("youwin.png")
    app.loseImage = app.scaleImage(app.loadImage("youlose.png"), 8/9)

###############################################################################
#Title screen
def titleMode_redrawAll(app, canvas):
    least =  min(app.width, app.height)
    canvas.create_image(app.width // 2, app.height // 2, 
                        image = ImageTk.PhotoImage(app.titleImage))
    canvas.create_text(app.width * .475, app.height // 7, 
                       text = "Showdown112!", fill = "black", 
                       font = f"Helvetica {int(.08 * least)} bold", anchor = W)
    canvas.create_text(app.width // 2, app.height * .3, 
                       text = "Press Enter...", fill = "black", 
                       font = f"Helvetica {int(.04 * least)} bold")
    canvas.create_text(app.width * .7, app.height * .975, 
                       text = "Peter Khoudary CMU 15-112 S22",fill = "black", 
                       font = f"Helvetica {int(.025 * least)} bold", anchor = W)
    canvas.create_image(app.width * .3, app.height // 7, 
                        image = ImageTk.PhotoImage(app.pokemonLogo))

def titleMode_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "modeSelect"

###############################################################################
#Mode select
def modeSelect_redrawAll(app, canvas):
    leftBound, rightBound = .2 * app.width, .8 * app.width
    least =  min(app.width, app.height)
    canvas.create_image(app.width // 2, app.height // 2, 
                        image = ImageTk.PhotoImage(app.modeSelectImage))
    #all boxes
    canvas.create_rectangle(leftBound, .1 * app.height, rightBound, .3 * app.height, fill = "black")
    canvas.create_text(app.width // 2, app.height * .2, text = "Information / Help",
                       fill = "light blue", font = f"Helvetica {int(.05 * least)} bold")
    canvas.create_rectangle(leftBound, .4 * app.height, rightBound, .6 * app.height, fill = "black")
    canvas.create_text(app.width // 2, app.height * .5, text = "Team Select",
                       fill = "light blue", font = f"Helvetica {int(.05 * least)} bold")
    canvas.create_rectangle(leftBound, .7 * app.height, rightBound, .9 * app.height, fill = "black")
    canvas.create_text(app.width // 2, app.height * .8, text = "Battle Start",
                       fill = "light blue", font = f"Helvetica {int(.05 * least)} bold")

def modeSelect_keyPressed(app, event):
    if event.key == "b":
        app.mode = "titleMode"

def modeSelect_mousePressed(app, event):
    leftBound, rightBound = .2 * app.width, .8 * app.width
    if leftBound < event.x < rightBound:
        if .7 * app.height < event.y < .9 * app.height:
            if app.gameOver:
                app.mode = "endScreen"
            else:
                app.mode = "battleMode"
        elif .4 * app.height < event.y < .6 * app.height:
            app.mode = "teamSelectMode"
        elif .1 * app.height < event.y < .3 * app.height:
            app.mode = "helpMode"

###############################################################################
#Help Mode
def helpMode_redrawAll(app, canvas):
    canvas.create_image(app.width // 2, app.height // 2, image = ImageTk.PhotoImage(app.helpSelectImage))
    canvas.create_rectangle(0, 0, app.width, app.height * .525, fill = "black")
    canvas.create_text(app.width * .01, app.height * .01, text = app.helpMessage,
            fill = "light blue", font = f"Helvetica {int(.015 * app.width)} bold", anchor = NW)

def helpMode_keyPressed(app, event):
    if event.key == "b":
        app.mode = "modeSelect"

###############################################################################
#Team select mode
def teamSelectMode_redrawAll(app, canvas):
    canvas.create_image(app.width // 2, app.height // 2, image = ImageTk.PhotoImage(app.teamSelectImage))
    drawTeamInfo(app, canvas)
    drawTeams(app, canvas)

def drawTeamInfo(app, canvas): #displays who has what team and who use is currently picking for
    canvas.create_text(app.width * .1, app.height * .05, text = f'Player Team: {app.globalUserTeamName}',
            fill = "black", font = f"Helvetica {int(.0175 * app.width)} bold", anchor = W)
    canvas.create_text(app.width * .9, app.height * .05, text = f'AI Team: {app.globalFoeTeamName}',
            fill = "black", font = f"Helvetica {int(.0175 * app.width)} bold", anchor = E)
    if app.choosingFor == True:
        beingChosen = "Player"
    else:
        beingChosen = "AI"
    canvas.create_rectangle(app.width // 4, app.height * .7, app.width * .75, app.height * .785, fill = "light blue")
    canvas.create_text(app.width // 2, app.height * .74, text = f'Choosing for: {beingChosen}', font = f"Helvetica {int(.0325 * app.width)} bold", fill = "black")

def drawTeams(app, canvas): #draws icon and team names for user to pick
    slot = 0
    leftBound, rightBound = .1 * app.width, .9 * app.width
    for teamTuple in teamTuples:
        teamName, team = teamTuple[0], teamTuple[1]
        canvas.create_rectangle(leftBound, app.height * .1 * (1 + slot), rightBound, .1 * app.height * (2 + slot ), fill = "black", outline = "white")
        canvas.create_text(app.width * .11, app.height * .1 * (1.5 + slot), text = f'{teamName}',
            fill = "light blue", font = f"Helvetica {int(.035 * app.width)} bold", anchor = W)
        for monSlot in range(len(team) - 1):
            canvas.create_image(app.width * .625 + app.width * .08 * (1 + monSlot), app.height * .1 * (1.5 + slot), image = ImageTk.PhotoImage(app.scaleImage(app.monSprites[team[monSlot].name]["front"], 1/5)))
        slot += 1

def teamSelectMode_mousePressed(app, event):
    if app.width * .1 <= event.x <= app.width * .9:
        if app.height * .1 <= event.y < app.height * .2:
            assignTeams(app, 0)
        elif app.height * .2 <= event.y < app.height * .3:
            assignTeams(app, 1)
        elif app.height * .3 <= event.y < app.height * .4:
            assignTeams(app, 2)
        elif app.height * .4 <= event.y < app.height * .5:
            assignTeams(app, 3)
        elif app.height * .5 <= event.y < app.height * .6:
            assignTeams(app, 4)

def teamSelectMode_keyPressed(app, event):
    if event.key == "b":
        teamRefresh(app)
        app.mode = "modeSelect"
    if event.key == "t":
        if app.choosingFor == False:
            app.choosingFor = True
        else:
            app.choosingFor = False

def assignTeams(app, choice): #sets the teams for the battle
    if app.choosingFor == True:
        app.globalUserTeamName, app.globalUserTeam = teamTuples[choice][0], teamTuples[choice][1]
    else:
        app.globalFoeTeamName, app.globalFoeTeam = teamTuples[choice][0], teamTuples[choice][1]
            
###############################################################################
#Battle mode
def battleMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_image(app.width // 2, app.height * .275, image = ImageTk.PhotoImage(app.battleBackground))
    drawPokemon(app, canvas)
    drawHUD(app, canvas)
    drawMoves(app, canvas)
    drawChat(app, canvas)

def battleMode_timerFired(app):
    if app.gameOver:
        if app.userTeam[-1] == 0:
            app.winner = app.foeTeam
            app.winQuote = "AI wins!"
        else:
            app.winner = app.userTeam
            app.winQuote = "Player wins!"
        app.mode = "endScreen"
            
def battleMode_keyPressed(app, event):
    if event.key == "r":
        teamRefresh(app)
    if event.key == "b":
        teamRefresh(app)
        app.mode = "modeSelect"

def drawChat(app, canvas): #draws textbox
    least = min(app.width, app.height)
    canvas.create_text(app.width * .01, app.height * .78, text = f"{app.message}", anchor = NW,
                            fill = "white", font = f"Helvetica {int(.015 * least)} bold")

def drawHUD(app, canvas): #draws health bars
    barLength = app.width * .35
    barWidth = app.height * .02
    userFill, foeFill = "green", "green"
    userPercent = app.userTeam[0].currentHP / app.userTeam[0].finalStats["HP"]
    foePercent = app.foeTeam[0].currentHP / app.foeTeam[0].finalStats["HP"]
    if userPercent <= .5:
        if userPercent <= .2:
            userFill = "red"
        else:
            userFill = "yellow"
    if foePercent <= .5:
        if foePercent <= .2:
            foeFill = "red"
        else:
            foeFill = "yellow"
    #User health bar
    canvas.create_rectangle(app.width * .63, app. height * .6, app.width, app.height * .7 + barWidth, fill = "silver")
    canvas.create_rectangle(app.width * .64, app. height * .65, app.width * .64 + barLength, app.height * .65 + barWidth, fill = None)
    canvas.create_rectangle(app.width * .64 + ((1 - userPercent) * barLength), app. height * .65, app.width * .64 + barLength, app.height * .65 + barWidth, fill = userFill)
    canvas.create_text(app.width * .64, app.height * .65, text = f"{app.userTeam[0].name}",
                            fill = "black", font = f"Helvetica {int(20)} bold", anchor = SW)
    canvas.create_text(app.width * .64, app.height * .67, text = f"Lv. {app.userTeam[0].level}",
                            fill = "black", font = f"Helvetica {int(20)} bold", anchor = NW)
    canvas.create_text(app.width * .99, app.height * .65, text = f"{round(app.userTeam[0].currentHP / app.userTeam[0].finalStats['HP'] * 100, 2)}%",
                            fill = "black", font = f"Helvetica {int(20)} bold", anchor = SE)
    canvas.create_text(app.width * .99, app.height * .67, text = f"{app.userTeam[0].currentHP}/{app.userTeam[0].finalStats['HP']}",
                            fill = "black", font = f"Helvetica {int(20)} bold", anchor = NE)
    #AI health bar
    canvas.create_rectangle(0, app. height * .025, app.width * .02 + barLength, app.height * .125 + barWidth, fill = "silver")
    canvas.create_rectangle(app.width * .01, app. height * .075, app.width * .01 + barLength, app.height * .075 + barWidth, fill = None)
    canvas.create_rectangle(app.width * .01, app. height * .075, app.width * .01 + barLength * foePercent, app.height * .075 + barWidth, fill = foeFill)
    canvas.create_text(app.width * .01, app.height * .075, text = f"{app.foeTeam[0].name}",
                            fill = "black", font = f"Helvetica {int(20)} bold", anchor = SW)
    canvas.create_text(app.width * .01, app.height * .095, text = f"Lv. {app.foeTeam[0].level}",
                            fill = "black", font = f"Helvetica {int(20)} bold", anchor = NW)
    canvas.create_text(app.width * .36, app.height * .075, text = f"{round(app.foeTeam[0].currentHP / app.foeTeam[0].finalStats['HP'] * 100, 2)}%",
                            fill = "black", font = f"Helvetica {int(20)} bold", anchor = SE)
    canvas.create_text(app.width * .36, app.height * .095, text = f"{app.foeTeam[0].currentHP}/{app.foeTeam[0].finalStats['HP']}",
                            fill = "black", font = f"Helvetica {int(20)} bold", anchor = NE)

def drawPokemon(app, canvas): #draws pokemon sprites
    if app.foeTeam[0].fainted == False:
        canvas.create_image(app.width * .74, app.height * .223, image = ImageTk.PhotoImage(app.monSprites[app.foeTeam[0].name]["front"]))
    if app.userTeam[0].fainted == False:
        canvas.create_image(app.width * .3, app.height * .5475, image = ImageTk.PhotoImage(app.monSprites[app.userTeam[0].name]["back"]))

def drawMoves(app, canvas): #draws moves
    least =  min(app.width, app.height)
    moveset = app.userTeam[0].moveset
    for moveSlot in range(len(moveset)):
        width = app.width // 5
        move = moveNames[moveset[moveSlot][0]]
        moveColor = moveColors[move.type]
        if move.type == "dark":
            textColor = "white"
        else:
            textColor = "black"
        canvas.create_rectangle(width * moveSlot, app. height * .9, width * moveSlot + width, app.height, fill = moveColor)
        canvas.create_text(width * moveSlot + width / 2, app.height * .93, text = f"{move.name}",
                            fill = textColor, font = f"Helvetica {int(.03 * least)} bold")
        canvas.create_text(width * moveSlot + width / 2, app.height * .97, text = f"{move.type[0].upper() + move.type[1:]}\t{moveset[moveSlot][1]}/{moveNames[move.name].PP}",
                            fill = textColor, font = f"Helvetica {int(.02 * least)} bold")
    canvas.create_rectangle(app.width - width, app. height * .9, app.width, app.height, fill = "white")
    canvas.create_text(width * 4 + width / 2, app.height * .95, text = "Switch",
                            fill = "black", font = f"Helvetica {int(.03 * least)} bold")

def battleMode_mousePressed(app, event):
    if app.gameOver:
        return
    else:
        if event.y > .9 * app.height:
            width = app.width // 5
            if event. x <= 4 * width:
                if 0 < event.x <= width:
                    app.attackChoice = 0
                    turn(app)
                elif width < event.x <= 2 * width:
                    app.attackChoice = 1
                    turn(app)
                elif 2 * width < event.x <= 3 * width:
                    app.attackChoice = 2
                    turn(app)
                elif 3 * width < event.x <= 4 * width:
                    app.attackChoice = 3
                    turn(app)
            else:
                app.mode = "switchMode"

def teamRefresh(app): #resets game state
    app.gameOver = False
    app.winQuote = ''
    app.userTeam = copy.deepcopy(app.globalUserTeam)
    app.foeTeam = copy.deepcopy(app.globalFoeTeam)
    app.message = f'What will {app.userTeam[0]} do?'
    app.turnCount = 0
            
def turn(app):
    user, foe = app.userTeam[0], app.foeTeam[0]
    userChoice = app.attackChoice
    userLeft, foeLeft = app.userTeam[-1], app.foeTeam[-1]
    if userLeft > 0 and foeLeft > 0: #game is over if one team has no living mons
        app.turnCount += 1
        userLeft, foeLeft = app.userTeam[-1], app.foeTeam[-1]
        userAttacked, foeAttacked = True, True
        app.message = f'Turn {app.turnCount}\n'
        foeChoice = minmax((app.userTeam, app.foeTeam), 2, True)[1] #this is the soul of the program, calls minmax to produce a best choice for AI
        if type(foeChoice) == list:
                switch(app, app.foeTeam, True) 
                foe = app.foeTeam[0]
                foeAttacked = False
        if userChoice == 4:
            app.message += f'{user.name} has switched in!\n'
            user = app.userTeam[0]
            userAttacked = False
        if foe.finalStats["SPE"] > user.finalStats["SPE"]: #speed checks
            moveOrder = [(foe, foeAttacked), (user, userAttacked)]
        else:
            moveOrder = [(user, userAttacked), (foe, foeAttacked)]
        if moveOrder[1][1] == False:
            moveOrder.pop(1)
        if moveOrder[0][1] == False:
            moveOrder.pop(0) #switch checking
        if len(moveOrder) == 2: #priority check
            if moveNames[user.moveset[userChoice][0]].priority > moveNames[foe.moveset[foeChoice][0]].priority:
                moveOrder = [(user, userAttacked), (foe, foeAttacked)]
            elif moveNames[foe.moveset[foeChoice][0]].priority > moveNames[user.moveset[userChoice][0]].priority: 
                moveOrder = [(foe, foeAttacked), (user, userAttacked)]
        for attackerData in moveOrder: #actually simulates the turn
            attacker = attackerData[0]
            if attacker.fainted == True:
                continue
            if attacker == user:
                defender = foe
                attackerChoice = userChoice
            else:
                defender = user
                attackerChoice = foeChoice
            attackSequence(app, attacker, defender, moveNames[attacker.moveset[attackerChoice][0]]) #damage and state calculator
            attacker.moveset[attackerChoice][1] -= 1
            if defender.fainted == True:
                if defender == foe:
                    app.foeTeam[-1] -= 1
                else:
                    app.userTeam[-1] -= 1
        if app.userTeam[-1] == 0 or app.foeTeam[-1] == 0:
            app.gameOver = True
            return
        if user.fainted == True:
            app.mode = "switchMode" #switches if the pokemon is dead, after the turn has ended
        if foe.fainted == True:
            switch(app, app.foeTeam, True)
    else:
        app.gameOver = True

def attackSequence(app, attacker, defender, move):
    missThreshold = move.accuracy * 100
    hitCheck = random.randint(1, 100) #miss potential, no damage
    if hitCheck > missThreshold:
        app.message += f"{attacker.name}'s {move.name} missed!\n"
        return
    percentBefore = round(defender.currentHP / defender.finalStats["HP"] * 100, 1)
    damage = (((((2 * attacker.level) / 5) + 2) * move.power * (attacker.finalStats[move.uses] / defender.finalStats[move.hits])) / 50) + 2 #official pokemon damage formula
    if move.type in attacker.types: #STAB (same type attack bonus)
        damage *= 1.5
    roll = random.randint(85,100) #gives a roll
    damage = roundHalfUp(damage * roll / 100)
    critChance = random.randint(1, 16) #crits
    if critChance == 1:
        damage = 1.5 * roundHalfUp(damage * 1.5)
    damageBeforeTypes = damage
    for defenseType in defender.types: #type effectiveness multipliers
        if move.type in resists[defenseType]:
            damage /= 2
        elif move.type in weaknesses[defenseType]:
            damage *= 2
        elif move.type in immunities[defenseType]:
            app.message += f"{defenseType[0].upper() + defenseType[1:]} types are immune to {attacker.name}'s {move.name}... \n" #if immune return no damage
            return 
    defender.currentHP -= damage
    percentDamage = round(damage / defender.finalStats["HP"] * 100, 1)
    if percentDamage > percentBefore:
        percentDamage = percentBefore
    percentAfter = round(defender.currentHP / defender.finalStats["HP"] * 100, 1)
    if percentAfter <= 0:
        percentAfter = 0
    app.message += f"{attacker.name}'s {move.name} takes {percentDamage}% of {defender.name}'s HP! "
    if critChance == 1: #checks to see what needs to be added to the message
        app.message += "A critical hit! "
    if damage < damageBeforeTypes:
        app.message += "It's not very effective..."
    elif damage > damageBeforeTypes:
        app.message += "It's super effective!"
    app.message += f" {defender.name} has {percentAfter}% HP left.\n"
    if defender.currentHP <= 0: # if dead modify object
        defender.currentHP = 0
        app.message += f"{defender.name} fainted!\n"
        defender.fainted = True

###############################################################################
#Switch Mode
def switchMode_mousePressed(app, event):
    if event.y < .9 * app.width:
        width = app.width // 3
        if 0 < event.x <= width:
            app.switchChoice = 0
        elif width < event.x <= 2 * width:
            app.switchChoice = 1
        elif 2 * width < event.x <= 3 * width:
            app.switchChoice = 2
        if app.switchChoice >= len(app.userTeam) - 1: # all the following conditionals merely ensure it is a legal switch
            return
        if app.userTeam[app.switchChoice].fainted == True:
            app.message = f'{app.userTeam[app.switchChoice]} has no energy left to battle!\n'
            return
        if app.userTeam[app.switchChoice] == app.userTeam[0]: #if you're cancelling a switch
            app.mode = "battleMode"
            return
        if app.userTeam[0].fainted == False: # if it's a regular switch
            switch(app, app.userTeam)
            app.attackChoice = 4
            app.mode = "battleMode"
            turn(app)
        else: #if you're switching because you died
            switch(app, app.userTeam)
            app.mode = "battleMode"
    
def switch(app, team, bot = False):
    if team[-1] == 0:
        app.gameOver = True
        return
    elif bot: #if bot then don't use user input
        botMon = team[bestSwitch(app.userTeam, app.foeTeam, True)] #calls the state evaluator on every possible switch
        team.remove(botMon)
        team.insert(0, botMon)  
        app.message += f"{botMon.name} has switched in!\n"
        return 
    newMon = team[app.switchChoice] #switches the mon
    team.remove(newMon)
    team.insert(0, newMon)
    app.message += f"{newMon.name} has switched in!\n"
    app.mode = "battleMode"
    return

def switchMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_image(app.width // 2, app.height * .275, image = ImageTk.PhotoImage(app.battleBackground))
    drawPokemon(app, canvas)
    drawHUD(app, canvas)
    drawSwitch(app, canvas)
    drawChat(app, canvas)

def drawSwitch(app, canvas): #draws the switch possibilites instead of moves
    width = app.width // 3
    for monSlot in range(len(app.userTeam) - 1):
        percent = app.userTeam[monSlot].currentHP / app.userTeam[monSlot].finalStats["HP"]
        if app.userTeam[monSlot].fainted == True:
            fill = "black"
        elif percent <= .5:
            if percent <= .2:
                fill = "red"
            else:
                fill = "yellow"
        else:
            fill = "green"
        canvas.create_rectangle(width * monSlot, app. height * .9, width * monSlot + width, app.height, fill = fill)
        canvas.create_image(width * (.5 +  monSlot), app.height * .95, image = ImageTk.PhotoImage(app.scaleImage(app.monSprites[app.userTeam[monSlot].name]["front"], 1/5)))

###############################################################################
#Win screen
def endScreen_keyPressed(app, event): #restarts
    if event.key == "r":
        teamRefresh(app)
        app.mode = "battleMode"
    if event.key == "b":
        teamRefresh(app)
        app.mode = "modeSelect"

def endScreen_redrawAll(app, canvas):
    drawVictoryQuote(app, canvas)
    drawVictoryMons(app, canvas)
    drawFinalTurn(app, canvas)

def drawFinalTurn(app, canvas): #shows what happened on final turn since timerFired truncates it immediately
    splitMessage = app.message.splitlines()
    splitMessage[0] = "Final Turn"
    splitMessage = "\n".join(splitMessage)
    canvas.create_text(app.width * .5, app.height * .4, text = f"{splitMessage}",
                            fill = "black", font = f"Helvetica {int(15)} bold")

def drawVictoryMons(app, canvas): #draws the mons from the winning team
    width = app.width // 3
    team = app.winner
    for monSlot in range(len(team) - 1):
        canvas.create_image(app.width * .2 + (monSlot * width), app.height * .775, image = ImageTk.PhotoImage(app.monSprites[team[monSlot].name]["front"]))

def drawVictoryQuote(app, canvas): #winning decal
    if app.winner == app.userTeam:
        canvas.create_image(app.width * .5, app.height * .2, image = ImageTk.PhotoImage(app.winImage))
    else:
        canvas.create_image(app.width * .5, app.height * .175, image = ImageTk.PhotoImage(app.loseImage))

runApp(width = 1200, height = 700)