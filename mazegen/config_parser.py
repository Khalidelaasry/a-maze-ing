from typing import Dict, Tuple, Optional


class ConfigParser:

    def __init__(self, config_file: str):

        self.config_file = config_file
        self.data: Dict[str, str] = {}

        self.width: int = 0
        self.height: int = 0
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.output_file: str = ""
        self.perfect: bool = False
        self.seed: Optional[int] = None

    def parse(self):

        self._read_file()
        self._parse_values()
        self._validate_coordinates()

    def _read_file(self):

        with open(self.config_file, "r") as f:

            for line in f:

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Invalid line: {line}")

                key, value = line.split("=", 1)

                self.data[key.strip().upper()] = value.strip()

    def _parse_values(self):

        self.width = int(self.data["WIDTH"])
        self.height = int(self.data["HEIGHT"])

        self.entry = self._parse_coordinates(self.data["ENTRY"])
        self.exit = self._parse_coordinates(self.data["EXIT"])

        self.output_file = self.data["OUTPUT_FILE"]

        perfect_value = self.data["PERFECT"].lower()

        if perfect_value not in ("true", "false"):
            raise ValueError("PERFECT must be True or False")

        self.perfect = perfect_value == "true"

        if "SEED" in self.data:
            self.seed = int(self.data["SEED"])

    def _parse_coordinates(self, value: str):

        x_str, y_str = value.split(",")

        return int(x_str), int(y_str)

    def _validate_coordinates(self):

        x_entry, y_entry = self.entry
        x_exit, y_exit = self.exit

        if not (0 <= x_entry < self.width and 0 <= y_entry < self.height):
            raise ValueError("Entry coordinates out of bounds")

        if not (0 <= x_exit < self.width and 0 <= y_exit < self.height):
            raise ValueError("Exit coordinates out of bounds")

        if self.entry == self.exit:
            raise ValueError("Entry and Exit cannot be the same")