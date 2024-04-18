from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Filters transactions by currency and returns all transactions filtered by currency.
    """
    return filter(lambda x: x["operationAmount"]["currency"]["code"] == currency, transactions)


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Returns all transaction descriptions.
    """
    return (transaction["description"] for transaction in transactions)


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Returns card number generators at given intervals.
    """
    for number in range(start, end + 1):
        yield (
            f"{number:016d}"[:4]
            + " "
            + f"{number:016d}"[4:8]
            + " "
            + f"{number:016d}"[8:12]
            + " "
            + f"{number:016d}"[12:]
        )
