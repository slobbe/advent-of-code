from collections import deque

import numpy as np
import z3
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


def least_presses_joltages(machines):
    least_presses = []
    for machine in machines:
        presses = solve_joltage(machine)
        least_presses.append(sum(presses) if presses is not None else 0)

    return least_presses


def solve_joltage(machine):
    joltages = np.array(machine["joltages"], dtype=int)
    buttons = get_matrix(machine["buttons"], len(joltages)).T
    m, n = buttons.shape

    opt = z3.Optimize()

    x = [z3.Int(f"x{j}") for j in range(n)]
    for v in x:
        opt.add(v >= 0)

    for i in range(m):
        opt.add(
            z3.Sum([(int(buttons[i, j]) * x[j]) for j in range(n)]) == int(joltages[i])
        )

    opt.minimize(z3.Sum(x))
    if opt.check() != z3.sat:
        return None

    model = opt.model()
    return np.array([model[v].as_long() for v in x], dtype=int)


def main() -> None:
    machines = get_machines(read_input(10))

    p_1 = sum(least_button_presses(machines))
    p_2 = sum(least_presses_joltages(machines))

    pretty_print([p_1, p_2], "Day 10: Factory")


if __name__ == "__main__":
    main()
