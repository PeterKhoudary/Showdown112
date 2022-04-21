from cmu_112_graphics import *
from turn import *
from damageCalc import *
from moveClass import *
from monsterClass import *

###############################################################################
#Main App
def appStarted(app):
    app.pokemonLogo = app.loadImage("pokemonLogo.png")
    app.pokemonLogoStart = app.scaleImage(app.pokemonLogo, 1/4)
    app.mode = "splashScreenMode"
    app.battleBackground = app.loadImage("starlight.png")
    app.battleBackground = app.scaleImage(app.battleBackground, 1/4)
    app.monSprites = dict()
    for mon in monNames:
        app.monSprites[mon] = dict()
        app.monSprites[mon]["front"] = app.loadImage(mon.upper() + "FRONT.png")
        app.monSprites[mon]["front"] = app.scaleImage(app.monSprites[mon]["front"], 2)
        app.monSprites[mon]["back"] = app.loadImage(mon.upper() + "BACK.png")
        app.monSprites[mon]["back"] = app.scaleImage(app.monSprites[mon]["back"], 2)

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
            
###############################################################################

#Battle Mode
def battleMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_image(app.width // 2, app.height * .275, image = ImageTk.PhotoImage(app.battleBackground))
    drawPokemon(app, canvas)
    drawMoves(app, canvas)
    drawHUD(app, canvas)
    drawChat(app, canvas)

def drawChat(app, canvas, message = "bruh"):
    least = min(app.width, app.height)
    canvas.create_text(app.width * .01, app.height * .78, text = f"{message}", anchor = NW,
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
    canvas.create_rectangle(app.width * .01, app. height * .05, app.width * .01 + barLength, app.height * .05 + barWidth, fill = "white")
    canvas.create_rectangle(app.width * .01, app. height * .05, app.width * .01 + barLength * userPercent, app.height * .05 + barWidth, fill = userFill)
    canvas.create_rectangle(app.width * .05, app. height * .2, app.width * .05 + barLength, app.height * .2 + barWidth, fill = "white")
    canvas.create_rectangle(app.width * .05, app. height * .2, app.width * .05 + barLength * foePercent, app.height * .2 + barWidth, fill = foeFill)
    
def drawPokemon(app, canvas):
    canvas.create_image(app.width * .75, app.height * .225, image = ImageTk.PhotoImage(app.monSprites[foeTeam[0].name]["front"]))
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
        canvas.create_text(width * moveSlot + width / 2, app.height * .97, text = f"{moveset[moveSlot][1]}/{moveNames[move.name].PP}",
                            fill = textColor, font = f"Helvetica {int(.02 * least)} bold")
    canvas.create_rectangle(app.width - width, app. height * .9, app.width, app.height, fill = "white")
    canvas.create_text(width * 4 + width / 2, app.height * .95, text = "Switch",
                            fill = "black", font = f"Helvetica {int(.03 * least)} bold")

def battleMode_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "modeSelect"

runApp(width = 1200, height = 700)