from __future__ import annotations

import curses
import random
import time
from collections import deque
from dataclasses import dataclass


BOARD_WIDTH = 32
BOARD_HEIGHT = 18
INITIAL_LENGTH = 4
FRAME_DELAY = 0.12

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

KEY_DIRECTIONS = {
    curses.KEY_UP: UP,
    curses.KEY_DOWN: DOWN,
    curses.KEY_LEFT: LEFT,
    curses.KEY_RIGHT: RIGHT,
    ord("w"): UP,
    ord("W"): UP,
    ord("s"): DOWN,
    ord("S"): DOWN,
    ord("a"): LEFT,
    ord("A"): LEFT,
    ord("d"): RIGHT,
    ord("D"): RIGHT,
}

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}


@dataclass
class GameState:
    snake: deque[tuple[int, int]]
    direction: tuple[int, int]
    pending_direction: tuple[int, int]
    food: tuple[int, int]
    score: int = 0
    is_over: bool = False
    is_paused: bool = False


def wrap_position(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return x % BOARD_WIDTH, y % BOARD_HEIGHT


def advance_position(
    position: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    x, y = position
    dx, dy = direction
    return wrap_position((x + dx, y + dy))


def spawn_food(
    snake: deque[tuple[int, int]], rng: random.Random
) -> tuple[int, int]:
    occupied = set(snake)
    available = [
        (x, y)
        for y in range(BOARD_HEIGHT)
        for x in range(BOARD_WIDTH)
        if (x, y) not in occupied
    ]
    if not available:
        return snake[0]
    return rng.choice(available)


def create_game(rng: random.Random | None = None) -> GameState:
    rng = rng or random.Random()
    center_x = BOARD_WIDTH // 2
    center_y = BOARD_HEIGHT // 2
    snake = deque(
        (center_x - offset, center_y) for offset in range(INITIAL_LENGTH)
    )
    food = spawn_food(snake, rng)
    return GameState(
        snake=snake,
        direction=RIGHT,
        pending_direction=RIGHT,
        food=food,
    )


def queue_direction(state: GameState, candidate: tuple[int, int]) -> None:
    if candidate == OPPOSITE_DIRECTIONS[state.direction]:
        return
    state.pending_direction = candidate


def step_game(state: GameState, rng: random.Random) -> None:
    if state.is_over or state.is_paused:
        return

    state.direction = state.pending_direction
    new_head = advance_position(state.snake[0], state.direction)
    will_grow = new_head == state.food
    body_to_check = state.snake if will_grow else list(state.snake)[:-1]

    if new_head in body_to_check:
        state.is_over = True
        return

    state.snake.appendleft(new_head)
    if will_grow:
        state.score += 1
        state.food = spawn_food(state.snake, rng)
    else:
        state.snake.pop()


def draw_board(stdscr: curses.window, state: GameState) -> None:
    stdscr.erase()
    stdscr.addstr(
        0,
        0,
        "Snake  Score: "
        f"{state.score}  "
        "Move: arrows/WASD  Pause: P  Restart: R  Quit: Q"
    )
    stdscr.addstr(1, 0, "+" + "-" * BOARD_WIDTH + "+")

    snake_positions = set(state.snake)
    head = state.snake[0]
    for y in range(BOARD_HEIGHT):
        row = ["|"]
        for x in range(BOARD_WIDTH):
            point = (x, y)
            if point == head:
                row.append("@")
            elif point == state.food:
                row.append("*")
            elif point in snake_positions:
                row.append("#")
            else:
                row.append(" ")
        row.append("|")
        stdscr.addstr(y + 2, 0, "".join(row))

    stdscr.addstr(BOARD_HEIGHT + 2, 0, "+" + "-" * BOARD_WIDTH + "+")

    status_row = BOARD_HEIGHT + 4
    if state.is_paused:
        stdscr.addstr(status_row, 0, "Paused. Press P to continue.")
    elif state.is_over:
        stdscr.addstr(status_row, 0, "Game over. Press R to restart or Q to quit.")
    else:
        stdscr.addstr(status_row, 0, "Eat food, avoid yourself, and keep growing.")

    stdscr.refresh()


def run(stdscr: curses.window) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    min_height = BOARD_HEIGHT + 6
    min_width = BOARD_WIDTH + 2
    if curses.LINES < min_height or curses.COLS < min_width:
        raise SystemExit(
            f"Terminal must be at least {min_width}x{min_height} to play."
        )

    rng = random.Random()
    state = create_game(rng)
    last_tick = time.monotonic()

    while True:
        key = stdscr.getch()
        if key != -1:
            if key in KEY_DIRECTIONS and not state.is_over:
                queue_direction(state, KEY_DIRECTIONS[key])
            elif key in (ord("p"), ord("P")) and not state.is_over:
                state.is_paused = not state.is_paused
            elif key in (ord("r"), ord("R")):
                state = create_game(rng)
                last_tick = time.monotonic()
            elif key in (ord("q"), ord("Q")):
                break

        now = time.monotonic()
        if now - last_tick >= FRAME_DELAY:
            step_game(state, rng)
            last_tick = now

        draw_board(stdscr, state)
        time.sleep(0.01)


def main() -> None:
    curses.wrapper(run)


if __name__ == "__main__":
    main()
