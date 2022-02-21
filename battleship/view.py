import curses
from config import *

class View():
    def __init__(self, screen, field_height, field_width):
        self.field_height = field_height
        self.field_width  = field_width

        self.screen = screen
        self.windows = {}

        self.create_windows()

    def create_windows(self):
        self.windows["title"] = curses.newwin(TITLE_HEIGHT, TITLE_WIDTH, 1, 0)
        self.windows["left_field"]  = curses.newwin(self.field_height + 3, self.field_width + 3, \
                                                    TITLE_HEIGHT + 2, 0)
        self.windows["right_field"] = curses.newwin(self.field_height + 3, self.field_width + 3, \
                                                    TITLE_HEIGHT + 2, self.field_width + 3)
        self.windows["message"] = curses.newwin(MESSAGE_HEIGHT, MESSAGE_WIDTH, \
                                                TITLE_HEIGHT + 2 + self.field_height + 3, 0)
    
    def update(self, left_field_str, right_field_str, cursor_y, cursor_x, status):
        self.screen.clear()

        self.windows["title"].addstr(0, 0, TITLE_TEXT)
        self.windows["left_field"].addstr(0, 0, left_field_str)
        self.windows["right_field"].addstr(0, 0, right_field_str)
        self.windows["right_field"].chgat(cursor_y + 1, cursor_x + 1, 1, curses.A_REVERSE)
        self.windows["message"].addstr(0, 0, MESSAGE_CONTROL)
        self.windows["message"].addstr(MESSAGE_HEIGHT - 1, 0, status)

        self.refresh()


    def refresh(self):
        self.screen.refresh()
        self.windows["title"].refresh()
        self.windows["left_field"].refresh()
        self.windows["right_field"].refresh()
        self.windows["message"].refresh()  