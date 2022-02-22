DEBUG = True

W_TITLE_H = 3
W_HELP_H = 6
W_STATUS_H = 2

TITLE_TEXT   = "<<< BATTLESHIP >>>"
HELP_TEXT = """CONTROL:\n""" \
            """[q]      - exit\n""" \
            """[arrows] - move cursor\n""" \
            """[space]  - bomb"""
STATUS_TEXT_MAX_LEN = 40

FIELD_DEFAULT_HEIGHT = 10
FIELD_DEFAULT_WIDTH  = 10
MIN_FIELD_SIZE = 5
MAX_FIELD_SIZE = 30

CONTROL_QUIT = ord('q')
CONTROL_BOMB = ord(' ')

FILENAME = ".battleforce_saved"

TARGET_FILLING = 0.2 # what percent of space fill by ships