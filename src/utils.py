import json
from decimal import Decimal
from typing import Dict, List

import requests


def calc_to_rubles(any_currency_amount: Decimal | int | float, rub_amount_for_one: Decimal | int | float) -> Decimal:
    """
    Calculates your currency to rubles, by a course that you will give
    """
    return Decimal(any_currency_amount) * Decimal(rub_amount_for_one)


def decimal_rub_course(input_data: str) -> Decimal:
    """
    Function that tryes to find an ₽ sign and then returns a decimal integer of the symbols
    that are located before this sign
    """
    rub_index = input_data.find("₽")
    raw_course = input_data[rub_index - 8 : rub_index - 1]
    course_lst = [char for char in raw_course if char.isdigit() or char in ",."]
    str_course = "".join(course_lst).replace(",", ".")
    return Decimal(str_course)


def json_transactions_from(filepath: str) -> List:
    """
    Returns a list from JSON file that you will give as filepath param
    """
    json_list = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            json_list = json.load(f)
    except Exception as error:
        print(f"There is at least a {type(error).__name__}")
    finally:
        return json_list


def transaction_sum(json_transaction: Dict) -> Decimal:
    """
    Returns amount of given transaction in rubles
    """
    rub_amount = Decimal("0.0")
    currency_code = json_transaction["operationAmount"]["currency"]["code"]
    base_url = f"https://www.banki.ru/products/currency/{currency_code.lower()}/"

    if currency_code == "RUB":
        rub_amount = Decimal(json_transaction["operationAmount"]["amount"])
    elif currency_code in ("USD", "EUR"):
        response = requests.get(base_url)
        data = response.text
        foreign_currency_amount = Decimal(json_transaction["operationAmount"]["amount"])
        rub_amount = calc_to_rubles(foreign_currency_amount, decimal_rub_course(data))
    return rub_amount
