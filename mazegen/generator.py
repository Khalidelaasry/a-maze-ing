import sys
from typing import List, Optional, Tuple
from random import shuffle, randint, seed
from collections import deque
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

IMPERFECT_RATIO = 0.15


class MazeGenerator:

    def __init__(
        self,
        width: int,
        height: int,
        seed_value: Optional[int] = None,
        perfect: bool = True,
        entry: Tuple[int, int] = (0, 0),
        exit_: Tuple[int, int] = None
    ):

        self.width = width
        self.height = height
        self.perfect = perfect
        self.entry = entry
        self.exit_ = exit_ if exit_ is not None else (width - 1, height - 1)

        if seed_value is None:
            seed_value = randint(0, 999999)

        self.seed = seed_value

        self.maze: List[List[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

        limit_needed = width * height + 100
        if sys.getrecursionlimit() < limit_needed:
            sys.setrecursionlimit(limit_needed)

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

        while True:

            self.maze = [
                [Cell() for _ in range(self.width)]
                for _ in range(self.height)
            ]

            seed(self.seed)

            start_x = self.seed % self.width
            start_y = self.seed % self.height

            self._dfs(start_x, start_y)

            if not self.perfect:
                self._add_loops()

            self.draw_42()

            if self._has_path():
                break

            # 42 blocked the path — try next seed
            self.seed = (self.seed + 1) % 1000000

    def _has_path(self):
        """BFS check: is there a path from entry to exit?"""

        start = self.entry
        end   = self.exit_

        visited = [[False] * self.width for _ in range(self.height)]
        queue = deque([start])
        visited[start[1]][start[0]] = True

        while queue:

            x, y = queue.popleft()

            if (x, y) == end:
                return True

            cell = self.maze[y][x]

            for direction, (dx, dy) in DIR_MOVE.items():

                nx, ny = x + dx, y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height and not visited[ny][nx]:

                    wall_open = (
                        (direction == "N" and not cell.north) or
                        (direction == "E" and not cell.east)  or
                        (direction == "S" and not cell.south) or
                        (direction == "W" and not cell.west)
                    )

                    if wall_open:
                        visited[ny][nx] = True
                        queue.append((nx, ny))

        return False

    def draw_42(self):

        cx = self.width // 2
        cy = self.height // 2

        pattern = [
            # "4"
            (cx-4, cy-2), (cx-4, cy-1), (cx-4, cy),
            (cx-3, cy),
            (cx-2, cy-2), (cx-2, cy-1), (cx-2, cy), (cx-2, cy+1), (cx-2, cy+2),
            # "2"
            (cx,   cy-2), (cx+1, cy-2), (cx+2, cy-2),
            (cx+2, cy-1),
            (cx,   cy),   (cx+1, cy),   (cx+2, cy),
            (cx,   cy+1),
            (cx,   cy+2), (cx+1, cy+2), (cx+2, cy+2),
        ]

        for x, y in pattern:

            if 0 <= x < self.width and 0 <= y < self.height:

                cell = self.maze[y][x]

                cell.north = True
                cell.east  = True
                cell.south = True
                cell.west  = True

                if y > 0:
                    self.maze[y-1][x].south = True
                if y < self.height - 1:
                    self.maze[y+1][x].north = True
                if x > 0:
                    self.maze[y][x-1].east  = True
                if x < self.width - 1:
                    self.maze[y][x+1].west  = True

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

    def _add_loops(self):

        candidates = []

        for y in range(self.height):
            for x in range(self.width):

                cell = self.maze[y][x]

                if x + 1 < self.width and cell.east:
                    candidates.append((x, y, "E"))

                if y + 1 < self.height and cell.south:
                    candidates.append((x, y, "S"))

        shuffle(candidates)

        remove_count = int(len(candidates) * IMPERFECT_RATIO)

        for x, y, direction in candidates[:remove_count]:

            dx, dy = DIR_MOVE[direction]
            nx, ny = x + dx, y + dy

            self.open_wall(self.maze[y][x], direction)
            self.open_wall(self.maze[ny][nx], OPPOSITE[direction])

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