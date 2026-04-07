import tempfile
import unittest
from pathlib import Path

from game_logic import MatchSession, PersistentStats


class MatchSessionTests(unittest.TestCase):
    def test_round_winner_and_reset(self):
        session = MatchSession(max_score=3, best_of=3)
        session.add_point("left")
        session.add_point("left")
        session.add_point("left")

        self.assertEqual(session.round_winner(), "left")
        session.conclude_round("left")

        self.assertEqual(session.left_round_wins, 1)
        self.assertEqual(session.right_round_wins, 0)
        self.assertEqual(session.left_score, 0)
        self.assertEqual(session.right_score, 0)

    def test_match_winner_best_of_three(self):
        session = MatchSession(max_score=2, best_of=3)
        session.conclude_round("left")
        self.assertIsNone(session.match_winner())
        session.conclude_round("left")
        self.assertEqual(session.match_winner(), "left")

    def test_streak_tracking(self):
        session = MatchSession(max_score=2, best_of=5)
        session.conclude_round("left")
        session.conclude_round("left")
        session.conclude_round("right")

        self.assertEqual(session.longest_streak, 2)
        self.assertEqual(session.current_streak_owner, "right")
        self.assertEqual(session.current_streak_length, 1)


class PersistentStatsTests(unittest.TestCase):
    def test_load_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            stats = PersistentStats.load(Path(tmp_dir) / "missing.json")
            self.assertEqual(stats.matches_played, 0)
            self.assertEqual(stats.left_match_wins, 0)
            self.assertEqual(stats.right_match_wins, 0)

    def test_save_and_reload(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "stats.json"
            stats = PersistentStats()
            stats.record_match_result("left", session_longest_streak=4)
            stats.save(file_path)

            loaded = PersistentStats.load(file_path)
            self.assertEqual(loaded.matches_played, 1)
            self.assertEqual(loaded.left_match_wins, 1)
            self.assertEqual(loaded.longest_streak, 4)

    def test_load_bad_json_gracefully(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "stats.json"
            file_path.write_text("{bad json", encoding="utf-8")
            loaded = PersistentStats.load(file_path)
            self.assertEqual(loaded.matches_played, 0)


if __name__ == "__main__":
    unittest.main()
