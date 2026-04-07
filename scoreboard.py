from turtle import Turtle

SCORE_FONT = ("arial", 72, "normal")
BANNER_FONT = ("arial", 22, "bold")
STATUS_FONT = ("arial", 14, "normal")
ALIGNMENT = "center"


class ScoreBoard:
    def __init__(self):
        self.score_turtle = self._make_writer()
        self.banner_turtle = self._make_writer()
        self.status_turtle = self._make_writer()
        self.left_score = 0
        self.right_score = 0
        self.update_score(self.left_score, self.right_score)

    @staticmethod
    def _make_writer():
        writer = Turtle()
        writer.color("white")
        writer.penup()
        writer.hideturtle()
        return writer

    def update_score(self, left_score, right_score):
        self.left_score = left_score
        self.right_score = right_score
        self.score_turtle.clear()
        self.score_turtle.goto(-120, 180)
        self.score_turtle.write(self.left_score, font=SCORE_FONT, align=ALIGNMENT)
        self.score_turtle.goto(120, 180)
        self.score_turtle.write(self.right_score, font=SCORE_FONT, align=ALIGNMENT)

    def show_banner(self, text):
        self.banner_turtle.clear()
        self.banner_turtle.goto(0, 30)
        self.banner_turtle.write(text, font=BANNER_FONT, align=ALIGNMENT)

    def clear_banner(self):
        self.banner_turtle.clear()

    def show_status(self, text):
        self.status_turtle.clear()
        self.status_turtle.goto(0, -260)
        self.status_turtle.write(text, font=STATUS_FONT, align=ALIGNMENT)
