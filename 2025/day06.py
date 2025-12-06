import math
import re

from util import Input, pretty_print, read_input

type MathProblem = tuple[str, list[int]]


def get_math_problems_1(input: Input) -> list[MathProblem]:
    def clean(row):
        return re.sub(r"\s+", " ", row.strip())

    def transpose(matrix):
        return list(map(list, zip(*matrix)))

    operators = clean(input[-1]).split(" ")
    numbers = transpose([list(map(int, clean(r).split(" "))) for r in input[:-1]])

    return list(zip(operators, numbers))


def get_math_problems_2(input: Input) -> list[MathProblem]:
    operators = input[-1][::-1]
    numbers = input[:-1]

    problems = []

    temp_nums = []
    for i in range(len(operators)):
        op = operators[i]
        num = "".join([num_r[::-1][i] for num_r in numbers])

        if not num.strip():
            continue

        temp_nums.append(int(num))
        if op != " ":
            problems.append((op, temp_nums))
            temp_nums = []

    return problems


def solve_math_problems(problems: list[MathProblem]) -> list[int]:
    results = []
    for op, nums in problems:
        result = math.prod(nums) if op == "*" else sum(nums)
        results.append(result)

    return results


def grand_total(problems: list[MathProblem]) -> int:
    results = solve_math_problems(problems)

    return sum(results)


def main() -> None:
    input = read_input(6)

    problems_1 = get_math_problems_1(input)
    problems_2 = get_math_problems_2(input)

    total_1 = grand_total(problems_1)
    total_2 = grand_total(problems_2)

    pretty_print([total_1, total_2], "Day 6: Trash Compactor")


if __name__ == "__main__":
    main()
