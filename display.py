import os
import sys

RESET = "\033[0m"
WALL_COLOR = "\033[47m"
PATH_COLOR = "\033[40m"
SOL_COLOR = "\033[42m"
ENTRY_COLOR = "\033[44m"
EXIT_COLOR = "\033[41m"

class TerminalDisplay:
    def __init__(self, generator, config):
        self.generator = generator
        self.config = config
        self.width = config.width
        self.height = config.height
        
    def render(self, solution_path: list = None):
        os.system('cls' if os.name == 'nt' else 'clear')

        path_set = set(solution_path) if solution_path else set()

        print(f"Maze: {self.width}x{self.height}")
        print("Controls: [Enter] Regenerate | [S] Toggle Solution | [Q] Quit\n")

        W = f"{WALL_COLOR}  {RESET}"

        for y in range(self.height):
            row_top = ""
            row_mid = ""
            row_bot = ""

            for x in range(self.width):
                cell = self.generator.maze[y][x]
                
                if (x, y) == self.config.entry:
                    C = f"{ENTRY_COLOR}  {RESET}"
                elif (x, y) == self.config.exit:
                    C = f"{EXIT_COLOR}  {RESET}"
                elif (x, y) in path_set:
                    C = f"{SOL_COLOR}  {RESET}"
                else:
                    C = f"{PATH_COLOR}  {RESET}"

                wall_n = (cell.walls & 1) != 0
                wall_e = (cell.walls & 2) != 0
                wall_s = (cell.walls & 4) != 0
                wall_w = (cell.walls & 8) != 0

                N = W if wall_n else C
                S = W if wall_s else C
                WEST = W if wall_w else C
                EAST = W if wall_e else C

                row_top += f"{W}{N}{W}"
                row_mid += f"{WEST}{C}{EAST}"
                row_bot += f"{W}{S}{W}"

            print(row_top)
            print(row_mid)
            print(row_bot)