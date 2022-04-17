#! /bin/env python3
"""
Game: Simple Pong

Daniel Komnick (high101bro)
8 April 2022
Learning how to write games with my son Nathan

==========================
|      Simple Pong       |
| []                     |    
|         o              |
|                        |
|                     [] |
|                        |
==========================
"""
import turtle as t
import random

print('Starting Pong...')

window = t.Screen()
window.title("Pong by high101bro")
window.bgcolor("black")
window.setup(
    width  = 800,
    height = 600
)
window.tracer(0)


# Left Paddle
leftPaddle = t.Turtle()
leftPaddle.speed(0)        # 0 = fastest speed
leftPaddle.shape("square") #"square","circle","triange","turtle"
leftPaddle.color("lightblue")
leftPaddle.shapesize(      # default size is 20px by 20px
    stretch_wid = 5,       # vertical width of paddle
    stretch_len = 1        # horizontal len of paddle
)
leftPaddle.penup()         # Disables the automatically drawing of lines
leftPaddle.goto(-350,0)    # Initial location of paddle, 0 = dead center
leftPaddle.dy = .2         # Y Delta Speed


# Right Paddle
rightPaddle = t.Turtle()
rightPaddle.speed(0)          # 0 = fastest speed
rightPaddle.shape("square") # "square","circle","triange","turtle"
rightPaddle.color("pink")
rightPaddle.shapesize(      # default size is 20px by 20px
    stretch_wid = 5,        # vertical width of paddle
    stretch_len = 1         # horizontal len of paddle
)
rightPaddle.tilt(180)       # Flips the image
rightPaddle.penup()         # Disables the automatically drawing of lines
rightPaddle.goto(350,0)     # Initial location of paddle, 0 = dead center
rightPaddle.dy = .2         # Y Delta Speed


# The pong ball
ball = t.Turtle()
ball.speed(0)        # 0 = fastest speed
ball.shape("circle") # "square","circle","triange","turtle"
ball.color("lightgreen")
ball.shapesize(      # default size is 20px by 20px
    stretch_wid = 1, # vertical width of paddle
    stretch_len = 1  # horizontal len of paddle
)
ball.penup()         # Disables the automatically drawing of lines

leftScoreCount = 0
rightScoreCount = 0
ballSpeedDisplayCount = 1

def updateScreenText(leftScoreCount,rightScoreCount,ballSpeedDisplayCount) :
    # Top Title Bar
    topBar = t
    topBar.color('white')
    topBar.hideturtle()
    topBar.penup()
    topBar.goto(0,250)
    style = ('Courier', 15, 'italic')
    topBar.write( 'Pong', font=style, align='center' )

    # Left Player Score
    global leftScore
    leftScore = t
    leftScore.color('deep pink')
    leftScore.hideturtle()
    leftScore.penup()
    leftScore.goto(-200,250)
    style = ('Courier', 15, 'italic')
    leftScore.write( leftScoreCount, font=style, align='center' )

    # Right Player Score
    global rightScore
    rightScore = t
    rightScore.color('deep pink')
    rightScore.hideturtle()
    rightScore.penup()
    rightScore.goto(200,250)
    style = ('Courier', 15, 'italic')
    rightScore.write( rightScoreCount, font=style, align='center' )

    # Right Player Score
    global ballSpeedDisplay
    ballSpeedDisplay = t
    ballSpeedDisplay.color('white')
    ballSpeedDisplay.hideturtle()
    ballSpeedDisplay.penup()
    ballSpeedDisplay.goto(0,-275)
    style = ('Courier', 12, 'italic')
    speed = "Ball Speed: {0}".format(round(abs(ballSpeedDisplayCount),2))
    ballSpeedDisplay.write( speed, font=style, align='center' )


# Randomly starts the ball 
def randomStart(ball) :
    # Initial location of paddle, 0 = dead center
    ball.goto(0,0)
    # ball.settiltangle(0)

    randomDirectionY = random.randint(0, 1)
    randomDirectionX = random.randint(0, 1)
    randomDirectionAngleX = random.randint(1, 10) / 50
    randomDirectionAngleY = random.randint(1, 7) / 50

    if randomDirectionY == 1 :
        # Y Delta Speed
        # ball.dy = .1
        ball.dy = randomDirectionAngleY

        # X Delta Speed
        if randomDirectionX == 1 :
            ball.dx = .1
        else :
            ball.dx = -.1          
    else :
        # Y Delta Speed
        ball.dy = randomDirectionAngleY
        # ball.dy = -.1

        # X Delta Speed
        if randomDirectionX == 1 :
            ball.dx = .1
        else :
            ball.dx = -.1

