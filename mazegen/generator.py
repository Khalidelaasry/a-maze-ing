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
    """Generate a maze using DFS (recursive backtracking)."""

    def __init__(
        self,
        width: int,
        height: int,
        seed_value: Optional[int] = None
    ) -> None:

        if width <= 1 or height <= 1:
            raise ValueError("Maze size too small")

        self.width = width
        self.height = height

        if seed_value is None:
            seed_value = randint(0, 999999)

        self.seed = seed_value
        seed(self.seed)

        self.maze: List[List[Cell]] = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

    # ------------------------
    # WALL MANAGEMENT
    # ------------------------

    def open_wall(self, cell: Cell, direction: str) -> None:

        if direction == "N":
            cell.north = False
        elif direction == "E":
            cell.east = False
        elif direction == "S":
            cell.south = False
        elif direction == "W":
            cell.west = False

    # ------------------------
    # MAZE GENERATION
    # ------------------------

    def generate(self) -> None:

        start_x = self.seed % self.width
        start_y = self.seed % self.height

        self._dfs(start_x, start_y)

    def _dfs(self, x: int, y: int) -> None:

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

    # ------------------------
    # OUTPUT
    # ------------------------

    def _cell_to_value(self, cell: Cell) -> int:

        value = 0

        if cell.north:
            value += 1
        if cell.east:
            value += 2
        if cell.south:
            value += 4
        if cell.west:
            value += 8

        return value

    def to_hex(self) -> str:

        output = ""

        for y in range(self.height):
            for x in range(self.width):

                value = self._cell_to_value(self.maze[y][x])
                output += f"{value:X}"

            output += "\n"

        return output

    # ------------------------
    # DRAW 42
    # ------------------------

    def carve_42(self) -> None:
        """Carve the number 42 in the center of the maze."""

        cx = self.width // 2
        cy = self.height // 2

        coords = [

            # 4
            (cx-4,cy-2),(cx-4,cy-1),(cx-4,cy),
            (cx-3,cy),
            (cx-2,cy-2),(cx-2,cy-1),(cx-2,cy),(cx-2,cy+1),(cx-2,cy+2),

            # 2
            (cx,cy-2),(cx+1,cy-2),(cx+2,cy-2),
            (cx+2,cy-1),
            (cx,cy),(cx+1,cy),(cx+2,cy),
            (cx,cy+1),
            (cx,cy+2),(cx+1,cy+2),(cx+2,cy+2),
        ]

        for x, y in coords:

            if 0 <= x < self.width and 0 <= y < self.height:

                cell = self.maze[y][x]

                # open all walls to make visible path
                cell.north = False
                cell.south = False
                cell.east = False
                cell.west = False