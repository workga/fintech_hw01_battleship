import curses

from battleship import Battleship

def main(screen):
    # Clear screen
    screen.clear()

    # screen_height, screen_width = screen.getmaxyx()
    game = Battleship(10, 10)
    
    while True:
        screen.addstr(0, 0, game.as_str())

        ch = screen.getch()
        if ch in [curses.KEY_LEFT, curses.KEY_RIGHT, \
                  curses.KEY_UP, curses.KEY_DOWN]:
            game.move_cursor(ch)
        elif ch == ord(' '):
            game.make_move()
            if game.is_over():
                break
        elif ch == ord('q'):
            return
    screen.addstr(0, 0, game.as_str() + "\nGame over!")
    screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)