# Calling Initial Functions
randomStart(ball)
updateScreenText(leftScoreCount,rightScoreCount,ball.dx * 10)


# Currently pong is configured for gliding... it would be fun that a power-reduce removes this, or gives gliding... lol
# So this is still useful
paddleSpeed = 1

leftPaddleDirection  = 'none'
rightPaddleDirection = 'none'

# Functions: Left Paddle
def leftPaddleUp() :
    global leftPaddleDirection
    leftPaddleDirection = 'up'
    y = leftPaddle.ycor()
    y += paddleSpeed
    leftPaddle.sety(y)

def leftPaddleDown() :
    global leftPaddleDirection
    leftPaddleDirection = 'down'
    y = leftPaddle.ycor()
    y -= paddleSpeed
    leftPaddle.sety(y)

def leftPaddleLeft() :
    global leftPaddleDirection
    leftPaddleDirection = 'none'
    # x = leftPaddle.xcor()
    # x -= paddleSpeed
    # leftPaddle.setx(x)

def leftPaddleRight() :
    global leftPaddleDirection
    leftPaddleDirection = 'none'
    x = leftPaddle.xcor()
    if leftPaddle.xcor() == -350 :
        x += 20
    leftPaddle.setx(x)
    
    global leftPushCounter
    leftPushCounter = 250

# Functions: Right Paddle
def rightPaddleUp() :
    global rightPaddleDirection
    rightPaddleDirection = 'up'
    y = rightPaddle.ycor()
    y += paddleSpeed
    rightPaddle.sety(y)

def rightPaddleDown() :
    global rightPaddleDirection
    rightPaddleDirection = 'down'
    y = rightPaddle.ycor()
    y -= paddleSpeed
    rightPaddle.sety(y)

def rightPaddleLeft() :
    global rightPaddleDirection
    rightPaddleDirection = 'none'
    # x = rightPaddle.xcor()
    # x -= paddleSpeed
    # rightPaddle.setx(x)

def rightPaddleRight() :
    global rightPaddleDirection
    rightPaddleDirection = 'none'
    # x = rightPaddle.xcor()
    # x += paddleSpeed
    # rightPaddle.setx(x)


gameStatus = 'paused'
def upadateGaneStatus() :
    global gameStatus
    if gameStatus == 'paused' :
        gameStatus = 'running'
    elif gameStatus == 'running' :
        gameStatus = 'paused'



# Keyboard Binding
window.listen()     # Tells the windows to listen to keyboard inputs
window.onkeypress(leftPaddleUp,      "w")
window.onkeypress(leftPaddleDown,    "s")
window.onkeypress(leftPaddleLeft,    "a")
window.onkeypress(leftPaddleRight,   "d")
window.onkeypress(rightPaddleUp,     "i")
window.onkeypress(rightPaddleDown,   "k")
window.onkeypress(rightPaddleLeft,   "j")
window.onkeypress(rightPaddleRight,  "l")
window.onkeypress(upadateGaneStatus, "space")

leftPushCounter = 0

