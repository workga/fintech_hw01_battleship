from random import randint
from math import sqrt, floor

from config import *

LEGEND = {
    "SHIP": "#",
    "DAMAGED": "X",

    "UNCHECKED": " ",
    "CHECKED": "~",
    # for unchecked tiles which can't contain ship, add it later
    # "KNOWN"     : "-",
}

class Tile():
    def __init__(self):
        self.is_ship = False
        self.is_checked = False

    def is_empty(self):
        return not self.is_ship

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
            return self.is_ship


class Field():
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.tiles = [[Tile() for j in range(self.width)]
                                for i in range(self.height)]

        self.ships_area = 0
        self.fill()

    def get_ships_area(self):
        return self.ships_area

    def is_defeated(self):
        return self.ships_area <= 0

    def as_str(self, hidden=False):
        border = "+" + ("-" * self.width) + "+"

        lines = [border]
        for i in range(self.height):
            row = "".join([t.as_str(hidden=hidden) for t in self.tiles[i]])
            lines.append("|" + row + "|")
        lines.append(border)

        return "\n".join(lines)

    def fill(self):
        ships, self.ships_area = self.choose_ships()

        ships.sort(key=lambda x: x["size"], reverse=True)

        for ship in ships:
            size = ship["size"]
            for i in range(ship["count"]):
                self.place_ship(size)

    def choose_ships(self):
        """
        Choose the correct number of ships with the correct sizes
        """
        h, w = min(self.height, self.width), max(self.height, self.width)

        # n is max size of ships,
        # it looks complicated, but it's based on math and works great
        n = floor((sqrt(1 + 8 * h) - 1) // 2)
        

        # choose one set of ships,
        # ships_area is total area of all ships in choosen set
        ships = []
        ships_area = 0
        for i in range(1, n + 1):
            ships.append({"size": i, "count": n + 1 - i})
            ships_area += i * (n + 1 - i)
        
        # repeat this set several times
        sets_count = floor(TARGET_FILLING // (ships_area / (h*w)))
        if sets_count == 0:
            sets_count = 1

        for s in ships:
            s["count"] *= sets_count
        ships_area *= sets_count

        return ships, ships_area
    
    def check_region(self, region_up, region_down, region_left, region_right):
        """
        Check whether choosen region contains ships or not
        """
        for i in range(region_up, region_down + 1):
            for j in range(region_left, region_right + 1):
                if not self.tiles[i][j].is_empty():
                    return False
        return True


    def place_ship(self, size):
        """
        Correctly place ship on the field
        """
        while True:
            vertical = bool(randint(0, 1))
            max_y = (self.height - size) if vertical else (self.height - 1)
            max_x = (self.width - size) if not vertical else (self.width - 1)

            y, x = randint(0, max_y), randint(0, max_x)

            # define surrounding region
            region_up = max(y - 1, 0)
            region_left = max(x - 1, 0)
            region_down = min(
                self.height - 1,
                (y + size) if vertical else y + 1
            )
            region_right = min(
                self.width - 1,
                (x + size) if not vertical else x + 1
            )

            if self.check_region(region_up, region_down,
                                 region_left, region_right):
                if vertical:
                    for yi in range(y, y + size):
                        self.tiles[yi][x].put_ship()
                else:
                    for xi in range(x, x + size):
                        self.tiles[y][xi].put_ship()
                break

    def bomb(self, y, x):
        if self.tiles[y][x].bomb():
            self.ships_area -= 1
