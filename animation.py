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
    app.keldeo = app.loadImage("keldeoFront.png")
    app.keldeo = app.scaleImage(app.keldeo, 2/3)
    #app.battleBackground = app.loadImage("starlight.png")
    #app.battleBackground = app.scaleImage(app.battleBackground, 1/4)

###############################################################################
#Title Screen
def splashScreenMode_redrawAll(app, canvas):
    least =  min(app.width, app.height)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width // 2, app.height // 5, text = "Pokemon Showdown112!",
    fill = "silver", font = f"Helvetica {int(.08 * least)} bold")
    canvas.create_text(app.width // 2, app.height * .3, text = "#Agency",
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
    #canvas.create_image(app.width // 2, app.height // 2, image = ImageTk.PhotoImage(app.battleBackground))
    canvas.create_image(app.width * .8, app.height * .3, image = ImageTk.PhotoImage(app.keldeo))

def battleMode_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "modeSelect"


runApp(width = 1200, height = 700)