import sys


def write_maze_file(generator, entry, exit_, solution, filepath):

    lines = []

    lines.append(generator.to_hex().strip())

    lines.append(f"{entry[0]},{entry[1]}")

    lines.append(f"{exit_[0]},{exit_[1]}")

    lines.append("".join(solution))

    try:

        with open(filepath, "w") as f:

            f.write("\n".join(lines) + "\n")

        print(f"[INFO] Maze written to '{filepath}'")

    except OSError as e:

        print(f"[ERROR] Cannot write file: {e}")

        sys.exit(1)


def verify_maze_file(filepath, width, height):

    try:

        with open(filepath, "r") as f:

            lines = f.read().splitlines()

    except OSError as e:

        print(f"[VERIFY] FAIL: {e}")

        return False

    if len(lines) != height + 3:

        print("[VERIFY] FAIL: wrong number of lines")

        return False

    for y in range(height):

        row = lines[y]

        if len(row) != width:

            print(f"[VERIFY] FAIL: row {y} wrong width")

            return False

    print("[VERIFY] OK: maze file valid")

    return True