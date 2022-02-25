import curses

from config import (
    W_TITLE_H,
    W_HELP_H,
    W_STATUS_H,
    TITLE_TEXT,
    HELP_TEXT,
    STATUS_TEXT_MAX_LEN,
)


class View:
    def __init__(self, screen, game):
        self.game = game
        self.field_height, self.field_width = game.get_fields_size()

        self.required_height = W_TITLE_H + W_HELP_H + W_STATUS_H + self.field_height + 3
        self.required_width = max(
            self.field_width * 2 + 5,
            len(TITLE_TEXT),
            max(map(len, HELP_TEXT.split())),
            STATUS_TEXT_MAX_LEN,
        )

        self.screen = screen
        self.windows = {}

    def get_required_size(self):
        return self.required_height, self.required_width

    def resize(self):
        if not self.check_console_size():
            return False

        _, screen_w = self.screen.getmaxyx()

        self.windows["title"] = curses.newwin(W_TITLE_H, screen_w, 0, 0)
        self.windows["help"] = curses.newwin(W_HELP_H, screen_w, W_TITLE_H, 0)
        self.windows["left_status"] = curses.newwin(
            W_STATUS_H, screen_w // 2, W_TITLE_H + W_HELP_H, 0
        )
        self.windows["right_status"] = curses.newwin(
            W_STATUS_H, screen_w // 2, W_TITLE_H + W_HELP_H, screen_w // 2
        )
        self.windows["left_field"] = curses.newwin(
            self.field_height + 3, screen_w // 2, W_TITLE_H + W_HELP_H + W_STATUS_H, 0
        )
        self.windows["right_field"] = curses.newwin(
            self.field_height + 3,
            screen_w // 2,
            W_TITLE_H + W_HELP_H + W_STATUS_H,
            screen_w // 2,
        )

        return True

    def update(self):
        cursor_y, cursor_x = self.game.get_cursor_pos()
        left_status_str, right_status_str = self.game.get_statuses_as_str()
        left_field_str, right_field_str = self.game.get_fields_as_str()

        self.screen.clear()

        View.centered_output(self.windows["title"], TITLE_TEXT)
        View.centered_output(self.windows["help"], HELP_TEXT)
        View.centered_output(self.windows["left_status"], left_status_str)
        View.centered_output(self.windows["right_status"], right_status_str)
        View.centered_output(self.windows["left_field"], left_field_str)

        pad_y, pad_x = self.centered_output(
            self.windows["right_field"], right_field_str
        )

        self.windows["right_field"].addstr(
            pad_y + cursor_y + 1, pad_x + cursor_x + 1, "", curses.A_REVERSE
        )

        self.refresh()

    def refresh(self):
        self.screen.refresh()
        for w in self.windows.values():
            w.refresh()

    @staticmethod
    def centered_output(window, text):
        """
        Output text in the center of the window
        """
        lines = text.split("\n")
        text_height = len(lines)
        text_width = max(map(len, lines))
        window_height, window_width = window.getmaxyx()

        pad_y = (window_height - text_height) // 2
        pad_x = (window_width - text_width) // 2

        for i, line in enumerate(lines):
            window.addstr(pad_y + i, pad_x, line)

        return pad_y, pad_x

    def check_console_size(self):
        screen_height, screen_width = self.screen.getmaxyx()

        return (
            screen_height >= self.required_height
            and screen_width >= self.required_width
        )
