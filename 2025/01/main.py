import os


def parse_input(input_path: str):
    path = os.path.join(os.path.dirname(__file__), input_path)
    content = ""
    with open(path) as doc:
        content = doc.read()

    return content.strip().split("\n")


def parse_rotations(rotation_instructions):
    rotations = map(lambda r: (r[0], int(r[1:])), rotation_instructions)

    return list(rotations)


def execute_rotations(starting_position: int, rotations):
    dial_max: int = 99

    if starting_position > dial_max:
        return []

    positions = [(starting_position, 0)]
    for rotation in rotations:
        current_position = positions[-1][0]
        direction = rotation[0]
        distance = rotation[1]
        if direction == "L":
            naive_end_position = current_position - distance
            end_position = naive_end_position % (dial_max + 1)

            full_rotations = distance // (dial_max + 1)
            if (end_position > current_position) and (
                end_position != 0 and current_position != 0
            ):
                full_rotations += 1

            positions.append((end_position, full_rotations))
        elif direction == "R":
            naive_end_position = current_position + distance
            end_position = naive_end_position % (dial_max + 1)

            full_rotations = distance // (dial_max + 1)
            if (end_position < current_position) and (
                end_position != 0 and current_position != 0
            ):
                full_rotations += 1

            positions.append((end_position, full_rotations))
        else:
            return []

    return positions


def get_code(positions):
    end_positions = list(map(lambda p: p[0], positions))
    full_rotations = list(map(lambda p: p[1], positions))

    code_1 = end_positions.count(0)
    code_2 = end_positions.count(0) + sum(full_rotations)
    return code_1, code_2


def main():
    input_path: str = "input.txt"
    dial_starting_positions: int = 50

    content = parse_input(input_path)
    rotations = parse_rotations(content)
    positions = execute_rotations(dial_starting_positions, rotations)

    code_1, code_2 = get_code(positions)

    # Pretty print answers
    print("===== Advent of Code =====")
    print("Day 1: Secret Entrance")
    print("--------------------------")
    print("Password (Part 1):", code_1)
    print("Password (Part 2):", code_2)
    print("--------------------------")


if __name__ == "__main__":
    main()
