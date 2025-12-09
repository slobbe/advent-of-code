import numpy as np
from util import Input, pretty_print, read_input


def get_nodes(input: Input) -> np.ndarray:
    return np.array([np.array(list(map(int, node.split(",")))) for node in input])


def distances(nodes: np.ndarray) -> np.ndarray:
    diff = nodes[:, None, :] - nodes[None, :, :]

    return np.linalg.norm(diff, axis=-1)


def get_pairs(
    distances: np.ndarray, n_connections: int = 1000
) -> list[tuple[int, int]]:
    pairs = []
    all_distances = np.unique(distances.flatten())
    sorted_distances = sorted(all_distances[all_distances > 0])
    for dist in sorted_distances[:n_connections]:
        pair = np.where(distances == dist)[0]
        pairs.append((float(dist), (int(pair[0]), int(pair[1]))))

    pairs = [pair for _, pair in sorted(list(set(pairs)))]

    return pairs


def connect_circuits(pairs):
    circuits = []
    for pair in pairs:
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

    circuits = sorted(circuits, key=len)[::-1]
    sizes = list(map(len, circuits))
    return circuits, sizes


def main() -> None:
    nodes = get_nodes(read_input(8, False))
    dist = distances(nodes)
    pairs = get_pairs(dist)
    circuits, sizes = connect_circuits(pairs)

    p_1 = eval("*".join([str(s) for s in sizes[:3]]))

    pretty_print([p_1], "Day 8: Playground")


if __name__ == "__main__":
    main()
