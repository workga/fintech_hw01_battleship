from mailbox import linesep
from random import randint

LEGEND = {
    "SHIP"    : "#",
    "DAMAGED" : "X",

    "UNCHECKED" : " ",
    "CHECKED"   : "~",
    # "KNOWN"     : "-",  # for unchecked tiles which can't contain ship, add later
}

class Tile():
    def __init__(self):
        self.is_ship = False
        self.is_checked = False

    def as_str(self, hidden=False):
        if self.is_checked:
            if self.is_ship:
                return LEGEND["DAMAGED"]
            else:
                return LEGEND["CHECKED"]
        else:
            if self.is_ship:
                return LEGEND["UNCHECKED"] if hidden else LEGEND["SHIP"]
            else:
                return LEGEND["UNCHECKED"]
    
    def put_ship(self):
        self.is_ship = True

    def bomb(self):
        if self.is_checked:
            return False
        else:
            self.is_checked = True

            if self.is_ship:
                return True
            else:
                return False


class Field():
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.tiles = [[Tile() for j in range(self.width)] \
                                for i in range(self.height)]
        self.create_ships()

    def as_str(self, hidden=False):
        border = "+" + ("-" * self.width) + "+"
        
        lines = []
        for i in range(self.height):
            row = "".join([t.as_str(hidden=hidden) for t in self.tiles[i]])
            lines.append("|" + row + "|")
        

        return "\n".join([border] + lines + [border])

    def create_ships(self):
        # use some algorithm

        self.ships_count = 1
        y, x = randint(0, self.height - 1), randint(0, self.width - 1)

        self.tiles[y][x].put_ship()

    def bomb(self, y, x):
        if self.tiles[y][x].bomb():
            self.ships_count -= 1

    @property
    def defeated(self):
        return not bool(self.ships_count)
