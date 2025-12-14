from collections import deque
from itertools import combinations, permutations, product

import numpy as np
from util import Input, pretty_print, read_input


def get_machines(input: Input):
    machines = []
    for line in input:
        elements = line.split(" ")
        components = {"indicator_lights": (), "buttons": [], "joltages": ()}
        for element in elements:
            if element[0] == "[" and element[-1] == "]":
                components["indicator_lights"] = tuple(
                    [1 if light == "#" else 0 for light in list(element[1:-1])]
                )
            elif element[0] == "(" and element[-1] == ")":
                components["buttons"].append(tuple(map(int, element[1:-1].split(","))))
            elif element[0] == "{" and element[-1] == "}":
                components["joltages"] = tuple(map(int, element[1:-1].split(",")))

        machines.append(components)

    return machines


def get_matrix(buttons, size):
    matrix = []
    for button in buttons:
        vec = np.zeros(size)
        for i in button:
            vec[i] = 1
        matrix.append(vec)

    return np.array(matrix, dtype=int)


def least_button_presses(machines):
    least_presses = []
    for machine in machines:
        least_presses.append(press_buttons(machine))

    return least_presses


def press_buttons(machine):
    def state_key(state):
        return "".join(map(str, list(state)))

    final_state = np.array(machine["indicator_lights"], dtype=int)
    initial_state = np.zeros(len(final_state), dtype=int)
    buttons = get_matrix(machine["buttons"], len(final_state))

    seen, queue = {state_key(initial_state)}, deque([(initial_state, 0)])

    final_state_k = state_key(final_state)
    initial_state_k = state_key(initial_state)
    if initial_state_k == final_state_k:
        return 0

    while queue:
        state, depth = queue.popleft()

        for button in buttons:
            new_state = (state + button) % 2
            k = state_key(new_state)

            if k in seen:
                continue
            if k == final_state_k:
                return depth + 1

            queue.append((new_state, depth + 1))
            seen.add(k)

    return None


def main() -> None:
    machines = get_machines(read_input(10, False))

    p_1 = sum(least_button_presses(machines))

    pretty_print([p_1], "Day 10: Factory")


if __name__ == "__main__":
    main()
