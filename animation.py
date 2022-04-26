from cmu_112_graphics import *
from turn import *
from damageCalc import *
from moveClass import *
from monsterClass import *

#ONCE MINMAX IS FINISHED REMOVE ALL RANDOM ELEMENTS AND SWITCH PROPER

###############################################################################
#Main App
def appStarted(app):
    app.mode = "splashScreenMode"
    app.battleBackground = app.scaleImage(app.loadImage("starlight.png"), 1/4)
    app.pokemonLogoStart = app.scaleImage(app.loadImage("pokemonLogo.png"), 1/4)
    app.monSprites = dict()
    app.monIcons = dict()
    for mon in monNames:
        app.monSprites[mon] = dict()
        app.monSprites[mon]["front"] = app.loadImage(mon.upper() + "FRONT.png")
        app.monSprites[mon]["back"] = app.loadImage(mon.upper() + "BACK.png")
        for side in ["front", "back"]:
            app.monSprites[mon][side] = app.scaleImage(app.monSprites[mon][side], 2)
    app.userTeam = copy.deepcopy(globalUserTeam)
    app.foeTeam = copy.deepcopy(globalFoeTeam)
    app.gameOver = False
    app.message = f'What will {app.userTeam[0]} do?'
    app.turnCount = 0
    app.attackChoice = 0
    app.switchChoice = 0
    app.userAttacked = True
    app.winQuote = ''

###############################################################################
#Title Screen
def splashScreenMode_redrawAll(app, canvas):
    least =  min(app.width, app.height)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width // 2, app.height // 5, 
                       text = "Pokemon Showdown112!", fill = "silver", 
                       font = f"Helvetica {int(.08 * least)} bold")
    canvas.create_text(app.width // 2, app.height * .3, 
                       text = "#Agency", fill = "silver", 
                       font = f"Helvetica {int(.04 * least)} bold")
    canvas.create_text(app.width // 2, app.height * .9, 
                       text = "Press Enter...",fill = "silver", 
                       font = f"Helvetica {int(.03 * least)} bold")
    canvas.create_image(app.width // 2, app.height * .6, 
                        image = ImageTk.PhotoImage(app.pokemonLogoStart))

def splashScreenMode_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "modeSelect"

###############################################################################
#Mode select
def modeSelect_redrawAll(app, canvas):
    leftBound, rightBound = .2 * app.width, .8 * app.width
    least =  min(app.width, app.height)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_rectangle(leftBound, .1 * app.height, rightBound, .3 * app.height, fill = "white")
    canvas.create_text(app.width // 2, app.height * .2, text = "Teambuilder",
    fill = "Blue", font = f"Helvetica {int(.05 * least)} bold")
    canvas.create_rectangle(leftBound, .4 * app.height, rightBound, .6 * app.height, fill = "white")
    canvas.create_text(app.width // 2, app.height * .5, text = "Premade Teams",
    fill = "Blue", font = f"Helvetica {int(.05 * least)} bold")
    canvas.create_rectangle(leftBound, .7 * app.height, rightBound, .9 * app.height, fill = "white")
    canvas.create_text(app.width // 2, app.height * .8, text = "Battle Start",
    fill = "Blue", font = f"Helvetica {int(.05 * least)} bold")

def modeSelect_keyPressed(app, event):
    if event.key == "b":
        app.mode = "splashScreenMode"

def modeSelect_mousePressed(app, event):
    leftBound, rightBound = .2 * app.width, .8 * app.width
    if leftBound < event.x < rightBound:
        if .7 * app.height < event.y < .9 * app.height:
            app.mode = "battleMode"
            
###############################################################################
#Battle Mode
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
            
def battleMode_keyPressed(app, event):
    if event.key == "r":
        app.gameOver = False
        app.winQuote = ''
        app.userTeam = copy.deepcopy(globalUserTeam)
        app.foeTeam = copy.deepcopy(globalFoeTeam)
        app.message = f'What will {app.userTeam[0]} do?'
        app.turnCount = 0
    if event.key == "b":
        app.mode = "modeSelect"

def drawChat(app, canvas):
    least = min(app.width, app.height)
    canvas.create_text(app.width * .01, app.height * .78, text = f"{app.message}", anchor = NW,
                            fill = "white", font = f"Helvetica {int(.015 * least)} bold")
    if app.gameOver:
        canvas.create_text(app.width * .5, app.height * .25, text = f"{app.winQuote}",
                            fill = "orange", font = f"Times {int(.225 * least)} bold")

def drawHUD(app, canvas):
    barLength = app.width * .4
    barWidth = app.height * .05
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
    canvas.create_rectangle(app.width * .01, app. height * .05, app.width * .01 + barLength, app.height * .05 + barWidth, fill = None)
    canvas.create_rectangle(app.width * .01, app. height * .05, app.width * .01 + barLength * userPercent, app.height * .05 + barWidth, fill = userFill)
    canvas.create_rectangle(app.width * .05, app. height * .2, app.width * .05 + barLength, app.height * .2 + barWidth, fill = None)
    canvas.create_rectangle(app.width * .05, app. height * .2, app.width * .05 + barLength * foePercent, app.height * .2 + barWidth, fill = foeFill)
    
def drawPokemon(app, canvas):
    if app.foeTeam[0].fainted == False:
        canvas.create_image(app.width * .74, app.height * .223, image = ImageTk.PhotoImage(app.monSprites[app.foeTeam[0].name]["front"]))
    if app.userTeam[0].fainted == False:
        canvas.create_image(app.width * .3, app.height * .542, image = ImageTk.PhotoImage(app.monSprites[app.userTeam[0].name]["back"]))

