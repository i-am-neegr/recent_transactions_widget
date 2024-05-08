from src.decorators import log


@log("test_log.txt")
def add_two(x: int | float) -> int | float:
    return x + 2


@log("test_log.txt")
def half_of(x: int | float) -> int | float:
    return 2 / x


def test_add_two() -> None:
    with open("test_log.txt", "r", encoding="UTF-8") as file:
        amount_before = 0
        for _ in file:
            amount_before += 1
    add_two(52)
    with open("test_log.txt", "r", encoding="UTF-8") as file:
        amount_after = 0
        for _ in file:
            amount_after += 1
    assert amount_before + 1 == amount_after


def test_half_of() -> None:
    with open("test_log.txt", "r", encoding="UTF-8") as file:
        amount_before = 0
        for _ in file:
            amount_before += 1
    half_of(52)
    with open("test_log.txt", "r", encoding="UTF-8") as file:
        amount_after = 0
        for _ in file:
            amount_after += 1
    assert amount_before + 1 == amount_after
