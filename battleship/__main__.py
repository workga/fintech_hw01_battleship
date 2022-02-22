import os
import curses
import typer
# from typing import Optional

from config import *
from battleship import Battleship
from view import View

def run_curses(height: int=typer.Argument(FIELD_DEFAULT_HEIGHT, help="Field's height"), \
               width: int=typer.Argument(FIELD_DEFAULT_WIDTH, help="Field's width")):
    curses.wrapper(main, height, width)

def main(screen, height, width):
    # Check that field's size is correct
    if (height < MIN_FIELD_SIZE or height > MAX_FIELD_SIZE or
        width < MIN_FIELD_SIZE or width > MAX_FIELD_SIZE):
        screen.addstr(0, 0,f"Wrong size of field, press any key (\
                             min size: {MIN_FIELD_SIZE}, \
                             max size: {MAX_FIELD_SIZE})")
        screen.getch()
        return
    
    game = Battleship(height, width)
    view = View(screen, game)

    # Game loop
    console_is_correct = view.resize()
    while True:
        
        # Check if console is correct
        if not console_is_correct:
            screen.clear()

            required_height, required_width = view.get_required_size()
            screen.addstr(0, 0, f"Requiered size of console is {required_height}x{required_width}")
            screen.addstr(1, 0, f"Resize console or press q to quit")
            ch = screen.getch()

            if ch == curses.KEY_RESIZE:
                console_is_correct = view.resize()
            elif ch == CONTROL_QUIT:
                break
            continue

        view.update(game)

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
            game.handle_input(ch)

    game.save()

if __name__ == "__main__":
    typer.run(run_curses)