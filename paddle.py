from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position, move_distance=20, min_y=-230, max_y=230):
        super().__init__()
        self.shape("square")
        self.penup()
        self.color("white")
        self.shapesize(stretch_len=1, stretch_wid=5)
        self.goto(position)
        self.move_distance = move_distance
        self.min_y = min_y
        self.max_y = max_y

    def _move_to_y(self, y_target):
        clamped_y = min(self.max_y, max(self.min_y, y_target))
        self.goto(self.xcor(), clamped_y)

    def go_up(self):
        self._move_to_y(self.ycor() + self.move_distance)

    def go_down(self):
        self._move_to_y(self.ycor() - self.move_distance)
