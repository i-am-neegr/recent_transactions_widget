from datetime import datetime
from functools import wraps

def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
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