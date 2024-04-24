from src.decorators import log


@log("test_log.txt")
def add_two(x: int | float) -> int | float:
    return x + 2


@log("test_log.txt")
def half_of(x: int | float) -> int | float:
    return 2 / x


def test_add_two():
    add_two(52)
    with open("test_log.txt", "r", encoding="UTF-8") as file:
        logged_message = file.readline().strip()
    assert logged_message == "2024-04-24 12:56:47 add_two ok"


def test_half_of():
    half_of(0)
    with open("test_log.txt", "r", encoding="UTF-8") as file:
        file.readline()
        logged_message = file.readline().strip()
    assert logged_message == "2024-04-24 16:53:18 half_of error: <ZeroDivisionError>. Inputs: (0,), {}"