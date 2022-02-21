DEBUG = True

TITLE_HEIGHT = 1
TITLE_WIDTH  = 80
TITLE_TEXT   = "<<< BATTLESHIP >>>"

MESSAGE_HEIGHT = 6
MESSAGE_WIDTH  = 80
MESSAGE_CONTROL = """CONTROL:\n""" \
                  """[q]      - exit\n""" \
                  """[arrows] - move cursor\n""" \
                  """[space]  - bomb"""

FIELD_DEFAULT_HEIGHT = 10
FIELD_DEFAULT_WIDTH  = 10
MIN_FIELD_SIZE = 5
MAX_FIELD_SIZE = 30

CONTROL_QUIT = ord('q')
CONTROL_BOMB = ord(' ')

FILENAME = ".battleforce_saved"