# Main game loop
while True :
    window.update()

    # Left paddle glide movement
    if leftPaddleDirection == 'up' :
        if (leftPaddle.ycor() + 0) >= 300 :
            leftPaddle.sety(leftPaddle.ycor())
        else :
            leftPaddle.sety(leftPaddle.ycor() + leftPaddle.dy)
    elif leftPaddleDirection == 'down' :
        if (leftPaddle.ycor() - 0) <= -300 :
            leftPaddle.sety(leftPaddle.ycor())
        else :
            leftPaddle.sety(leftPaddle.ycor() - leftPaddle.dy)
    elif leftPaddleDirection == 'none' :
        leftPaddle.sety(leftPaddle.ycor())


    # Right paddle glide movement
    if rightPaddleDirection == 'up' :
        if (rightPaddle.ycor() + 0) >= 300 :
            rightPaddle.sety(rightPaddle.ycor())
        else :
            rightPaddle.sety(rightPaddle.ycor() + rightPaddle.dy)
    elif rightPaddleDirection == 'down' :
        if (rightPaddle.ycor() - 0) <= -300 :
            rightPaddle.sety(rightPaddle.ycor())
        else :
            rightPaddle.sety(rightPaddle.ycor() - rightPaddle.dy)
    elif rightPaddleDirection == 'none' :
        rightPaddle.sety(rightPaddle.ycor())


    # returns the paddle to normal state from boarder
    leftPushCounter -= 1
    if (leftPaddle.xcor() != -350) and not (leftPushCounter > 0) :
        x = leftPaddle.xcor()
        x -= 20
        leftPaddle.setx(x)
        

    if gameStatus == "running" :

        # Moves the ball
        ball.sety(ball.ycor() + ball.dy)
        ball.setx(ball.xcor() + ball.dx)


        #########################
        # Ball Boarder Bouncing #
        #########################

        # Top boarder
        if ball.ycor() > 290 :
            ball.sety(290)
            ball.dy *= -1

        # Bottom boarder
        elif ball.ycor() < -290 :
            ball.sety(-290)
            ball.dy *= -1

        # Left boarder - player scoring
        elif ball.xcor() < -390 :
            leftShield = False
            if leftShield :
                ball.dx *= -1  
            else :
                randomStart(ball)
                leftPaddle.goto(-350,0)
                rightPaddle.goto(350,0) 
                gameStatus = 'paused'

                rightScoreCount += 1
                leftScore.clear()
                updateScreenText(leftScoreCount,rightScoreCount,ball.dx * 10)

        # Right boarder - player scoring
        elif ball.xcor() > 390 :
            rightShield = False
            if rightShield :
                ball.dx *= -1
            else :
                randomStart(ball)
                leftPaddle.goto(-350,0)
                rightPaddle.goto(350,0)
                gameStatus = 'paused'

                leftScoreCount += 1
                rightScore.clear()
                updateScreenText(leftScoreCount,rightScoreCount,ball.dx * 10)


        #################
        # Paddle Bounce #
        #################

        ballSpeed = "ball y = {0}, ball x = {1}".format(ball.dy,ball.dx)

        # Left Paddle Bounce
        if ball.xcor() < -340 and ball.xcor() > -350 :
            rightScore.clear()
            updateScreenText(leftScoreCount,rightScoreCount,ball.dx * 10)

            # Accounts for bug where ball bounces between paddle and wall
            if ball.ycor() < leftPaddle.ycor() + 55 and ball.ycor() > leftPaddle.ycor() -55 :
                ball.setx(-340)
                ball.dx *= -1.1
        elif ball.xcor() < -330 and ball.xcor() > -340 :
            print('push')
            rightScore.clear()
            updateScreenText(leftScoreCount,rightScoreCount,ball.dx * 10)

            # Accounts for bug where ball bounces between paddle and wall
            if ball.ycor() < leftPaddle.ycor() + 55 and ball.ycor() > leftPaddle.ycor() -55 :
                ball.setx(-330)
                ball.dx *= -1.5


        # Right Paddle Bounce
        elif ball.xcor() > 340 and ball.xcor() < 350 :
            rightScore.clear()
            updateScreenText(leftScoreCount,rightScoreCount,ball.dx * 10)

            # Accounts for bug where ball bounces between paddle and wall
            if ball.ycor() < rightPaddle.ycor() + 55 and ball.ycor() > rightPaddle.ycor() -55 :
                ball.setx(340)
                ball.dx *= -1.1

            # if ball.ycor() < rightPaddle.ycor() + 10 and ball.ycor() > rightPaddle.ycor() -10 :
            #     # Accounts for bug where ball bounces between paddle and wall
            #     ball.setx(340)
            #     # Reverses the balls direction
            #     ball.dx *= -1
            # elif ball.ycor() < rightPaddle.ycor() + 20 and ball.ycor() > rightPaddle.ycor() -20 :
            #     ball.setx(340)
            #     ball.dx *= -1.1
            # elif ball.ycor() < rightPaddle.ycor() + 30 and ball.ycor() > rightPaddle.ycor() -30 :
            #     ball.setx(340)
            #     ball.dx *= -1.2
            # elif ball.ycor() < rightPaddle.ycor() + 40 and ball.ycor() > rightPaddle.ycor() -40 :
            #     ball.setx(340)
            #     ball.dx *= -1.3
            # elif ball.ycor() < rightPaddle.ycor() + 50 and ball.ycor() > rightPaddle.ycor() -50 :
            #     ball.setx(340)
            #     ball.dx *= -1.4
