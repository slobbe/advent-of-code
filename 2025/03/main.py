import os


def parse_input(input_path: str) -> list[str]:
    path = os.path.join(os.path.dirname(__file__), input_path)
    content = ""
    with open(path) as f:
        content = f.read()

    content = content.strip()
    banks = content.split("\n")

    return banks

def largest_joltage(bank: str) -> int:
    digits = list(bank)
    first = max(digits[:-1])
    index_first = digits.index(first)

    second = max(digits[(index_first + 1):])

    return int(first+second)

def total_joltage(banks: list[str]) -> int:
    max_jolts = [largest_joltage(bank) for bank in banks]

    return sum(max_jolts)

def main() -> None:
    input_path = "input.txt"
    banks = parse_input(input_path)
    joltage = total_joltage(banks)

    # Pretty print answers
    print("===== Advent of Code =====")
    print("Day 3: Lobby")
    print("--------------------------")
    print("Total output joltage (Part 1):", joltage)
    print("--------------------------")


if __name__ == "__main__":
    main()
