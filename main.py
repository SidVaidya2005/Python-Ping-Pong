from scoreboard import ScoreBoard
from paddle import Paddle
from turtle import Screen
from ball import Ball
import time

# --------------------- INITIALIZATION -------------------- #
l_paddle = Paddle((-350,0))
r_paddle = Paddle((350,0))
scoreboard = ScoreBoard()
screen = Screen()
ball = Ball()

# --------------------- SCREEN ----------------------- #
screen.setup(width=800,height=600)
screen.bgcolor('black')
screen.title('Ping Pong')
screen.tracer(0)

# ----------------------- CONTROLS ---------------------- #
screen.listen()
screen.onkey(r_paddle.go_up,'Up')
screen.onkey(r_paddle.go_down,"Down")
screen.onkey(l_paddle.go_up,'w')
screen.onkey(l_paddle.go_down,"s")

# -------------------------- MAIN ------------------------- #
MAX_SCORE = 3
game_is_on = True

while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect Collision With Wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect Collision With Paddle
    if ball.xcor() > 320 and ball.distance(r_paddle) < 50 or\
        ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()

    # If r_paddle has missed the Ball
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    # If l_paddle has missed the Ball
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()
    
    if scoreboard.l_score == MAX_SCORE or scoreboard.r_score == MAX_SCORE:
        game_is_on = False
        
screen.exitonclick()

