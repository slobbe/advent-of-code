from util import Input, pretty_print, read_input


def beam(manifold: Input) -> tuple[int, int]:
    tachyons: dict[int, int] = dict(
        [(manifold[0].index("S"), 1)]
    )  # { position: possible paths there }
    total_splits = 0

    for i in range(1, len(manifold)):
        eff_splitters = []
        for j, m in enumerate(manifold[i]):
            if m == "^" and j in tachyons.keys():
                eff_splitters.append(j)

        if len(eff_splitters) == 0:
            continue

        total_splits += len(eff_splitters)

        for splitter in eff_splitters:
            created_tachyons = [
                max(0, splitter - 1),
                min(len(manifold[i]), splitter + 1),
            ]
            for new_tachyon in created_tachyons:
                if new_tachyon in tachyons.keys():
                    tachyons[new_tachyon] += tachyons[splitter]
                else:
                    tachyons[new_tachyon] = tachyons[splitter]

            tachyons.pop(splitter, None)

    timelines = sum(tachyons.values())

    return total_splits, timelines


def main() -> None:
    tachyon_manifold = read_input(7)

    total_splits, timelines = beam(tachyon_manifold)

    pretty_print([total_splits, timelines], "Day 7: Laboratories")


if __name__ == "__main__":
    main()
