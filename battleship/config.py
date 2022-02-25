W_TITLE_H = 3
W_HELP_H = 6
W_STATUS_H = 2

STATUS_TEXT_MAX_LEN = 40

TITLE_TEXT = "<<< BATTLESHIP >>>"
HELP_TEXT = (
    """CONTROL:"""
    """[q]      - quit"""
    """[arrows] - move cursor"""
    """[space]  - drop bomb"""
)

FIELD_DEFAULT_HEIGHT = 10
FIELD_DEFAULT_WIDTH = 10

MIN_FIELD_SIZE = 5
MAX_FIELD_SIZE = 30

CONTROL_QUIT = ord("q")
CONTROL_BOMB = ord(" ")

MAX_RESIZE_ATTEMPTS_COUNT = 10
MAX_CONTROL_ATTEMPTS_COUNT = 10

TARGET_FILLING = 0.2  # what percent of area fill by ships
