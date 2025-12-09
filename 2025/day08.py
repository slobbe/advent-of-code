from collections import deque

import numpy as np
from util import Input, pretty_print, read_input


def get_nodes(input: Input) -> np.ndarray:
    return np.array([np.array(list(map(int, node.split(",")))) for node in input])


def distances(nodes: np.ndarray) -> np.ndarray:
    diff = nodes[:, None, :] - nodes[None, :, :]

    return np.linalg.norm(diff, axis=-1)


def get_pairs(
    distances: np.ndarray, n_connections: int | None = None
) -> list[tuple[int, int]]:
    all_distances = np.unique(distances.flatten())
    sorted_distances = sorted(all_distances[all_distances > 0])

    if n_connections is None:
        n_connections = len(sorted_distances)

    pairs = deque([])
    for dist in sorted_distances[:n_connections]:
        pair = np.where(distances == dist)[0]
        pairs.appendleft((int(pair[0]), int(pair[1])))

    # pairs = [pair for _, pair in list(set(pairs))]

    return list(pairs)


def connect_circuits(jboxes, n_connections: int | None = None, terminate: bool = False):
    dists = distances(jboxes)
    all_distances = np.unique(dists.flatten())
    sorted_distances = sorted(all_distances[all_distances > 0])

    if n_connections is None:
        n_connections = len(sorted_distances)

    connection_circuits = []
    last_connection = []

    circuits = []
    for i, dist in enumerate(sorted_distances):
        pair = np.where(dists == dist)[0]
        pair = (int(pair[0]), int(pair[1]))

        if len(circuits) == 0:
            circuits.append({*pair})
            continue

        t_circuits = set()
        for circuit in circuits:
            jbox_1, jbox_2 = pair
            if jbox_1 in circuit:
                t_circuits.add(frozenset(circuit))
            if jbox_2 in circuit:
                t_circuits.add(frozenset(circuit))

        if len(t_circuits) == 0:
            circuits.append({*pair})
        else:
            for circuit in t_circuits:
                circuits.remove(circuit)

            circuits.append(set().union(*[*t_circuits, {*pair}]))

        if (n_connections is not None) and (i == n_connections - 1):
            connection_circuits = sorted(circuits, key=len)[::-1]
            if terminate:
                break

        if len(circuits) == 1 and len(circuits[0]) == len(jboxes):
            last_connection = [jboxes[pair[0]], jboxes[pair[1]]]
            break

    sizes = list(map(len, connection_circuits))

    return sizes, last_connection


def main() -> None:
    jboxes = get_nodes(read_input(8, False))
    sizes, last_connection = connect_circuits(jboxes, 1000, False)

    p_1 = eval("*".join([str(s) for s in sizes[:3]]))
    p_2 = last_connection[0][0] * last_connection[1][0]

    pretty_print([p_1, p_2], "Day 8: Playground")


if __name__ == "__main__":
    main()
