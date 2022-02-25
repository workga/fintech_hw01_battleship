import curses
import typer

from config import (
    FIELD_DEFAULT_HEIGHT,
    FIELD_DEFAULT_WIDTH,
    MIN_FIELD_SIZE,
    MAX_FIELD_SIZE,
    CONTROL_QUIT,
    MAX_RESIZE_ATTEMPTS_COUNT,
    MAX_CONTROL_ATTEMPTS_COUNT,
)
from battleship import Battleship
from view import View


def run_curses(
    height: int = typer.Argument(FIELD_DEFAULT_HEIGHT, help="Field's height"),
    width: int = typer.Argument(FIELD_DEFAULT_WIDTH, help="Field's width"),
    debug: bool = typer.Option(False, help="Debug mode"),
):
    curses.wrapper(main, height, width, debug)


def main(screen, height, width, debug):
    if (
        height < MIN_FIELD_SIZE
        or height > MAX_FIELD_SIZE
        or width < MIN_FIELD_SIZE
        or width > MAX_FIELD_SIZE
    ):
        screen.addstr(
            0,
            0,
            (
                f"Wrong size of field, press any key ("
                f"min size: {MIN_FIELD_SIZE},"
                f"max size: {MAX_FIELD_SIZE})"
            ),
        )
        screen.getch()
        return

    game = Battleship(height, width, debug)
    view = View(screen, game)

    console_is_correct = view.resize()
    resize_attempts_count = 0
    control_attempts_count = 0
    moves_count = 0
    max_moves_count = height * width
    while (
        resize_attempts_count < MAX_RESIZE_ATTEMPTS_COUNT
        and control_attempts_count < MAX_CONTROL_ATTEMPTS_COUNT
        and moves_count < max_moves_count
    ):
        if not console_is_correct:
            screen.clear()

            required_height, required_width = view.get_required_size()
            screen.addstr(
                0, 0, f"Required size of console is {required_height}x{required_width}"
            )
            screen.addstr(1, 0, f"Resize console or press q to quit")

            ch = screen.getch()
            resize_attempts_count += 1

            if ch == curses.KEY_RESIZE:
                if view.resize():
                    console_is_correct = True
                    resize_attempts_count = 0
            elif ch == CONTROL_QUIT:
                break
            continue

        view.update()

        if game.is_over():
            game.delete()
            screen.getch()
            return

        ch = screen.getch()

        if ch == curses.KEY_RESIZE:
            console_is_correct = view.resize()
            continue
        elif ch == CONTROL_QUIT:
            break
        else:
            if not game.handle_input(ch):
                control_attempts_count += 1
            else:
                moves_count += 1
                control_attempts_count = 0

    game.save()


if __name__ == "__main__":
    typer.run(run_curses)
