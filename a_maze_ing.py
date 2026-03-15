import sys
sys.setrecursionlimit(2000000)

import random
import os

from mazegen.config_parser import ConfigParser
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver

class TerminalDisplay:
    def __init__(self, config, hex_data_string):
        self.config = config
        self.width = config.width
        self.height = config.height
        self.rows = hex_data_string.strip().split('\n')
        
    def render(self, solution_path=None):
        RESET = "\033[0m"
        WALL = f"\033[47m  {RESET}"
        PATH = f"\033[40m  {RESET}"
        SOL  = f"\033[42m  {RESET}"
        ENT  = f"\033[44m  {RESET}"
        EXIT = f"\033[41m  {RESET}"

        os.system('cls' if os.name == 'nt' else 'clear')
        path_set = set(solution_path) if solution_path else set()

        print(f"Maze Size: {self.width}x{self.height}")
        print("Controls: [Enter] Regenerate | [S] Toggle Solution | [Q] Quit\n")

        for y, row_str in enumerate(self.rows):
            if y >= self.height:
                break
            
            top, mid, bot = "", "", ""

            for x, char in enumerate(row_str):
                if x >= self.width:
                    break

                try:
                    val = int(char, 16)
                except ValueError:
                    val = 15
                
                if (x,y) == self.config.entry:
                    floor = ENT
                elif (x,y) == self.config.exit:
                    floor = EXIT
                elif (x,y) in path_set:
                    floor = SOL
                else:
                    floor = PATH

                w_n = WALL if (val & 1) else floor
                w_e = WALL if (val & 2) else floor
                w_s = WALL if (val & 4) else floor
                w_w = WALL if (val & 8) else floor

                top += f"{WALL}{w_n}{WALL}"
                mid += f"{w_w}{floor}{w_e}"
                bot += f"{WALL}{w_s}{WALL}"

            print(top)
            print(mid)
            print(bot)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        config = ConfigParser(sys.argv[1])
        config.parse()
    except Exception as e:
        print(f"Config Error: {e}")
        return

    show_path = False 

    while True:
        while True:
            try:
                seed = config.seed if config.seed is not None else random.randint(0, 999999)
                gen = MazeGenerator(config.width, config.height, seed)
                gen.generate()
                hex_data = gen.to_hex()
                if "F" not in hex_data:
                    break
                elif config.seed is not None:
                    break 
            except RecursionError:
                continue

        solver = MazeSolver(gen.maze, config.entry, config.exit)
        directions = solver.solve() 

        full_file_content = ""
        full_file_content += hex_data + "\n"
        full_file_content += f"{config.entry[0]},{config.entry[1]}\n"
        full_file_content += f"{config.exit[0]},{config.exit[1]}\n"
        full_file_content += "".join(directions) + "\n"

        with open(config.output_file, "w") as f:
            f.write(full_file_content)

        path_coords = []
        if show_path:
            cx, cy = config.entry
            path_coords.append((cx, cy))
            for move in directions:
                if move == 'N':
                    cy -= 1
                elif move == 'S':
                    cy += 1
                elif move == 'E':
                    cx += 1
                elif move == 'W':
                    cx -= 1
                path_coords.append((cx, cy))

        display = TerminalDisplay(config, hex_data)
        display.render(solution_path=path_coords)
        
        cmd = input("Command > ").strip().lower()
        if cmd == 'q':
            break
        elif cmd == 's': 
            show_path = not show_path
            config.seed = seed
        else:
            config.seed = None
            show_path = False

if __name__ == "__main__":
    main()