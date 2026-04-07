import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class PersistentStats:
    matches_played: int = 0
    left_match_wins: int = 0
    right_match_wins: int = 0
    longest_streak: int = 0

    @classmethod
    def load(cls, path):
        stats_path = Path(path)
        if not stats_path.exists():
            return cls()
        try:
            data = json.loads(stats_path.read_text(encoding="utf-8"))
            return cls(
                matches_played=int(data.get("matches_played", 0)),
                left_match_wins=int(data.get("left_match_wins", 0)),
                right_match_wins=int(data.get("right_match_wins", 0)),
                longest_streak=int(data.get("longest_streak", 0)),
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return cls()

    def save(self, path):
        stats_path = Path(path)
        stats_path.write_text(
            json.dumps(asdict(self), indent=2, sort_keys=True),
            encoding="utf-8",
        )

    def record_match_result(self, winner, session_longest_streak):
        self.matches_played += 1
        if winner == "left":
            self.left_match_wins += 1
        elif winner == "right":
            self.right_match_wins += 1
        self.longest_streak = max(self.longest_streak, session_longest_streak)


class MatchSession:
    def __init__(self, max_score, best_of=1):
        self.max_score = max_score
        self.best_of = best_of
        self.left_score = 0
        self.right_score = 0
        self.rounds_played = 0
        self.left_round_wins = 0
        self.right_round_wins = 0
        self.current_streak_owner = None
        self.current_streak_length = 0
        self.longest_streak = 0

    @property
    def required_round_wins(self):
        return (self.best_of // 2) + 1

    def reset_scores(self):
        self.left_score = 0
        self.right_score = 0

    def reset_match(self):
        self.reset_scores()
        self.rounds_played = 0
        self.left_round_wins = 0
        self.right_round_wins = 0
        self.current_streak_owner = None
        self.current_streak_length = 0
        self.longest_streak = 0

    def add_point(self, side):
        if side == "left":
            self.left_score += 1
        elif side == "right":
            self.right_score += 1

    def round_winner(self):
        if self.left_score >= self.max_score:
            return "left"
        if self.right_score >= self.max_score:
            return "right"
        return None

    def _update_streak(self, winner):
        if self.current_streak_owner == winner:
            self.current_streak_length += 1
        else:
            self.current_streak_owner = winner
            self.current_streak_length = 1
        self.longest_streak = max(self.longest_streak, self.current_streak_length)

    def conclude_round(self, winner):
        self.rounds_played += 1
        if winner == "left":
            self.left_round_wins += 1
        elif winner == "right":
            self.right_round_wins += 1
        self._update_streak(winner)
        self.reset_scores()

    def match_winner(self):
        if self.left_round_wins >= self.required_round_wins:
            return "left"
        if self.right_round_wins >= self.required_round_wins:
            return "right"
        return None
