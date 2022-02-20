import curses

from battleship import Battleship

def main(screen):
    TITLE_HEIGHT = 1;
    TITLE_WIDTH  = 80;
    MESSAGE_HEIGHT = 2;
    MESSAGE_WIDTH  = 80;
    FIELD_HEIGHT = 100;
    FIELD_WIDTH  = 100;

    if (FIELD_WIDTH < 5 or FIELD_HEIGHT < 5):
        screen.addstr(0, 0, "Too small field, programm finished.")
        screen.getch()
        return


    TITLE = "<< BATTLESHIP GAME >>"
    MESSAGE_HELP = "Control: q - quit, arrows - choose target, space - bomb target"

    # required_height = 1 + \
    #                   TITLE_HEIGHT + \
    #                   1 + \
    #                   FIELD_HEIGHT + \
    #                   1 + \
    #                   MESSAGE_HEIGHT

    # required_width = max(TITLE_WIDTH, MESSAGE_WIDTH, FIELD_WIDTH * 2 + 5)


    win_title = curses.newwin(TITLE_HEIGHT, TITLE_WIDTH, 1, 0)
    win_left_field  = curses.newwin(1 + FIELD_HEIGHT + 2, 1 + FIELD_WIDTH + 2, \
                                    1 + TITLE_HEIGHT + 1, 0)
    win_right_field = curses.newwin(1+ FIELD_HEIGHT + 2, 1 + FIELD_WIDTH + 2, \
                                    1 + TITLE_HEIGHT + 1, 1 + FIELD_WIDTH + 1 + 1)
    win_message = curses.newwin(MESSAGE_HEIGHT, MESSAGE_WIDTH, \
                                1 + TITLE_HEIGHT + 1 + 1 + FIELD_HEIGHT + 2, 0)

    game = Battleship(FIELD_HEIGHT, FIELD_WIDTH)    
    
    # Game loop
    while True:
        screen.clear()
        # Check if screen is large enough
        # screen_height, screen_width = screen.getmaxyx()
        # if screen_height < required_height:
        #     screen.addstr(0, 0, "Please make your terminal higher.")
        #     continue
        # if screen_width < required_width:
        #     screen.addstr(0, 0, "Please make your terminal wider.")
        #     continue

        win_title.addstr(0, 0, TITLE)
        win_left_field.addstr(0, 0, game.left_field_as_str())
        win_right_field.addstr(0, 0, game.right_field_as_str())
        win_message.addstr(0, 0, MESSAGE_HELP)
        win_message.addstr(1, 0, "Try to win!!")

        cursor_x, cursor_y = game.get_cursor()
        win_right_field.chgat(cursor_x + 1, cursor_y + 1, 1, curses.A_REVERSE)

        screen.refresh()
        win_title.refresh()
        win_left_field.refresh()
        win_right_field.refresh()
        win_message.refresh()       

        if game.is_over():
            break

        ch = screen.getch()
        if ch in [curses.KEY_LEFT, curses.KEY_RIGHT, \
                  curses.KEY_UP, curses.KEY_DOWN]:
            game.move_cursor(ch)
        elif ch == ord(' '):
            game.make_move()
        elif ch == ord('q'):
            return

    win_message.addstr(1, 0, "Game over! (press any key)")
    win_message.refresh()
    screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)