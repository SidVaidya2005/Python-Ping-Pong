SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ARENA_X_LIMIT = 380
ARENA_Y_LIMIT = 280
PADDLE_X_OFFSET = 350

CONTROL_BINDINGS = {
    "left_up": "w",
    "left_down": "s",
    "right_up": "Up",
    "right_down": "Down",
    "start_pvp": "1",
    "start_cpu": "2",
    "pause_resume": "space",
    "restart": "r",
    "toggle_best_of": "b",
    "cycle_difficulty": "d",
    "quit": "q",
}

BEST_OF_OPTIONS = (1, 3, 5)

DIFFICULTY_PRESETS = {
    "easy": {
        "move_speed": 0.12,
        "speed_growth": 0.97,
        "paddle_speed": 16,
        "max_score": 3,
        "cpu_reaction": 0.09,
        "cpu_accuracy": 0.72,
    },
    "medium": {
        "move_speed": 0.1,
        "speed_growth": 0.95,
        "paddle_speed": 20,
        "max_score": 5,
        "cpu_reaction": 0.07,
        "cpu_accuracy": 0.8,
    },
    "hard": {
        "move_speed": 0.08,
        "speed_growth": 0.93,
        "paddle_speed": 24,
        "max_score": 7,
        "cpu_reaction": 0.05,
        "cpu_accuracy": 0.9,
    },
}

DEFAULT_DIFFICULTY = "medium"
