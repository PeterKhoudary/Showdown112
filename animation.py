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
    canvas.create_image(app.width // 2, app.height // 3, image = ImageTk.PhotoImage(app.battleBackground))
    drawPokemon(app, canvas)
    drawMoves(app, canvas)
    
def drawPokemon(app, canvas):
    canvas.create_image(app.width * .75, app.height * .25, image = ImageTk.PhotoImage(app.monSprites[foeTeam[0].name]["front"]))
    canvas.create_image(app.width * .3, app.height * .6, image = ImageTk.PhotoImage(app.monSprites[userTeam[0].name]["back"]))

def drawMoves(app, canvas):
    least =  min(app.width, app.height)
    moveset = userTeam[0].moveset
    slot = 0
    for moveSlot in moveset:
        width = app.width // 5
        move = moveNames[moveSlot[0]]
        moveColor = moveColors[move.type]
        if move.type == "dark":
            textColor = "white"
        else:
            textColor = "Black"
        canvas.create_rectangle(width * slot, app. height * .83, width * slot + width, app.height, fill = moveColor)
        if len(move.name.split(" ")) == 2:
            first = move.name.split(" ")[0]
            second = move.name.split(" ")[1]
            canvas.create_text(width * slot + width / 2, app.height * .875, text = f"{first}",
                            fill = textColor, font = f"Helvetica {int(.04 * least)} bold")
            canvas.create_text(width * slot + width / 2, app.height * .95, text = f"{second}",
                            fill = textColor, font = f"Helvetica {int(.04 * least)} bold")
        else:
            canvas.create_text(width * slot + width / 2, app.height * .915, text = f"{move.name}",
                            fill = textColor, font = f"Helvetica {int(.04 * least)} bold")
        slot += 1
    canvas.create_rectangle(app.width - width, app. height * .83, app.width, app.height, fill = "white")
    canvas.create_text(width * slot + width / 2, app.height * .915, text = "Switch",
                            fill = "black", font = f"Helvetica {int(.04 * least)} bold")

def battleMode_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "modeSelect"


runApp(width = 1200, height = 700)