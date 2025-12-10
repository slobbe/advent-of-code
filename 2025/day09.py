import numpy as np
from util import Input, pretty_print, read_input


def get_red_tiles(input: Input) -> list[tuple[int, int]]:
    red_tiles: list[tuple[int, int]] = [
        (x, y) for tile in input for x, y in [tuple(map(int, tile.split(",")))]
    ]

    return red_tiles


def get_area(points):
    points = np.array(points)
    xs = points[:, 0]
    ys = points[:, 1]

    dx = np.abs(xs[:, None] - xs[None, :])
    dy = np.abs(ys[:, None] - ys[None, :])

    return (dx + 1) * (dy + 1)


def point_in_boundary(point, boundary):
    x, y = point
    n = len(boundary)

    x_crossings = y_crossings = 0

    for i in range(n):
        x1, y1 = boundary[i]
        x2, y2 = boundary[(i + 1) % n]

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        # point on boundary -> considered as inside
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True

        if y1 == y2:
            if x1 <= x < x2 and y1 > y:
                y_crossings += 1
        else:
            if y1 <= y < y2 and x1 > x:
                x_crossings += 1

    return False if x_crossings % 2 + y_crossings % 2 == 0 else True


def edge_crossings(corners, boundary):
    def edges_intersect(a1, a2, b1, b2) -> bool:
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        def on_segment(o, a, b):
            return min(o[0], a[0]) <= b[0] <= max(o[0], a[0]) and min(o[1], a[1]) <= b[
                1
            ] <= max(o[1], a[1])

        c1 = cross(a1, a2, b1)
        c2 = cross(a1, a2, b2)
        c3 = cross(b1, b2, a1)
        c4 = cross(b1, b2, a2)

        if (c1 * c2 < 0) and (c3 * c4 < 0):
            return True

        if c1 == 0 and on_segment(a1, a2, b1):
            return True
        if c2 == 0 and on_segment(a1, a2, b2):
            return True
        if c3 == 0 and on_segment(b1, b2, a1):
            return True
        if c4 == 0 and on_segment(b1, b2, a2):
            return True

        return False

    n = len(boundary)

    for i in range(n):
        x1, y1 = boundary[i]
        x2, y2 = boundary[(i + 1) % n]

        n_corners = len(corners)
        for j in range(n_corners):
            c1 = corners[j]
            c2 = corners[(j + 1) % n_corners]
            if edges_intersect(c1, c2, (x1, y1), (x2, y2)):
                return True

    return False


def rect_in_boundary(p1, p2, boundary):
    def corners(a, b):
        ax, ay = a
        bx, by = b

        x_min, x_max = min(ax, bx) + 0.5, max(ax, bx) - 0.5
        y_min, y_max = min(ay, by) + 0.5, max(ay, by) - 0.5

        c0 = (x_min, y_min)
        c1 = (x_min, y_max)
        c2 = (x_max, y_min)
        c3 = (x_max, y_max)

        return [c0, c1, c2, c3]

    rect_corners = corners(p1, p2)

    for corner in rect_corners[1::2]:
        if not point_in_boundary(corner, boundary):
            return False

    if edge_crossings(rect_corners, boundary):
        return False

    return True


def largest_area_within(area, boundary):
    areas = sorted(np.unique(area.flatten()))[::-1]

    for a in areas:
        area_fully_enclosed = False
        for i, j in np.transpose(np.array(np.where(area == a))):
            pi, pj = boundary[i], boundary[j]
            if rect_in_boundary(pi, pj, boundary):
                area_fully_enclosed = True
                break

        if area_fully_enclosed:
            return a

    return 0


def main() -> None:
    red_tiles = get_red_tiles(read_input(9))
    area = get_area(red_tiles)

    p_1 = np.max(area)
    p_2 = largest_area_within(area, red_tiles)

    pretty_print([p_1, p_2], "Day 9: Movie Theater")


if __name__ == "__main__":
    main()
