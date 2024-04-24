from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Tuple


def log(filename: None | str = None) -> Callable:
    """
    A function decorator that will log some information about the operation of your function.
    Also it has an additional arguement "filename" where you can give the path to the logging file or its name,
    but if you won't do it this information will be printed in console
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Tuple, **kwargs: Dict) -> Any:
            status = "ok"
            try:
                res = func(*args, **kwargs)
            except Exception as error:
                res = None
                status = f"error: <{type(error).__name__}>. Inputs: {args}, {kwargs}"
            finally:
                message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {func.__name__} {status}"

            if filename:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(message + "\n")
            else:
                print(message)

            return res

        return wrapper

    return decorator
