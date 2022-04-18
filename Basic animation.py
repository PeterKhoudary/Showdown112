from cmu_112_graphics import *

def appStarted(app):
    app.pokemonLogo = app.loadImage("pokemonLogo.png")
    app.pokemonLogoStart = app.scaleImage(app.pokemonLogo, 1/4)

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width // 2, app.height // 5, text = "Pokemon Showdown112!",
    fill = "silver", font = f"Helvetica {int(.08 * min(app.width, app.height))} bold")
    canvas.create_text(app.width // 2, app.height * .3, text = "#Agency",
    fill = "silver", font = f"Helvetica {int(.04 * min(app.width, app.height))} bold")
    canvas.create_text(app.width // 2, app.height * .9, text = "Press Enter...",
    fill = "silver", font = f"Helvetica {int(.03 * min(app.width, app.height))} bold")
    canvas.create_image(app.width // 2, app.height * .6, image = ImageTk.PhotoImage(app.pokemonLogoStart))

runApp(width = 1200, height = 700)