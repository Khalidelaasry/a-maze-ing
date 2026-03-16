from typing import List, Optional
from random import shuffle, randint, seed
from .cell import Cell

DIR_MOVE = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}

OPPOSITE = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E"
}


class MazeGenerator:

    def __init__(self, width: int, height: int, seed_value: Optional[int] = None):

        self.width = width
        self.height = height

        if seed_value is None:
            seed_value = randint(0, 999999)

        self.seed = seed_value
        seed(self.seed)

        self.maze: List[List[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def open_wall(self, cell: Cell, direction: str):

        if direction == "N":
            cell.north = False
        elif direction == "E":
            cell.east = False
        elif direction == "S":
            cell.south = False
        elif direction == "W":
            cell.west = False

    def generate(self):

        start_x = self.seed % self.width
        start_y = self.seed % self.height

        self._dfs(start_x, start_y)

    def _dfs(self, x, y):

        self.maze[y][x].visited = True

        directions = ["N", "E", "S", "W"]
        shuffle(directions)

        for direction in directions:

            dx, dy = DIR_MOVE[direction]

            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:

                if not self.maze[ny][nx].visited:

                    self.open_wall(self.maze[y][x], direction)
                    self.open_wall(self.maze[ny][nx], OPPOSITE[direction])

                    self._dfs(nx, ny)

    def to_hex(self):

        output = ""

        for y in range(self.height):

            for x in range(self.width):

                cell = self.maze[y][x]

                value = (
                    (1 if cell.north else 0) +
                    (2 if cell.east else 0) +
                    (4 if cell.south else 0) +
                    (8 if cell.west else 0)
                )

                output += f"{value:X}"

            output += "\n"

        return output

    # draw blocked "42"
    def draw_42(self):

        cx = self.width // 2
        cy = self.height // 2

        pattern = [

            (cx-4,cy-2),(cx-4,cy-1),(cx-4,cy),
            (cx-3,cy),
            (cx-2,cy-2),(cx-2,cy-1),(cx-2,cy),(cx-2,cy+1),(cx-2,cy+2),

            (cx,cy-2),(cx+1,cy-2),(cx+2,cy-2),
            (cx+2,cy-1),
            (cx,cy),(cx+1,cy),(cx+2,cy),
            (cx,cy+1),
            (cx,cy+2),(cx+1,cy+2),(cx+2,cy+2),
        ]

        for x, y in pattern:

            if 0 <= x < self.width and 0 <= y < self.height:

                cell = self.maze[y][x]

                cell.north = True
                cell.east = True
                cell.south = True
                cell.west = True