from typing import Dict, Tuple, Optional


class ConfigParser:
    """Parse and validate the maze configuration file."""

    def __init__(self, config_file: str) -> None:
        """Initialize parser with config file path."""
        self.config_file: str = config_file
        self.data: Dict[str, str] = {}

        self.width: int = 0
        self.height: int = 0
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.output_file: str = ""
        self.perfect: bool = False #zid fham hadi
        self.seed: Optional[int] = None #zid fham hadi

    def parse(self) -> None:
        """Main function to parse and validate configuration."""
        self._read_file()
        self._parse_values()
        self._validate_coordinates()

    def _read_file(self) -> None:
        """Read config file and store key=value pairs."""
        try:
            with open(self.config_file, "r") as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    if "=" not in line:
                        raise ValueError(f"Invalid line: {line}")

                    key, value = line.split("=", 1)
                    self.data[key.strip().upper()] = value.strip()

        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

    def _parse_values(self) -> None:
        """Convert config values to correct types."""

        try:
            self.width = int(self.data["WIDTH"])
            self.height = int(self.data["HEIGHT"])
        except KeyError as e:
            raise ValueError(f"Missing key: {e}")

        try:
            self.entry = self._parse_coordinates(self.data["ENTRY"])
            self.exit = self._parse_coordinates(self.data["EXIT"])
        except KeyError as e:
            raise ValueError(f"Missing key: {e}")

        try:
            self.output_file = self.data["OUTPUT_FILE"]
        except KeyError:
            raise ValueError("Missing OUTPUT_FILE")

        try:
            perfect_value = self.data["PERFECT"].lower()

            if perfect_value == "true":
                self.perfect = True
            elif perfect_value == "false":
                self.perfect = False
            else:
                raise ValueError("PERFECT must be True or False")

        except KeyError:
            raise ValueError("Missing PERFECT")

        if "SEED" in self.data:
            self.seed = int(self.data["SEED"])

    def _parse_coordinates(self, value: str) -> Tuple[int, int]:
        """Convert 'x,y' into tuple."""
        try:
            x_str, y_str = value.split(",")
            return int(x_str), int(y_str)
        except Exception:
            raise ValueError(f"Invalid coordinate format: {value}")

    def _validate_coordinates(self) -> None:
        """Check coordinates validity."""

        x_entry, y_entry = self.entry
        x_exit, y_exit = self.exit

        if not (0 <= x_entry < self.width and 0 <= y_entry < self.height):
            raise ValueError("Entry coordinates out of bounds")

        if not (0 <= x_exit < self.width and 0 <= y_exit < self.height):
            raise ValueError("Exit coordinates out of bounds")

        if self.entry == self.exit:
            raise ValueError("Entry and Exit cannot be the same")
