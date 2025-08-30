from turtle import Turtle

FONT = ('arial',88,'normal')
ALIGNMENT = "center" 

class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_scoreboard()
        
    def update_scoreboard(self):
        self.clear()
        self.goto(-100,200)
        self.write(self.l_score,font=FONT,align=ALIGNMENT)
        self.goto(100,200)
        self.write(self.r_score,font=FONT,align=ALIGNMENT)

    def l_point(self):
        self.l_score += 1
        self.update_scoreboard()
        
    def r_point(self):
        self.r_score += 1
        self.update_scoreboard()
