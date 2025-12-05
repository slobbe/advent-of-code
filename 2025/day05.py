from util import Input, pretty_print, read_input

type Range = tuple[int, int]
type Ranges = list[Range]
type Data = tuple[Ranges, list[int]]


def parse_database(database: Input) -> Data:
    divider_idx = database.index("")

    ranges = [
        (int(start), int(end))
        for range in database[:divider_idx]
        for start, end in [range.split("-", 1)]
    ]

    available = list(map(int, database[divider_idx + 1 :]))

    return ranges, available


def in_range(range: Range, id: int) -> bool:
    start, end = range
    return start <= id <= end


def is_fresh(fresh_ranges: Ranges, id: int) -> bool:
    for range in fresh_ranges:
        if in_range(range, id):
            return True

    return False


def count_fresh_ingredients(fresh_ranges: Ranges, available: list[int]) -> int:
    fresh_available = list(map(lambda id: is_fresh(fresh_ranges, id), available))

    return sum(fresh_available)


def remove_overlaps(ranges: Ranges):
    ranges = sorted(ranges)
    new = []
    k = -1
    for i, rng in enumerate(ranges):
        if i <= k:
            continue

        start, end = rng
        largest_end = end

        for j, rrng in enumerate(ranges[i:]):
            rr_start, rr_end = rrng

            if rr_start <= largest_end:
                if rr_end > largest_end:
                    largest_end = rr_end
                k = i + j

        new.append((start, largest_end))

    return new


def total_ids(fresh_ranges: Ranges) -> int:
    all_possible = 0

    disjoint_ranges = remove_overlaps(fresh_ranges)

    for r in disjoint_ranges:
        s, e = r
        all_possible += e - s + 1

    return all_possible


def main() -> None:
    database = read_input(5)
    fresh_ranges, available = parse_database(database)

    available_fresh_ingredients = count_fresh_ingredients(fresh_ranges, available)

    total_possible_fresh_ingredients = total_ids(fresh_ranges)

    pretty_print(
        [available_fresh_ingredients, total_possible_fresh_ingredients],
        "Day 5: Cafeteria",
    )


if __name__ == "__main__":
    main()
