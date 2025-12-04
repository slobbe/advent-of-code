from util import Input, pretty_print, read_input

type Map = list[list[int]]


def get_map(input: Input) -> Map:
    return [list(map(lambda loc: 1 if loc == "@" else 0, list(r))) for r in input]


def get_vicinity(map: Map, loc: tuple[int, int]) -> Map:
    i, j = loc
    dim_i, dim_j = len(map), len(map[0])

    return [
        row[max(0, j - 1) : min(dim_j, j + 2)]
        for row in map[max(0, i - 1) : min(dim_i, i + 2)]
    ]


def mark_accessible_rolls(map: Map) -> tuple[int, Map]:
    max_rolls_in_vicinity = 4
    marked_map = []
    accessible = 0
    for i in range(len(map)):
        row_i = []
        for j in range(len(map[0])):
            if map[i][j] == 0:
                row_i.append(0)
                continue
            vicinity = get_vicinity(map, (i, j))
            vicinity = [k for row in vicinity for k in row]
            row_i.append(1 if sum(vicinity) <= max_rolls_in_vicinity else 0)

        marked_map.append(row_i)
        accessible += sum(row_i)

    return accessible, marked_map


def remove_rolls(map: Map) -> tuple[Map, int]:
    removed, marked = mark_accessible_rolls(map)
    updated_map = []
    for i in range(len(map)):
        updated_row = []
        for j in range(len(map[i])):
            updated_row.append(map[i][j] - marked[i][j])

        updated_map.append(updated_row)

    return updated_map, removed


def remove_all_rolls(map: Map, total_removed_rolls: int = 0) -> int:
    updated_map, removed_rolls = remove_rolls(map)
    total_removed_rolls += removed_rolls

    if removed_rolls == 0:
        return total_removed_rolls

    return remove_all_rolls(updated_map, total_removed_rolls)


def main() -> None:
    map = get_map(read_input(4))
    accessible_rolls_1, _ = mark_accessible_rolls(map)
    total_removed_rolls = remove_all_rolls(map)

    pretty_print(
        [accessible_rolls_1, total_removed_rolls], "Day 4: Printing Department"
    )


if __name__ == "__main__":
    main()
