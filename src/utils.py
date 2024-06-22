import json
from decimal import Decimal
from typing import Dict, List

import requests

from logger import setup_logging

logger = setup_logging()


def calc_to_rubles(any_currency_amount: Decimal | int | float, rub_amount_for_one: Decimal | int | float) -> Decimal:
    """
    Calculates your currency to rubles, by a course that you will give
    """
    result = Decimal(any_currency_amount) * Decimal(rub_amount_for_one)
    logger.debug(f"Converted {any_currency_amount} to rubles with rate {rub_amount_for_one}: {result}")
    return result


def decimal_rub_course(input_data: str) -> Decimal:
    """
    Function that tries to find a ₽ sign and then returns a decimal integer of the symbols
    that are located before this sign
    """
    rub_index = input_data.find("₽")
    if rub_index == -1:
        logger.error("₽ sign not found in input data")
        raise ValueError("₽ sign not found in input data")

    raw_course = input_data[rub_index - 8 : rub_index - 1]
    course_lst = [char for char in raw_course if char.isdigit() or char in ",."]
    str_course = "".join(course_lst).replace(",", ".")
    result = Decimal(str_course)
    logger.debug(f"Extracted decimal ruble course from input data: {result}")
    return result


def json_transactions_from(filepath: str) -> List:
    """
    Returns a list from JSON file that you will give as filepath param
    """
    json_list = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            json_list = json.load(f)
        logger.info(f"Loaded JSON data from {filepath}")
    except Exception as error:
        logger.error(f"Error loading JSON file {filepath}: {type(error).__name__} - {error}")
    finally:
        logger.info("JSON file processing completed")
        return json_list


def transaction_sum(json_transaction: Dict) -> Decimal:
    """
    Returns amount of given transaction in rubles
    """
    rub_amount = Decimal("0.0")
    currency_code = json_transaction["operationAmount"]["currency"]["code"]
    base_url = f"https://www.banki.ru/products/currency/{currency_code.lower()}/"

    try:
        if currency_code == "RUB":
            rub_amount = Decimal(json_transaction["operationAmount"]["amount"])
            logger.debug(f"Transaction amount in RUB: {rub_amount}")
        elif currency_code in ("USD", "EUR"):
            response = requests.get(base_url)
            data = response.text
            foreign_currency_amount = Decimal(json_transaction["operationAmount"]["amount"])
            rub_amount = calc_to_rubles(foreign_currency_amount, decimal_rub_course(data))
            logger.debug(
                f"Transaction amount in {currency_code}: {foreign_currency_amount}, converted to rubles: {rub_amount}"
            )
        else:
            logger.warning(f"Unsupported currency code: {currency_code}")
    except Exception as error:
        logger.error(f"Error calculating transaction sum: {type(error).__name__} - {error}")

    logger.info("Calculations finished")
    return rub_amount
