from util import Input, pretty_print, read_input


def get_summary(input: Input):
    i = [
        e.strip().split("\n")
        for e in "\n".join(list(map(lambda x: "\n" if x == "" else x, input))).split(
            "\n\n"
        )
    ]

    shapes = list(map(lambda s: s[1:], i[:-1]))
    regions = []
    for region in i[-1]:
        size, quantities = region.split(":")
        regions.append(
            {
                "size": tuple(map(int, size.split("x"))),
                "quantities": tuple(map(int, quantities.strip().split(" "))),
            }
        )

    return shapes, regions


def shapes_fit_region(shapes, region):
    """
    Check whether total area of the shapes fits the total area of the region.
    """
    shape_areas = [sum(list(map(lambda x: x.count("#"), shape))) for shape in shapes]
    shape_quants = region["quantities"]
    total_area_shapes = sum(
        [quant * shape_areas[i] for i, quant in enumerate(shape_quants)]
    )

    area_region = eval("*".join(list(map(str, region["size"]))))

    return total_area_shapes <= area_region


def naive_filtering_regions(regions, shapes):
    filtered_regions = list(
        filter(lambda region: shapes_fit_region(shapes, region), regions)
    )

    return filtered_regions


def main() -> None:
    title = "Day 12: Christmas Tree Farm"

    shapes, regions = get_summary(read_input(12))
    p_1 = len(naive_filtering_regions(regions, shapes))

    pretty_print([p_1], title)


if __name__ == "__main__":
    main()
