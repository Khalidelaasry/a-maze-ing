from typing import List, Tuple
from collections import deque
from .cell import Cell

DIR_MOVE = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}


class MazeSolver:

    def __init__(self, maze: List[List[Cell]], entry: Tuple[int, int], exit_: Tuple[int, int]):

        self.maze = maze
        self.entry = entry
        self.exit = exit_

        self.height = len(maze)
        self.width = len(maze[0])

    def solve(self):

        self._reset_visited()

        queue = deque()
        queue.append((self.entry[0], self.entry[1], []))

        while queue:

            x, y, path = queue.popleft()

            if (x, y) == self.exit:
                return path

            self.maze[y][x].visited = True

            for direction, (dx, dy) in DIR_MOVE.items():

                nx = x + dx
                ny = y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:

                    cell = self.maze[y][x]

                    wall_open = (
                        (direction == "N" and not cell.north) or
                        (direction == "E" and not cell.east) or
                        (direction == "S" and not cell.south) or
                        (direction == "W" and not cell.west)
                    )

                    if wall_open and not self.maze[ny][nx].visited:

                        queue.append((nx, ny, path + [direction]))

        return []

    def _reset_visited(self):

        for row in self.maze:
            for cell in row:
                cell.visited = False