def drawMoves(app, canvas):
    least =  min(app.width, app.height)
    moveset = app.userTeam[0].moveset
    for moveSlot in range(len(moveset)):
        width = app.width // 5
        move = moveNames[moveset[moveSlot][0]]
        moveColor = moveColors[move.type]
        if move.type == "dark":
            textColor = "white"
        else:
            textColor = "Black"
        canvas.create_rectangle(width * moveSlot, app. height * .9, width * moveSlot + width, app.height, fill = moveColor)
        canvas.create_text(width * moveSlot + width / 2, app.height * .93, text = f"{move.name}",
                            fill = textColor, font = f"Helvetica {int(.03 * least)} bold")
        canvas.create_text(width * moveSlot + width / 2, app.height * .97, text = f"{moveset[moveSlot][1]} / {moveNames[move.name].PP}",
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
            
def turn(app):
    user, foe = app.userTeam[0], app.foeTeam[0]
    userChoice = app.attackChoice
    userLeft, foeLeft = app.userTeam[-1], app.foeTeam[-1]
    if userLeft > 0 and foeLeft > 0:
        app.turnCount += 1
        print(f'user mons = {userLeft}, bot mons = {foeLeft}')
        userLeft, foeLeft = app.userTeam[-1], app.foeTeam[-1]
        userAttacked, foeAttacked = True, True
        app.message = f'Turn {app.turnCount}\n'
        # placeholder for minmax
        if userChoice == 4:
            app.message += f'{user.name} has switched in!\n'
            user = app.userTeam[0]
            userAttacked = False
        foeChoice = random.randint(0, 4) #random AI choice
        if foeChoice == 4:
            if app.foeTeam[-1] == 1:
                while foeChoice == 4:
                    foeChoice = random.randint(0, 4)
            else:
                switch(app, app.foeTeam, True) 
                foe = app.foeTeam[0]
                foeAttacked = False
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
            attackSequence(app, attacker, defender, moveNames[attacker.moveset[attackerChoice][0]])
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
            app.mode = "switchMode"
        if foe.fainted == True:
            switch(app, app.foeTeam, True)
    else:
        app.gameOver = True

def attackSequence(app, attacker, defender, move):
    missThreshold = move.accuracy * 100
    hitCheck = random.randint(1, 100)
    if hitCheck > missThreshold:
        app.message += f"{attacker.name}'s {move.name} missed!\n"
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
            app.message += f"{defenseType[0].upper() + defenseType[1:]} types are immune to {attacker.name}'s {move.name}... \n"
            return 
    defender.currentHP -= damage
    percentDamage = round(damage / defender.finalStats["HP"] * 100, 1)
    if percentDamage > percentBefore:
        percentDamage = percentBefore
    percentAfter = round(defender.currentHP / defender.finalStats["HP"] * 100, 1)
    if percentAfter <= 0:
        percentAfter = 0
    app.message += f"{attacker.name}'s {move.name} takes {percentDamage}% of {defender.name}'s HP! "
    if critChance == 1:
        app.message += "A critical hit! "
    if damage < damageBeforeTypes:
        app.message += "It's not very effective..."
    elif damage > damageBeforeTypes:
        app.message += "It's super effective!"
    app.message += f" {defender.name} has {percentAfter}% HP left.\n"
    if defender.currentHP <= 0:
        defender.currentHP = 0
        app.message += f"{defender.name} fainted!\n"
        defender.fainted = True

###############################################################################
#Switch Mode
def switchMode_mousePressed(app, event):
    if event.y < .9 * app.width:
        width = app.width // 6
        if 0 < event.x <= width:
            app.switchChoice = 0
        elif width < event.x <= 2 * width:
            app.switchChoice = 1
        elif 2 * width < event.x <= 3 * width:
            app.switchChoice = 2
        elif 3 * width < event.x <= 4 * width:
            app.switchChoice = 3
        elif 4 * width < event.x <= 5 * width:
            app.switchChoice = 4
        else:
            app.switchChoice = 5
        if app.switchChoice >= len(app.userTeam) - 1:
            return
        if app.userTeam[app.switchChoice].fainted == True:
            app.message = f'{app.userTeam[app.switchChoice]} has no energy left to battle!\n'
            return
        if app.userTeam[app.switchChoice] == app.userTeam[0]:
            app.mode = "battleMode"
            return
        if app.userTeam[0].fainted == False:
            switch(app, app.userTeam)
            app.attackChoice = 4
            app.mode = "battleMode"
            turn(app)
        else:
            switch(app, app.userTeam)
            app.mode = "battleMode"
    
def switch(app, team, bot = False):
    currentMon = team[0]
    if team[-1] == 0:
        app.gameOver = True
        return
    elif bot:
        botChoice = random.randint(0, len(team) - 2)
        botMon = team[botChoice]
        while botMon == currentMon or botMon.fainted == True:
            botChoice = random.randint(0, len(team) - 2)
            botMon = team[botChoice]
        team.remove(botMon)
        team.insert(0, botMon)  
        app.message += f"{botMon.name} has switched in!\n"
        return 
    newMon = team[app.switchChoice]
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

def drawSwitch(app, canvas):
    width = app.width // 6
    for monSlot in range(len(app.userTeam) - 1):
        if app.userTeam[monSlot].fainted == True:
            fill = "red"
        else:
            fill = "white"
        canvas.create_rectangle(width * monSlot, app. height * .9, width * monSlot + width, app.height, fill = fill)
        canvas.create_image(width * (.5 +  monSlot), app.height * .95, image = ImageTk.PhotoImage(app.scaleImage(app.monSprites[app.userTeam[monSlot].name]["front"], 1/5)))

runApp(width = 1200, height = 700)