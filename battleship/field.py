from random import randint
from math import sqrt, floor

TARGET_FILLING = 0.2

LEGEND = {
    "SHIP": "#",
    "DAMAGED": "X",

    "UNCHECKED": " ",
    "CHECKED": "~",
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

    def is_empty(self):
        return not self.is_ship

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

        self.tiles = [[Tile() for j in range(self.width)]
                      for i in range(self.height)]

        ships = self.choose_ships()
        self.place_ships(ships)

    def as_str(self, hidden=False):
        border = "+" + ("-" * self.width) + "+"

        lines = []
        for i in range(self.height):
            row = "".join([t.as_str(hidden=hidden) for t in self.tiles[i]])
            lines.append("|" + row + "|")

        return "\n".join([border] + lines + [border])

    def choose_ships(self):
        h, w = min(self.height, self.width), max(self.height, self.width)
        n = floor((sqrt(1 + 8 * h) - 1) // 2)  # max size of ship
        
        ships = []
        ships_set_space = 0
        for i in range(n, 0, -1):
            ships.append({"size": i, "count": n + 1 - i})
            ships_set_space += i * (n + 1 - i)

        sets_count = int(TARGET_FILLING // (ships_set_space / (h*w)))  # amount of sets of ships

        if sets_count == 0:
            sets_count = 1

        self.ships_space = 0
        for s in ships:
            s["count"] *= sets_count
            self.ships_space += s["size"] * s["count"]

        return ships
    
    def check_box(self, box_up, box_down, box_left, box_right):
        for i in range(box_up, box_down + 1):
            for j in range(box_left, box_right + 1):
                if not self.tiles[i][j].is_empty():
                    return False
        return True


    def place_ships(self, ships):
        ships.sort(key=lambda x: x["size"], reverse=True)

        for group in ships:
            size = group["size"]
            for i in range(group["count"]):
                vertical = bool(randint(0, 1))
                max_y = (self.height - size) if vertical else (self.height - 1)
                max_x = (self.width - size) if not vertical else (self.width - 1)

                while True:
                    y, x = randint(0, max_y), randint(0, max_x)
                    box_up = max(y - 1, 0)
                    box_left = max(x - 1, 0)
                    box_down = min(self.height - 1, (y + size) if vertical else y + 1)
                    box_right = min(self.width - 1, (x + size) if not vertical else x + 1)

                    if self.check_box(box_up, box_down, box_left, box_right):
                        if vertical:
                            for yi in range(y, y + size):
                                self.tiles[yi][x].put_ship()
                        else:
                            for xi in range(x, x + size):
                                self.tiles[y][xi].put_ship()
                        break

    def bomb(self, y, x):
        if self.tiles[y][x].bomb():
            self.ships_space -= 1

    @property
    def defeated(self):
        return not bool(self.ships_space)
