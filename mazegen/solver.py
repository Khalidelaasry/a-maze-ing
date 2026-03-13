from typing import List, Tuple
from .cell import Cell


DIR_MOVE = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}


class MazeSolver:
    """Solve a maze and find the shortest path."""

    def __init__(
        self,
        maze: List[List[Cell]],
        entry: Tuple[int, int],
        exit_: Tuple[int, int]
    ) -> None:

        self.maze = maze
        self.entry = entry
        self.exit = exit_

        self.height = len(maze)
        self.width = len(maze[0])

        self.solutions: List[List[str]] = []

    # ------------------------
    # PUBLIC SOLVE
    # ------------------------

    def solve(self) -> List[str]:
        """Return shortest path."""

        self._reset_visited()

        path: List[str] = []

        self._dfs(
            self.entry[0],
            self.entry[1],
            self.exit[0],
            self.exit[1],
            path
        )

        if not self.solutions:
            return []

        return min(self.solutions, key=len)

    # ------------------------
    # DFS SOLVER
    # ------------------------

    def _dfs(
        self,
        x: int,
        y: int,
        target_x: int,
        target_y: int,
        path: List[str]
    ) -> None:

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

                    self._dfs(
                        nx,
                        ny,
                        target_x,
                        target_y,
                        path
                    )

                    path.pop()

        self.maze[y][x].visited = False

    # ------------------------
    # UTILS
    # ------------------------

    def _reset_visited(self) -> None:
        """Reset visited flag in maze."""

        for row in self.maze:
            for cell in row:
                cell.visited = False
