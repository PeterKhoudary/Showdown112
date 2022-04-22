from cmu_112_graphics import *
from turn import *
from damageCalc import *
from moveClass import *
from monsterClass import *
import asyncio

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
    app.switch = False
    app.gameOver = False
    app.message = ""
    app.waitingForInput = False
    app.userChoice = None

###############################################################################
#Title Screen
def splashScreenMode_redrawAll(app, canvas):
    least =  min(app.width, app.height)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width // 2, app.height // 5, text = "Pokemon Showdown112!",
    fill = "silver", font = f"Helvetica {int(.08 * least)} bold")
    canvas.create_text(app.width // 2, app.height * .3, text = "#SunsIn4",
    fill = "silver", font = f"Helvetica {int(.04 * least)} bold")
    canvas.create_text(app.width // 2, app.height * .9, text = "Press Enter...",
    fill = "silver", font = f"Helvetica {int(.03 * least)} bold")
    canvas.create_image(app.width // 2, app.height * .6, image = ImageTk.PhotoImage(app.pokemonLogoStart))

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
    if event.key == "Enter":
        app.mode = "splashScreenMode"

def modeSelect_mousePressed(app, event):
    leftBound, rightBound = .2 * app.width, .8 * app.width
    if leftBound < event.x < rightBound:
        if .7 * app.height < event.y < .9 * app.height:
            app.mode = "battleMode"
            turn(app, userTeam[0], userTeam, foeTeam[0], foeTeam)
            
###############################################################################

#Battle Mode
def battleMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_image(app.width // 2, app.height * .275, image = ImageTk.PhotoImage(app.battleBackground))
    drawPokemon(app, canvas)
    drawHUD(app, canvas)
    drawChat(app, canvas)
    if app.switch == True:
        drawSwitch(app, canvas)
    else:
        drawMoves(app, canvas)
    

def battleMode_timerFired(app):
    if app.gameOver == True:
        if userTeam[-1] == 0:
            app.message = "AI wins!"
        else:
            app.message = "Player wins!"
        
def battleMode_keyPressed(app, event):
    #if event.key == "r":
        #battleRematch(app)
    if event.key == "enter":
        app.mode == "splashScreenMode"

def drawChat(app, canvas):
    least = min(app.width, app.height)
    canvas.create_text(app.width * .01, app.height * .78, text = f"{app.message}", anchor = NW,
                            fill = "white", font = f"Helvetica {int(.069 * least)} bold")

def drawHUD(app, canvas):
    barLength = app.width * .4
    barWidth = app.height * .05
    userFill, foeFill = "green", "green"
    userPercent = userTeam[0].currentHP / userTeam[0].finalStats["HP"]
    foePercent = foeTeam[0].currentHP / foeTeam[0].finalStats["HP"]
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
    if foeTeam[0].fainted == False:
        canvas.create_image(app.width * .74, app.height * .223, image = ImageTk.PhotoImage(app.monSprites[foeTeam[0].name]["front"]))
    if userTeam[0].fainted == False:
        canvas.create_image(app.width * .3, app.height * .542, image = ImageTk.PhotoImage(app.monSprites[userTeam[0].name]["back"]))

def drawMoves(app, canvas):
    least =  min(app.width, app.height)
    moveset = userTeam[0].moveset
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

def drawSwitch(app, canvas):
    width = app.width // 5
    for monSlot in range(len(userTeam) - 1):
        if userTeam[monSlot].fainted == True:
            fill = "red"
        else:
            fill = "white"
        canvas.create_rectangle(width * monSlot, app. height * .9, width * monSlot + width, app.height, fill = fill)
        canvas.create_image (width * (.5 +  monSlot), app.height * .95, image = ImageTk.PhotoImage(app.scaleImage(app.monSprites[userTeam[monSlot].name]["front"], 1/5)))

def turn(app, user, userTeam, foe, foeTeam):
    userChoice = app.userChoice
    userLeft, foeLeft = userTeam[-1], foeTeam[-1]
    while userLeft > 0 and foeLeft > 0:
        print(f'user mons = {userLeft}, bot mons = {foeLeft}')
        if user.fainted == True:
            app.switch = True
            newUser = switch(app, user, userTeam)
            user = newUser
        if foe.fainted == True:
            newFoe = switch(app, foe, foeTeam, True)
            foe = newFoe
        userLeft, foeLeft = userTeam[-1], foeTeam[-1]
        userAttacked, foeAttacked = True, True
        # foeChoice = random.randint(0, 4) #random AI choice
        # while foeChoice == 4 and foeTeam[-1] == 1:
        #     foeChoice = random.randint(0, 4)
        # if foeChoice == 4:
        #     newFoe = switch(foe, foeTeam, True) 
        #     foeAttacked = False
        #     foe = newFoe
        app.message = f"What will {user.name} do?"
        userChoice = int(app.getUserInput("Enter a moveslot 0 - 3, or 4 to switch"))
        if userChoice == 4:
            if userTeam[-1] == 1:
                while userChoice == 4:
                    app.message = "You have no other remaining pokemon! Pick another"
                    userChoice = int(app.getUserInput("Enter a moveslot 0 - 3"))
            else:
                app.switch = True
                newUser = switch(app, user, userTeam) 
                userAttacked = False
                user = newUser
        foeChoice = random.randint(0, 4) #random AI choice
        if foeChoice == 4:
            if foeTeam[-1] == 1:
                while foeChoice == 4:
                    foeChoice = random.randint(0, 4)
            else:
                newFoe = switch(app, foe, foeTeam, True) 
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
            attackSequence(app, attacker, defender, moveNames[attacker.moveset[attackerChoice][0]])
            attacker.moveset[attackerChoice][1] -= 1
            if defender.fainted == True:
                if defender == foe:
                    foeTeam[-1] -= 1
                else:
                    userTeam[-1] -= 1
            userLeft, foeLeft = userTeam[-1], foeTeam[-1]
    print(userTeam[-1], foeTeam[-1])
    app.gameOver = True

def attackSequence(app, attacker, defender, move):
    app.message = f"{attacker.name} used {move.name}"
    missThreshold = move.accuracy * 100
    hitCheck = random.randint(1, 100)
    if hitCheck > missThreshold:
        app.message = f"{attacker.name}'s attack missed!"
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
            app.message = f'{defenseType} types are immune to {move}'
            return 
    defender.currentHP -= damage
    percentDamage = round(damage / defender.finalStats["HP"] * 100, 1)
    if percentDamage > percentBefore:
        percentDamage = percentBefore
    percentAfter = round(defender.currentHP / defender.finalStats["HP"] * 100, 1)
    if percentAfter <= 0:
        percentAfter = 0
    app.message = f"{attacker.name}'s {move.name} takes {percentDamage}% of {defender.name}'s HP!"
    if critChance == 1:
        app.message = "A critical hit!"
    if damage < damageBeforeTypes:
        app.message = "It's not very effective..."
    elif damage > damageBeforeTypes:
        app.message = "It's super effective!"
    app.message = f"{defender.name} has {percentAfter}% HP left."
    if defender.currentHP <= 0:
        defender.currentHP = 0
        app.message = f"{defender.name} fainted!"
        defender.fainted = True

def switch(app, currentMon, team, bot = False):
    if bot:
        botChoice = random.randint(0, len(team) - 2)
        botMon = team[botChoice]
        while botMon == currentMon or botMon.fainted == True:
            botChoice = random.randint(0, len(team) - 2)
            botMon = team[botChoice]
        team.remove(botMon)
        team.insert(0, botMon)  
        app.message = f"{botMon.name} has switched in!"
        return botMon
    app.message = "Here's your team"
    # teamNameMap = dict()
    # for teamMon in team:
    #     if type(teamMon) == int:
    #         continue
    #     if teamMon.fainted == True:
    #         app.message = teamMon.name + " (fainted)"
    #     else:
    #         app.message = teamMon.name
    #     teamNameMap[teamMon.name] = teamMon
    foundMon = False
    while foundMon == False:
        teamSlot = int(app.getUserInput("Pick a member to switch in: "))
        newMon = team[teamSlot]
        if newMon.fainted == True:
            app.message = f"{newMon.name} has no energy left to battle!"
        elif newMon == currentMon:
            app.message = "You can't cancel a switch!"
        else:
            foundMon = True
    team.remove(newMon)
    team.insert(0, newMon)
    app.message = f"{newMon.name} has switched in!"
    app.switch = False
    return newMon

def battleMode_mousePressed(app, event):
    if event.y >= .9 * app.height:
        if app.switch == True:
            width = app.width // 6
            if 0 < event.x <= width:
                app.userChoice = 0
            elif width < event.x <= 2 * width:
                app.userChoice = 1
            elif 2 * width < event.x <= 3 * width:
                app.userChoice = 2
            elif 3 * width < event.x <= 4 * width:
                app.userChoice = 3
            elif 4 * width < event.x <= 5 * width:
                app.userChoice = 4
            else:
                app.userChoice = 5
        else:
            width = app.width // 5
            if 0 < event.x <= width:
                app.userChoice = 0
            elif width < event.x <= 2 * width:
                app.userChoice = 1
            elif 2 * width < event.x <= 3 * width:
                app.userChoice = 2
            elif 3 * width < event.x <= 4 * width:
                app.userChoice = 3
            else:
                app.userChoice = 4
    print(app.userChoice)

runApp(width = 1200, height = 700)