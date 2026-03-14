from mazegen.config_parser import ConfigParser
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver


def main():

    parser = ConfigParser("config.txt")
    parser.parse()

    width = parser.width
    height = parser.height
    entry = parser.entry
    exit_ = parser.exit
    seed = parser.seed

    generator = MazeGenerator(width, height, 123)
    generator.generate()

    maze = generator.maze

    print("Generated Maze:")
    print(generator.to_hex())

    solver = MazeSolver(maze, entry, exit_)
    path = solver.solve()

    print("Solution path:")
    print(path)


if __name__ == "__main__":
    main()