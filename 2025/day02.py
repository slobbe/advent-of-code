import os
from collections.abc import Callable


def parse_input(input_path: str) -> list[tuple[int, int]]:
    path = os.path.join(os.path.dirname(__file__), input_path)
    content = ""
    with open(path) as f:
        content = f.read()

    content = content.strip()
    ranges = [
        (int(start), int(end))
        for part in content.split(",")
        for start, end in [part.split("-", 1)]
    ]

    return ranges


def invalid_ids_1(range_boundaries: tuple[int, int]) -> list[int]:
    (first, last) = range_boundaries

    invalid_ids = []
    for id in range(first, last + 1):
        id = str(id)
        if len(id) % 2 != 0:
            continue  # invalid IDs must have even number of digits

        sub_id = id[: (len(id) // 2)]
        if id == (sub_id + sub_id):
            invalid_ids.append(int(id))

    return invalid_ids


def invalid_ids_2(range_boundaries: tuple[int, int]) -> list[int]:
    (first, last) = range_boundaries

    invalid_ids = []
    for id in range(first, last + 1):
        id = str(id)

        for sub_id_len in range(1, (len(id) // 2) + 1):
            sub_id = id[:sub_id_len]
            multiplier = len(id) // sub_id_len
            if id == multiplier * sub_id:
                invalid_ids.append(int(id))

    invalid_ids = list(set(invalid_ids))  # remove duplicate IDs
    return invalid_ids


def sum_invalid_ids(
    ranges: list[tuple[int, int]],
    invalid_id_rule: Callable[[tuple[int, int]], list[int]],
) -> int:
    total_invalid_ids = []
    for range_boundaries in ranges:
        ids = invalid_id_rule(range_boundaries)
        for id in ids:
            total_invalid_ids.append(id)

    return sum(total_invalid_ids)


def main() -> None:
    input_path = "inputs/day02.txt"
    ranges = parse_input(input_path)

    sum_rule_1 = sum_invalid_ids(ranges, invalid_ids_1)
    sum_rule_2 = sum_invalid_ids(ranges, invalid_ids_2)

    # Pretty print answers
    print("===== Advent of Code =====")
    print("Day 2: Gift Shop")
    print("--------------------------")
    print("Invalid IDs sum (Part 1):", sum_rule_1)
    print("Invalid IDs sum (Part 2):", sum_rule_2)
    print("--------------------------")


if __name__ == "__main__":
    main()
