from typing import List, Optional
from random import shuffle, randint, seed
from .cell import Cell


DIR_BITS = {"N": 0, "E": 1, "S": 2, "W": 3}

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

        # create maze grid
        self.maze: List[List[Cell]] = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

    # ------------------------
    # WALL MANAGEMENT
    # ------------------------

    def open_wall(self, cell: Cell, direction: str) -> None:
        """Open a wall in the given direction."""
        cell.walls &= ~(1 << DIR_BITS[direction])

    # ------------------------
    # MAZE GENERATION
    # ------------------------

    def generate(self) -> None:
        """Start maze generation."""
        start_x = self.seed % self.width
        start_y = self.seed % self.height

        self._dfs(start_x, start_y)

    def _dfs(self, x: int, y: int) -> None:
        """Recursive DFS algorithm."""

        self.maze[y][x].visited = True

        directions = ["N", "E", "S", "W"]
        shuffle(directions)

        for direction in directions:

            dx, dy = DIR_MOVE[direction]

            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:

                if not self.maze[ny][nx].visited:

                    # open wall between cells
                    self.open_wall(self.maze[y][x], direction)
                    self.open_wall(self.maze[ny][nx], OPPOSITE[direction])

                    self._dfs(nx, ny)

    # ------------------------
    # UTILS
    # ------------------------

    def reset_visited(self) -> None:
        """Reset visited flag for all cells."""
        for row in self.maze:
            for cell in row:
                cell.visited = False

    # ------------------------
    # OUTPUT
    # ------------------------

    def to_hex(self) -> str:
        """Return maze encoded in hexadecimal."""

        output = ""

        for y in range(self.height):
            for x in range(self.width):
                output += f"{self.maze[y][x].walls:X}"

            output += "\n"

        return output