import random
from turtle import Turtle


class Ball(Turtle):
    def __init__(self, step_size=10, base_move_speed=0.1, speed_growth=0.9):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("white")
        self.step_size = step_size
        self.base_move_speed = base_move_speed
        self.speed_growth = speed_growth
        self.x_move = step_size
        self.y_move = random.choice([-step_size, step_size])
        self.move_speed = base_move_speed

    def move(self):
        self.goto(self.xcor() + self.x_move, self.ycor() + self.y_move)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_paddle(self, normalized_offset=0.0):
        self.x_move *= -1
        self.y_move += normalized_offset * (self.step_size * 0.8)
        max_vertical = self.step_size * 1.8
        self.y_move = max(-max_vertical, min(max_vertical, self.y_move))
        self.move_speed *= self.speed_growth

    def reset_position(self, serve_to="right"):
        self.goto(0, 0)
        self.move_speed = self.base_move_speed
        serve_direction = 1 if serve_to == "right" else -1
        self.x_move = abs(self.step_size) * serve_direction
        self.y_move = random.choice([-self.step_size, self.step_size])
