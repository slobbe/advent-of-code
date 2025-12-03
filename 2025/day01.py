from util import pretty_print, read_input


def parse_input(input: list[str]) -> list[int]:
    rotations = [int(r.replace("L", "-").replace("R", "")) for r in input]
    return rotations


def execute_rotations(
    rotations: list[int], starting_position: int, dial_size: int = 99
) -> list[tuple[int, int]]:
    if starting_position > dial_size:
        return []

    positions = [(starting_position, 0)]
    for rotation in rotations:
        current_position = positions[-1][0]
        end_position = (current_position + rotation) % (dial_size + 1)
        zero_crossings_count = abs(rotation) // (dial_size + 1)

        def sign(x):
            return (x > 0) - (x < 0)

        effective_displacement = sign(rotation) * (abs(rotation) % (dial_size + 1))
        naive_effective_end_position = current_position + effective_displacement
        is_in_dial_range = (
            naive_effective_end_position >= 0
            and naive_effective_end_position <= (dial_size + 1)
        )
        if (
            not is_in_dial_range
            and effective_displacement != naive_effective_end_position
        ):
            zero_crossings_count += 1

        positions.append((end_position, zero_crossings_count))

    return positions


def get_passwords(positions: list[tuple[int, int]]) -> tuple[int, int]:
    end_positions = list(map(lambda p: p[0], positions))
    zero_crossings_count = list(map(lambda p: p[1], positions))

    password_1 = end_positions.count(0)
    password_2 = password_1 + sum(zero_crossings_count)
    return password_1, password_2


def main() -> None:
    dial_starting_positions: int = 50

    rotations = parse_input(read_input(1))
    positions = execute_rotations(rotations, dial_starting_positions)

    password_1, password_2 = get_passwords(positions)

    pretty_print([password_1, password_2], "Day 1: Secret Entrance")


if __name__ == "__main__":
    main()
