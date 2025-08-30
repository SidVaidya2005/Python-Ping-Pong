from turtle import Turtle

class Paddle(Turtle):

    def __init__(self,position):
        super().__init__()
        self.shape("square")
        self.penup()
        self.color("white")
        self.shapesize(stretch_len=1,stretch_wid=5)
        self.goto(position)

    def go_up(self):
        if self.ycor() > 230:
            self.goto(self.xcor(),230)
        else:
            new_y = self.ycor() + 20
            self.goto(self.xcor(),new_y)

    def go_down(self):
        if self.ycor() < -230:
            self.goto(self.xcor(),-230)
        else:
            new_y = self.ycor() - 20
            self.goto(self.xcor(),new_y)
