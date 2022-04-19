# def reorderRainbow(allowedToFollow):
#     available = set(allowedToFollow)
#     return backtracker(allowedToFollow, available, [])

# def backtracker(allowedToFollow, available, order):
#     if available == set():
#         return order
#     for color in available:
#         if order == [] or color in allowedToFollow[order[-1]]:
#             order.append(color)
#             available.remove(color)
#             potentialSolution = backtracker(allowedToFollow, available, order)
#             if potentialSolution!= None:
#                 return potentialSolution
#             order.pop()
#             available.add(color)
#     return None

# allowedToFollow = {
# "red": {"yellow", "black"},
# "yellow": {"black", "blue"},
# "blue": {"black"},
# "black": {"red", "yellow", "blue"} }

# assert(reorderRainbow(allowedToFollow))
# print(reorderRainbow(allowedToFollow))

# # 112 Grade Explorer, S22

# # This does not take into account AMG grading, the Semester Grade Cap,
# # Academic integrity penalties, or the Participation requirements.  
# # See the syllabus for details.

# # Enter your grades here (estimate your tp3 and final exam grades):
# quizAvg      = 85.4
# hwAvg        = 99.9
# midtermAvg   = 76.3
# tp3          = 90      # guesstimate
# final        = 89 # default

# grade = round(0.10*quizAvg + 0.30*hwAvg + 0.20*midtermAvg +
#               0.20*tp3 + 0.20*final, 1)

# def letterGrade(grade):
#     if grade >= 89.5: return 'A'
#     elif grade >= 79.5: return 'B'
#     elif grade >= 69.5: return 'C'
#     elif grade >= 59.5: return 'D'
#     else: return 'R'

# print(f'Grade (with tp3={tp3} and final={final}) = {grade} ' +
#       f'--> {letterGrade(grade)}')

# print('*************************************')

# print('Final exam grades required given specific tp3 grades:')
# print('   -----    -----   -----   -----   -----')
# print('    tp3       A       B       C       D')
# print('   -----    -----   -----   -----   -----')
# for tp3 in range(100, 59, -5):
#     print(f'   {tp3:4}', end='')
#     gradeWithoutFinal = 0.10*quizAvg + 0.30*hwAvg + 0.20*midtermAvg + 0.20*tp3
#     for targetGrade in [89.5, 79.5, 69.5, 59.5]:
#         final = max(0, round((targetGrade - gradeWithoutFinal) / 0.20))
#         print(f'    {final:4}', end='')
#     print()

# print('*************************************')

# print('Term Project (tp3) grades required given specific final exam grades:')
# print('   -----    -----   -----   -----   -----')
# print('   final      A       B       C       D')
# print('   -----    -----   -----   -----   -----')
# for final in range(100, 49, -5):
#     print(f'   {final:4}', end='')
#     gradeWithoutTp3 = 0.10*quizAvg + 0.30*hwAvg + 0.20*midtermAvg + 0.20*final
#     for targetGrade in [89.5, 79.5, 69.5, 59.5]:
#         tp3 = max(0, round((targetGrade - gradeWithoutTp3) / 0.20))
#         print(f'    {tp3:4}', end='')
#     print()

# ans = 1
# for x in range(1, 2023):
#     ans *= x
# print(ans)
# zeroCount = 0
# while ans > 0:
#     currentDigit = ans % 10
#     if currentDigit == 0:
#         zeroCount += 1
#     ans //= 10
# print(zeroCount)

# import math

# power = 1
# top = 2022
# factor = 5
# count = 0
# while factor ** power <= top:
#     depth = math.floor(2022 / (factor ** power))
#     count += depth
#     print(factor ** power, depth)
#     power += 1
# print(count)

# This demos using image.size

from cmu_112_graphics import *

# def appStarted(app):
#     url = 'https://tinyurl.com/great-pitch-gif'
#     app.image1 = app.loadImage(url)
#     app.image2 = app.scaleImage(app.image1, 2/3)

# def drawImageWithSizeBelowIt(app, canvas, image, cx, cy):
#     canvas.create_image(cx, cy, image=ImageTk.PhotoImage(image))
#     imageWidth, imageHeight = image.size
#     msg = f'Image size: {imageWidth} x {imageHeight}'
#     canvas.create_text(cx, cy + imageHeight/2 + 20,
#                        text=msg, font='Arial 20 bold', fill='black')

# def redrawAll(app, canvas):
#     drawImageWithSizeBelowIt(app, canvas, app.image1, 200, 300)
#     drawImageWithSizeBelowIt(app, canvas, app.image2, 500, 300)

# runApp(width=700, height=600)

# This demos using modes (aka screens).

from cmu_112_graphics import *
import random

##########################################
# Splash Screen Mode
##########################################

def splashScreenMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, text='This demos a ModalApp!',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 200, text='This is a modal splash screen!',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 250, text='Press any key for the game!',
                       font=font, fill='black')

def splashScreenMode_keyPressed(app, event):
    app.mode = 'gameMode'

##########################################
# Game Mode
##########################################

def gameMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 20, text=f'Score: {app.score}',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 60, text='Click on the dot!',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 100, text='Press h for help screen!',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 140, text='Press v for an MVC Violation!',
                       font=font, fill='black')
    canvas.create_oval(app.x-app.r, app.y-app.r, app.x+app.r, app.y+app.r,
                       fill=app.color)
    if app.makeAnMVCViolation:
        app.ohNo = 'This is an MVC Violation!'

def gameMode_timerFired(app):
    moveDot(app)

def gameMode_mousePressed(app, event):
    d = ((app.x - event.x)**2 + (app.y - event.y)**2)**0.5
    if (d <= app.r):
        app.score += 1
        randomizeDot(app)
    elif (app.score > 0):
        app.score -= 1

def gameMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'
    elif (event.key == 'v'):
        app.makeAnMVCViolation = True

##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, text='This is the help screen!', 
                       font=font, fill='black')
    canvas.create_text(app.width/2, 250, text='(Insert helpful message here)',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 350, text='Press any key to return to the game!',
                       font=font, fill='black')

def helpMode_keyPressed(app, event):
    app.mode = 'gameMode'

##########################################
# Main App
##########################################

def appStarted(app):
    app.mode = 'splashScreenMode'
    app.score = 0
    app.timerDelay = 50
    app.makeAnMVCViolation = False
    randomizeDot(app)

def randomizeDot(app):
    app.x = random.randint(20, app.width-20)
    app.y = random.randint(20, app.height-20)
    app.r = random.randint(10, 20)
    app.color = random.choice(['red', 'orange', 'yellow', 'green', 'blue'])
    app.dx = random.choice([+1,-1])*random.randint(3,6)
    app.dy = random.choice([+1,-1])*random.randint(3,6)

def moveDot(app):
    app.x += app.dx
    if (app.x < 0) or (app.x > app.width): app.dx = -app.dx
    app.y += app.dy
    if (app.y < 0) or (app.y > app.height): app.dy = -app.dy

runApp(width=600, height=500)