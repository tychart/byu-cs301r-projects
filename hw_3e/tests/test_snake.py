from collections import deque
from pathlib import Path
import random
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from hw_3e.snake import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    DOWN,
    GameState,
    RIGHT,
    advance_position,
    queue_direction,
    spawn_food,
    step_game,
)


class SnakeTests(unittest.TestCase):
    def test_wraps_across_board_edges(self) -> None:
        self.assertEqual(advance_position((BOARD_WIDTH - 1, 5), RIGHT), (0, 5))
        self.assertEqual(advance_position((2, BOARD_HEIGHT - 1), DOWN), (2, 0))

    def test_spawn_food_avoids_snake(self) -> None:
        snake = deque([(0, 0), (1, 0), (2, 0)])
        food = spawn_food(snake, random.Random(0))
        self.assertNotIn(food, snake)

    def test_reverse_direction_is_ignored(self) -> None:
        state = GameState(
            snake=deque([(4, 4), (3, 4), (2, 4)]),
            direction=RIGHT,
            pending_direction=RIGHT,
            food=(7, 7),
        )
        queue_direction(state, (-1, 0))
        self.assertEqual(state.pending_direction, RIGHT)

    def test_step_marks_collision_with_body(self) -> None:
        state = GameState(
            snake=deque([(2, 2), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2)]),
            direction=DOWN,
            pending_direction=DOWN,
            food=(10, 10),
        )

        step_game(state, random.Random(0))
        self.assertTrue(state.is_over)


if __name__ == "__main__":
    unittest.main()
