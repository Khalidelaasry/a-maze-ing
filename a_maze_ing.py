import sys
import random

from mazegen.config_parser import ConfigParser
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver
from mazegen.display import TerminalDisplay
from mazegen.maze_writer import write_maze_file, verify_maze_file


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

    while True:

        seed = config.seed if config.seed is not None else random.randint(0, 999999)

        generator = MazeGenerator(config.width, config.height, seed)
        generator.generate()
        generator.draw_42()

        solver = MazeSolver(generator.maze, config.entry, config.exit)
        directions = solver.solve()

        write_maze_file(
            generator,
            config.entry,
            config.exit,
            directions,
            config.output_file
        )

        verify_maze_file(
            config.output_file,
            config.width,
            config.height
        )

        display = TerminalDisplay(generator, config)
        display.build_solution_cells(directions)
        display.draw()

        cmd = input("Command [Enter=regen | s=solution | q=quit] > ").strip().lower()

        if cmd == "q":
            break

        if cmd == "s":
            display.show_solution = not display.show_solution
            display.draw()


if __name__ == "__main__":
    main()