import random
import time
from pathlib import Path
from turtle import Screen, Turtle

from ball import Ball
from game_config import (
    ARENA_X_LIMIT,
    ARENA_Y_LIMIT,
    BEST_OF_OPTIONS,
    CONTROL_BINDINGS,
    DEFAULT_DIFFICULTY,
    DIFFICULTY_PRESETS,
    PADDLE_X_OFFSET,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from game_logic import MatchSession, PersistentStats
from paddle import Paddle
from scoreboard import ScoreBoard


class PongGame:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor("black")
        self.screen.title("Ping Pong")
        self.screen.tracer(0)

        self.game_state = "start"
        self.mode = "pvp"
        self.best_of_index = 0
        self.difficulty_order = list(DIFFICULTY_PRESETS.keys())
        self.difficulty_index = self.difficulty_order.index(DEFAULT_DIFFICULTY)
        self.session = None
        self.persisted_stats = PersistentStats.load(self._stats_path())

        self.left_paddle = None
        self.right_paddle = None
        self.ball = None
        self.scoreboard = ScoreBoard()

        self._last_cpu_update = time.monotonic()
        self.running = True

        self._draw_arena()
        self._bind_keys()
        self._show_start_screen()

    @staticmethod
    def _stats_path():
        return Path(__file__).resolve().parent / "stats.json"

    @property
    def difficulty_name(self):
        return self.difficulty_order[self.difficulty_index]

    @property
    def difficulty(self):
        return DIFFICULTY_PRESETS[self.difficulty_name]

    @property
    def current_best_of(self):
        return BEST_OF_OPTIONS[self.best_of_index]

    def _create_or_reset_entities(self):
        paddle_speed = self.difficulty["paddle_speed"]
        if self.left_paddle is None:
            self.left_paddle = Paddle(
                (-PADDLE_X_OFFSET, 0),
                move_distance=paddle_speed,
                min_y=-ARENA_Y_LIMIT + 50,
                max_y=ARENA_Y_LIMIT - 50,
            )
        if self.right_paddle is None:
            self.right_paddle = Paddle(
                (PADDLE_X_OFFSET, 0),
                move_distance=paddle_speed,
                min_y=-ARENA_Y_LIMIT + 50,
                max_y=ARENA_Y_LIMIT - 50,
            )
        self.left_paddle.goto(-PADDLE_X_OFFSET, 0)
        self.right_paddle.goto(PADDLE_X_OFFSET, 0)
        self.left_paddle.move_distance = paddle_speed
        self.right_paddle.move_distance = paddle_speed

        if self.ball is None:
            self.ball = Ball(
                base_move_speed=self.difficulty["move_speed"],
                speed_growth=self.difficulty["speed_growth"],
            )
        else:
            self.ball.base_move_speed = self.difficulty["move_speed"]
            self.ball.speed_growth = self.difficulty["speed_growth"]
        self.ball.reset_position(serve_to=random.choice(("left", "right")))

    def _draw_arena(self):
        arena = Turtle()
        arena.hideturtle()
        arena.color("white")
        arena.penup()
        arena.goto(0, -ARENA_Y_LIMIT)
        arena.setheading(90)
        for _ in range(18):
            arena.pendown()
            arena.forward(16)
            arena.penup()
            arena.forward(16)

        arena.goto(-ARENA_X_LIMIT, -ARENA_Y_LIMIT)
        arena.setheading(0)
        arena.pendown()
        for _ in range(2):
            arena.forward(ARENA_X_LIMIT * 2)
            arena.left(90)
            arena.forward(ARENA_Y_LIMIT * 2)
            arena.left(90)
        arena.penup()

    def _bind_keys(self):
        self.screen.listen()
        self.screen.onkey(self._move_left_up, CONTROL_BINDINGS["left_up"])
        self.screen.onkey(self._move_left_down, CONTROL_BINDINGS["left_down"])
        self.screen.onkey(self._move_right_up, CONTROL_BINDINGS["right_up"])
        self.screen.onkey(self._move_right_down, CONTROL_BINDINGS["right_down"])
        self.screen.onkey(lambda: self.start_match("pvp"), CONTROL_BINDINGS["start_pvp"])
        self.screen.onkey(lambda: self.start_match("cpu"), CONTROL_BINDINGS["start_cpu"])
        self.screen.onkey(self.toggle_pause, CONTROL_BINDINGS["pause_resume"])
        self.screen.onkey(self.restart_match, CONTROL_BINDINGS["restart"])
        self.screen.onkey(self.toggle_best_of, CONTROL_BINDINGS["toggle_best_of"])
        self.screen.onkey(self.cycle_difficulty, CONTROL_BINDINGS["cycle_difficulty"])
        self.screen.onkey(self.quit_game, CONTROL_BINDINGS["quit"])

    def _move_left_up(self):
        if self.left_paddle and self.game_state in {"playing", "paused"}:
            self.left_paddle.go_up()

    def _move_left_down(self):
        if self.left_paddle and self.game_state in {"playing", "paused"}:
            self.left_paddle.go_down()

    def _move_right_up(self):
        if self.mode == "pvp" and self.right_paddle and self.game_state in {"playing", "paused"}:
            self.right_paddle.go_up()

    def _move_right_down(self):
        if self.mode == "pvp" and self.right_paddle and self.game_state in {"playing", "paused"}:
            self.right_paddle.go_down()

    def _show_start_screen(self):
        self.scoreboard.update_score(0, 0)
        self.scoreboard.show_banner("Ping Pong")
        self.scoreboard.show_status(
            f"[1] PVP  [2] Player vs CPU  [Space] Pause/Resume  [R] Restart  [D] Difficulty({self.difficulty_name})  "
            f"[B] Best of {self.current_best_of}  [Q] Quit"
        )

    def _status_line(self):
        opponent = "P2" if self.mode == "pvp" else "CPU"
        return (
            f"Mode: {'PVP' if self.mode == 'pvp' else 'Player vs CPU'}  Difficulty: {self.difficulty_name}  "
            f"Round wins P1-{self.session.left_round_wins} {opponent}-{self.session.right_round_wins}  "
            f"Best of {self.current_best_of}"
        )

    def cycle_difficulty(self):
        if self.game_state == "playing":
            return
        self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulty_order)
        self._show_start_screen()

    def toggle_best_of(self):
        if self.game_state == "playing":
            return
        self.best_of_index = (self.best_of_index + 1) % len(BEST_OF_OPTIONS)
        self._show_start_screen()

    def start_match(self, mode):
        self.mode = mode
        self.session = MatchSession(
            max_score=self.difficulty["max_score"],
            best_of=self.current_best_of,
        )
        self._create_or_reset_entities()
        self.scoreboard.clear_banner()
        self.scoreboard.update_score(0, 0)
        self.scoreboard.show_status(self._status_line())
        self.game_state = "playing"

    def restart_match(self):
        self.start_match(self.mode)

    def toggle_pause(self):
        if self.game_state == "playing":
            self.game_state = "paused"
            self.scoreboard.show_banner("Paused")
        elif self.game_state == "paused":
            self.game_state = "playing"
            self.scoreboard.clear_banner()

    def quit_game(self):
        self.running = False

    def _handle_wall_collision(self):
        if self.ball.ycor() >= ARENA_Y_LIMIT - 10 or self.ball.ycor() <= -ARENA_Y_LIMIT + 10:
            self.ball.bounce_y()

    def _handle_paddle_collision(self):
        if self.ball.xcor() > PADDLE_X_OFFSET - 25 and self.ball.x_move > 0:
            if self.ball.distance(self.right_paddle) < 50:
                offset = (self.ball.ycor() - self.right_paddle.ycor()) / 50
                self.ball.bounce_paddle(offset)

        if self.ball.xcor() < -PADDLE_X_OFFSET + 25 and self.ball.x_move < 0:
            if self.ball.distance(self.left_paddle) < 50:
                offset = (self.ball.ycor() - self.left_paddle.ycor()) / 50
                self.ball.bounce_paddle(offset)

    def _handle_score(self):
        if self.ball.xcor() > ARENA_X_LIMIT:
            self.session.add_point("left")
            self.scoreboard.update_score(self.session.left_score, self.session.right_score)
            self.ball.reset_position(serve_to="right")
        elif self.ball.xcor() < -ARENA_X_LIMIT:
            self.session.add_point("right")
            self.scoreboard.update_score(self.session.left_score, self.session.right_score)
            self.ball.reset_position(serve_to="left")

        winner = self.session.round_winner()
        if winner:
            self.session.conclude_round(winner)
            match_winner = self.session.match_winner()
            self.scoreboard.update_score(self.session.left_score, self.session.right_score)
            if match_winner:
                self._finish_match(match_winner)
            else:
                round_winner_text = "P1" if winner == "left" else ("P2" if self.mode == "pvp" else "CPU")
                self.scoreboard.show_banner(f"{round_winner_text} won the round!")
                self.ball.reset_position(serve_to="left" if winner == "right" else "right")
                self.game_state = "paused"

    def _finish_match(self, winner):
        self.game_state = "game_over"
        winner_text = "P1" if winner == "left" else ("P2" if self.mode == "pvp" else "CPU")
        self.persisted_stats.record_match_result(winner, self.session.longest_streak)
        self.persisted_stats.save(self._stats_path())
        self.scoreboard.show_banner(f"{winner_text} wins the match!")
        self.scoreboard.show_status(
            f"Rounds: {self.session.rounds_played}  Session streak: {self.session.longest_streak}  "
            f"All-time longest streak: {self.persisted_stats.longest_streak}  [R] Restart  [Q] Quit"
        )

    def _maybe_move_cpu(self):
        if self.mode != "cpu":
            return
        now = time.monotonic()
        if now - self._last_cpu_update < self.difficulty["cpu_reaction"]:
            return
        self._last_cpu_update = now
        if random.random() > self.difficulty["cpu_accuracy"]:
            return
        y_delta = self.ball.ycor() - self.right_paddle.ycor()
        if y_delta > 10:
            self.right_paddle.go_up()
        elif y_delta < -10:
            self.right_paddle.go_down()

    def _tick(self):
        self.ball.move()
        self._handle_wall_collision()
        self._handle_paddle_collision()
        self._handle_score()
        self._maybe_move_cpu()
        if self.game_state == "playing":
            self.scoreboard.show_status(self._status_line())

    def run(self):
        while self.running:
            self.screen.update()
            if self.game_state == "playing":
                self.scoreboard.clear_banner()
                self._tick()
                time.sleep(self.ball.move_speed)
            else:
                time.sleep(0.02)
        self.screen.bye()
