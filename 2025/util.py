from pathlib import Path

ROOT = Path(__file__).parent
INPUT_DIR = ROOT / "inputs"

type Input = list[str]


def read_input(day: int, is_test: bool = False) -> Input:
    file_ext = ".test.txt" if is_test else ".txt"
    day_num = str(day).zfill(2)
    file_name = f"day{day_num}{file_ext}"
    path = INPUT_DIR / file_name

    return path.read_text(encoding="utf-8").rstrip("\n").splitlines()


def pretty_print(answers: list[int], topic: str) -> None:
    year = ROOT.name
    width = 31
    print(f" Advent of Code {year} ".center(width, "*"))
    print(topic.center(width, " "))
    print(width * "*")
    for i, answer in enumerate(answers):
        print(f" Part {i + 1}:", answer)

    print(width * "*")
