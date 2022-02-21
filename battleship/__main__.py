import os
import curses
import typer
# from typing import Optional

from config import *
from battleship import Battleship
from view import View

def run_curses(height: int=typer.Argument(None, help="Field's height"), \
               width: int=typer.Argument(None, help="Field's width"), \
               dirname: str=typer.Option(None, help="Directory for saving/loading game")):
    curses.wrapper(main, height, width, dirname)

def main(screen, height, width, dirname):
    no_size = True
    use_file = True
    height = height if height else FIELD_DEFAULT_HEIGHT
    width  = width if width else FIELD_DEFAULT_WIDTH
    # Check that field's size is correct
    if (height < MIN_FIELD_SIZE or height > MAX_FIELD_SIZE or
        width < MIN_FIELD_SIZE or width > MAX_FIELD_SIZE):
        screen.addstr(0, 0,f"Wrong size of field (\
                             min size: {MIN_FIELD_SIZE}, \
                             max size: {MAX_FIELD_SIZE})")
        screen.getch()
        return
    # check if there is saved game
    # game = None
    # if dirname and os.path.isfile("/".join([dirname, FILENAME])):
    #     game = Battleship

    game = Battleship(height, width)
    view = View(screen, height, width)
    
    # Game loop
    while True:
        left_field_str = game.left_field_as_str()
        right_field_str = game.right_field_as_str()
        cursor_y, cursor_x = game.get_cursor()
        status = game.get_status()

        view.update(left_field_str, \
                    right_field_str, \
                    cursor_y, cursor_x, \
                    status)    

        if game.is_over():
            #delete file
            break 
        
        # handle input
        ch = screen.getch()
        if ch == CONTROL_QUIT:
            # pickle
            # with open((PATH + name), "wb") as f_toks:
            #     pickle.dump(toks, f_toks)

            # with open((PATH + name), "rb") as f_toks:
            #     toks = pickle.load(f_toks)
            # if dirname and 
            return
        game.handle_input(ch)

    screen.getch()

if __name__ == "__main__":
    typer.run(run_curses)