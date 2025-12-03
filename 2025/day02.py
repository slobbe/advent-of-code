from collections.abc import Callable

from util import pretty_print, read_input


def parse_input(input: str) -> list[tuple[int, int]]:
    input = input.strip()
    ranges = [
        (int(start), int(end))
        for part in input.split(",")
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
    ranges = parse_input(read_input(2)[0])

    sum_1 = sum_invalid_ids(ranges, invalid_ids_1)
    sum_2 = sum_invalid_ids(ranges, invalid_ids_2)

    pretty_print([sum_1, sum_2], "Day 2: Gift Shop")


if __name__ == "__main__":
    main()
