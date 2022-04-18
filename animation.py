from cmu_112_graphics import *

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "light blue")
    canvas.create_text(app.width // 2, app.height // 4, text = "Pokemon Showdown!",
    fill = "dark blue", font = f"Helvetica {int(.05 * app.height)} bold")
    canvas.create_text(app.width // 2, app.height // 3, text = "112 Edition",
    fill = "dark blue", font = f"Helvetica {int(.03 * app.height)} bold")
    canvas.create_text(app.width // 2, app.height * .9, text = "Press Enter",
    fill = "dark blue", font = f"Helvetica {int(.03 * app.height)} bold")


runApp(width = 800, height = 800)