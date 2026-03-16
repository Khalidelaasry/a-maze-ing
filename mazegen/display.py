import os

RESET = "\033[0m"
WALL_COLOR = "\033[40m"   # black walls
PATH_COLOR = "\033[47m"   # white path
SOL_COLOR = "\033[42m"    # green solution
ENTRY_COLOR = "\033[44m"  # blue entry
EXIT_COLOR = "\033[41m"   # red exit


class TerminalDisplay:
    def __init__(self, generator, config):
        self.generator = generator
        self.config = config
        self.width = config.width
        self.height = config.height

    def render(self, solution_path=None):
        os.system('cls' if os.name == 'nt' else 'clear')

        path_set = set(solution_path) if solution_path else set()

        print(f"Maze: {self.width}x{self.height}")
        print("Controls: [Enter] Regenerate | [S] Toggle Solution | [Q] Quit\n")

        W = f"{WALL_COLOR}  "

        for y in range(self.height):
            row_top = ""
            row_mid = ""
            row_bot = ""

            for x in range(self.width):
                cell = self.generator.maze[y][x]

                # cell color
                if (x, y) == self.config.entry:
                    C = f"{ENTRY_COLOR}  "
                elif (x, y) == self.config.exit:
                    C = f"{EXIT_COLOR}  "
                elif (x, y) in path_set:
                    C = f"{SOL_COLOR}  "
                else:
                    C = f"{PATH_COLOR}  "

                # CORRECT WALL CHECK
                wall_n = cell.north
                wall_e = cell.east
                wall_s = cell.south
                wall_w = cell.west

                N = W if wall_n else C
                S = W if wall_s else C
                WEST = W if wall_w else C
                EAST = W if wall_e else C

                row_top += f"{W}{N}{W}"
                row_mid += f"{WEST}{C}{EAST}"
                row_bot += f"{W}{S}{W}"

            print(row_top + RESET)
            print(row_mid + RESET)
            print(row_bot + RESET)