from typing import List, Tuple
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

        self.solutions: List[List[str]] = []

    def solve(self):

        self._reset_visited()

        path = []

        self._dfs(self.entry[0], self.entry[1], self.exit[0], self.exit[1], path)

        if not self.solutions:
            return []

        return min(self.solutions, key=len)

    def _dfs(self, x, y, target_x, target_y, path):

        if x == target_x and y == target_y:
            self.solutions.append(list(path))
            return

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

                    path.append(direction)

                    self._dfs(nx, ny, target_x, target_y, path)

                    path.pop()

        self.maze[y][x].visited = False

    def _reset_visited(self):

        for row in self.maze:
            for cell in row:
                cell.visited = False