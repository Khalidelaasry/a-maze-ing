import os

RESET = "\033[0m"

WALL_COLOR = "\033[40m"
PATH_COLOR = "\033[107m"
SOL_COLOR = "\033[42m"
ENTRY_COLOR = "\033[44m"
EXIT_COLOR = "\033[41m"

CELL = "  "


class TerminalDisplay:

    def __init__(self, generator, config):

        self.generator = generator
        self.config = config

        self.width = config.width
        self.height = config.height

        self.show_solution = True

        self.solution_cells = set()

    def build_solution_cells(self, directions):

        self.solution_cells.clear()

        x, y = self.config.entry
        self.solution_cells.add((x, y))

        for d in directions:

            if d == "N":
                y -= 1
            elif d == "S":
                y += 1
            elif d == "E":
                x += 1
            elif d == "W":
                x -= 1

            self.solution_cells.add((x, y))

    def clear(self):

        if os.name == "nt":
            os.system("cls")
        else:
            print("\033[2J\033[H", end="")

    def cell_color(self, x, y):

        if (x, y) == self.config.entry:
            return ENTRY_COLOR

        if (x, y) == self.config.exit:
            return EXIT_COLOR

        if self.show_solution and (x, y) in self.solution_cells:
            return SOL_COLOR

        return PATH_COLOR

    def draw(self):

        self.clear()

        maze = self.generator.maze

        for y in range(self.height):

            top = ""
            mid = ""
            bot = ""

            for x in range(self.width):

                cell = maze[y][x]

                C = self.cell_color(x, y)

                N = WALL_COLOR if cell.north else C
                S = WALL_COLOR if cell.south else C
                E = WALL_COLOR if cell.east else C
                W = WALL_COLOR if cell.west else C

                top += f"{WALL_COLOR}{CELL}{RESET}{N}{CELL}{RESET}{WALL_COLOR}{CELL}{RESET}"
                mid += f"{W}{CELL}{RESET}{C}{CELL}{RESET}{E}{CELL}{RESET}"
                bot += f"{WALL_COLOR}{CELL}{RESET}{S}{CELL}{RESET}{WALL_COLOR}{CELL}{RESET}"

            print(top)
            print(mid)
            print(bot)