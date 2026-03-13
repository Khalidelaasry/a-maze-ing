class Cell:
    def __init__(
        self,
        north: bool = True,
        east: bool = True,
        south: bool = True,
        west: bool = True,
        static: bool = False,
        visited: bool = False
    ) -> None:
        """Initialize the cell"""

        # walls
        self.north: bool = north
        self.east: bool = east
        self.south: bool = south
        self.west: bool = west

        self.visited: bool = visited
        self.static: bool = static

        self.entrance: bool = False
        self.exit: bool = False
