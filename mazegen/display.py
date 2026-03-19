import os
import sys
import time

RESET = "\033[0m"

WALL_COLOR    = "\033[40m"              # black
PATH_COLOR    = "\033[107m"             # bright white
SOL_COLOR     = "\033[105m"             # green
ENTRY_COLOR   = "\033[44m"             # blue
EXIT_COLOR    = "\033[41m"             # red
BLOCKED_COLOR = "\033[105m" # orange (42 cells)

CELL = "  "

ANIMATION_DELAY = 0.02  # 50ms per step


def move_cursor(row, col):
    """Move terminal cursor to (row, col), 1-indexed."""
    sys.stdout.write(f"\033[{row};{col}H")


def paint_cell(grid_row, grid_col, color, cell_width=2):
    """
    Paint a single grid slot in-place using cursor positioning.
    grid_row and grid_col are 0-indexed grid coordinates.
    Terminal rows/cols are 1-indexed, and each slot is cell_width chars wide.
    We add 3 to row to account for the header lines printed above the maze.
    """
    term_row = grid_row + 3         # 2 header lines + 1 blank line before maze
    term_col = grid_col * cell_width + 1
    move_cursor(term_row, term_col)
    sys.stdout.write(f"{color}{' ' * cell_width}{RESET}")
    sys.stdout.flush()


class TerminalDisplay:

    def __init__(self, generator, config):

        self.generator = generator
        self.config = config

        self.width  = config.width
        self.height = config.height

        self.show_solution = False
        self.solution_cells    = set()
        self.solution_passages = set()

        # Ordered list of grid-space coords for animation
        self.solution_steps = []

        self.blocked_cells = self._build_42_pattern()

    def _build_42_pattern(self):

        cx = self.width  // 2
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

        return {(x, y) for x, y in pattern if 0 <= x < self.width and 0 <= y < self.height}

    def build_solution_cells(self, directions):
        """
        Build solution_cells, solution_passages, and solution_steps.
        solution_steps is an ordered list of grid-space (gx, gy) coords
        for the animation — each step is either a cell center or a passage slot.
        """

        self.solution_cells.clear()
        self.solution_passages.clear()
        self.solution_steps = []

        x, y = self.config.entry
        self.solution_cells.add((x, y))
        self.solution_steps.append((x * 2 + 1, y * 2 + 1))  # entry cell in grid space

        for d in directions:

            gx = x * 2 + 1
            gy = y * 2 + 1

            if d == "N":
                passage = (gx, gy - 1)
                y -= 1
            elif d == "S":
                passage = (gx, gy + 1)
                y += 1
            elif d == "E":
                passage = (gx + 1, gy)
                x += 1
            elif d == "W":
                passage = (gx - 1, gy)
                x -= 1

            self.solution_passages.add(passage)
            self.solution_steps.append(passage)                   # passage slot
            self.solution_steps.append((x * 2 + 1, y * 2 + 1))  # next cell center

            self.solution_cells.add((x, y))

    def clear(self):

        if os.name == "nt":
            os.system("cls")
        else:
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.flush()

    def cell_color(self, x, y):

        if (x, y) == self.config.entry:
            return ENTRY_COLOR

        if (x, y) == self.config.exit:
            return EXIT_COLOR

        if self.show_solution and (x, y) in self.solution_cells:
            return SOL_COLOR

        if (x, y) in self.blocked_cells:
            return BLOCKED_COLOR

        return PATH_COLOR

    def _build_grid(self):
        """Build the full color grid (no animation)."""

        maze    = self.generator.maze
        grid_h  = self.height * 2 + 1
        grid_w  = self.width  * 2 + 1
        grid    = [[WALL_COLOR] * grid_w for _ in range(grid_h)]

        for y in range(self.height):
            for x in range(self.width):

                cell = maze[y][x]
                gx   = x * 2 + 1
                gy   = y * 2 + 1

                color = self.cell_color(x, y)
                grid[gy][gx] = color

                if not cell.north:
                    p = SOL_COLOR if (self.show_solution and (gx, gy-1) in self.solution_passages) else PATH_COLOR
                    if grid[gy-1][gx] != SOL_COLOR:
                        grid[gy-1][gx] = p

                if not cell.south:
                    p = SOL_COLOR if (self.show_solution and (gx, gy+1) in self.solution_passages) else PATH_COLOR
                    if grid[gy+1][gx] != SOL_COLOR:
                        grid[gy+1][gx] = p

                if not cell.east:
                    p = SOL_COLOR if (self.show_solution and (gx+1, gy) in self.solution_passages) else PATH_COLOR
                    if grid[gy][gx+1] != SOL_COLOR:
                        grid[gy][gx+1] = p

                if not cell.west:
                    p = SOL_COLOR if (self.show_solution and (gx-1, gy) in self.solution_passages) else PATH_COLOR
                    if grid[gy][gx-1] != SOL_COLOR:
                        grid[gy][gx-1] = p

        return grid

    def _print_grid(self, grid):
        """Print the full grid to stdout."""

        for row in grid:
            line = ""
            for color in row:
                line += f"{color}{CELL}{RESET}"
            print(line)

    def _print_header(self, status):
        status_str = "solution: ON " if status else "solution: OFF"
        print(f"  Seed: {self.generator.seed}  |  "
              f"{'Perfect' if self.config.perfect else 'Imperfect'} maze  |  "
              f"{status_str}\n")

    def draw(self):
        """Draw the full maze (no animation)."""

        self.clear()
        self._print_header(self.show_solution)
        grid = self._build_grid()
        self._print_grid(grid)

    def animate(self):
        """
        Draw the maze without solution, then animate the path
        step by step from entry to exit at 50ms per step.
        After animation finishes, solution stays visible.
        """

        # Draw maze with solution OFF first
        self.show_solution = False
        self.clear()
        self._print_header(False)
        grid = self._build_grid()
        self._print_grid(grid)

        # Hide cursor during animation
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        try:
            for gx, gy in self.solution_steps:

                # Determine color for this grid slot
                # Convert grid coords back to cell coords
                cx = (gx - 1) // 2
                cy = (gy - 1) // 2

                is_cell_center = (gx % 2 == 1 and gy % 2 == 1)

                if is_cell_center and (cx, cy) == self.config.entry:
                    color = ENTRY_COLOR
                elif is_cell_center and (cx, cy) == self.config.exit:
                    color = EXIT_COLOR
                else:
                    color = SOL_COLOR

                paint_cell(gy, gx, color)
                time.sleep(ANIMATION_DELAY)

        finally:
            # Always restore cursor, even if interrupted
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

        # Move cursor below the maze so the prompt appears cleanly
        move_cursor(self.height * 2 + 5, 1)
        sys.stdout.flush()

        self.show_solution = True