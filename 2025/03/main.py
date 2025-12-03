import os
from collections.abc import Callable


def parse_input(input_path: str) -> list[str]:
    path = os.path.join(os.path.dirname(__file__), input_path)
    content = ""
    with open(path) as f:
        content = f.read()

    content = content.strip()
    banks = content.split("\n")

    return banks


def largest_joltage_1(bank: str) -> int:
    digits = list(bank)
    first = max(digits[:-1])
    index_first = digits.index(first)

    second = max(digits[(index_first + 1) :])

    return int(first + second)


def largest_joltage_2(bank: str) -> int:
    digits = list(bank)

    d = []
    k = 0
    for i in range(12):
        j = i - 11
        search_digits = digits[k:] if j == 0 else digits[k:j]
        largest_digit = max(search_digits)
        largest_digit_index = search_digits.index(largest_digit)
        k += largest_digit_index + 1
        d.append(largest_digit)

    return int("".join(d))


def total_joltage(banks: list[str], largest_joltage: Callable[[str], int]) -> int:
    max_jolts = [largest_joltage(bank) for bank in banks]

    return sum(max_jolts)


def main() -> None:
    input_path = "input.txt"
    banks = parse_input(input_path)
    joltage_1 = total_joltage(banks, largest_joltage_1)
    joltage_2 = total_joltage(banks, largest_joltage_2)

    # Pretty print answers
    print("===== Advent of Code =====")
    print("Day 3: Lobby")
    print("--------------------------")
    print("Total output joltage (Part 1):", joltage_1)
    print("Total output joltage (Part 2):", joltage_2)
    print("--------------------------")


if __name__ == "__main__":
    main()
