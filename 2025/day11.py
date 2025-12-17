from util import Input, pretty_print, read_input


def get_device_list(input: Input):
    devices = {}

    for device in input:
        name, connections = device.split(":")
        connections = connections.strip().split(" ")
        devices[name] = connections

    return devices


def count_paths(devices, start, end, memo):
    if start in memo.keys():
        return memo[start]

    if start == end:
        return 1
    elif start == "out":
        return 0

    n = 0
    for device in devices[start]:
        n += count_paths(devices, device, end, memo)

    memo[start] = n
    return n


def main() -> None:
    title = "Day 11: Reactor"

    devices = get_device_list(read_input(11, False))

    p_1 = count_paths(devices, "you", "out", {})
    p_2 = count_paths(devices, "svr", "dac", {}) * count_paths(
        devices, "dac", "fft", {}
    ) * count_paths(devices, "fft", "out", {}) + count_paths(
        devices, "svr", "fft", {}
    ) * count_paths(devices, "fft", "dac", {}) * count_paths(devices, "dac", "out", {})

    pretty_print([p_1, p_2], title)


if __name__ == "__main__":
    main()
