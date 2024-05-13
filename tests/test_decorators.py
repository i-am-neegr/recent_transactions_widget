import os
from src.decorators import log


@log(os.path.join("test_log.txt"))
def add_two(x: int | float) -> int | float:
    return x + 2


@log(os.path.join("test_log.txt"))
def half_of(x: int | float) -> int | float:
    raise ZeroDivisionError


def test_add_two() -> None:
    log_file_path = os.path.join("test_log.txt")
    with open(log_file_path, "r", encoding="UTF-8") as file:
        amount_before = sum(1 for _ in file)
    add_two(52)
    with open(log_file_path, "r", encoding="UTF-8") as file:
        amount_after = sum(1 for _ in file)
    assert amount_before + 1 == amount_after


def test_half_of() -> None:
    log_file_path = os.path.join("test_log.txt")
    with open(log_file_path, "r", encoding="UTF-8") as file:
        amount_before = sum(1 for _ in file)
    try:
        half_of(52)
    except ZeroDivisionError:
        pass
    with open(log_file_path, "r", encoding="UTF-8") as file:
        amount_after = sum(1 for _ in file)
    assert amount_before + 1 == amount_after
