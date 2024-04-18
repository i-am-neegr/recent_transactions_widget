from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


# first test of "filter_by_currency" if it returns correct number of transactions
def test_filter_by_currency_returns_correct_number_of_transactions(transactions: List[Dict[str, Any]]) -> None:
    assert len(list(filter_by_currency(transactions, "USD"))) == 3


# second test of "filter_by_currency" if if returns correct ids
def test_filter_by_currency_returns_correct_correct_ids(transactions: List[Dict[str, Any]]) -> None:
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert [transaction["id"] for transaction in usd_transactions] == [939719570, 142264268, 895315941]


# third test of "filter_by_currency" if it works with empty list without errors
def test_filter_by_currency_empty_list() -> None:
    assert len(list(filter_by_currency([], "USD"))) == 0


# forth test of "filter_by_currency" if it works with missing currency without errors
def test_filter_by_not_founded_currency(transactions: List[Dict[str, Any]]) -> None:
    assert len(list(filter_by_currency(transactions, "EUR"))) == 0


# first test of "transaction_descriptions" if it returns correct number of descriptions
def test_transaction_descriptions_returns_correct_number_of_descriptions(transactions: List[Dict[str, Any]]) -> None:
    assert len(list(transaction_descriptions(transactions))) == len(transactions)


# second test of "transaction_descriptions" if it works with empty list without errors
def test_transaction_descriptions_empty_list() -> None:
    assert len(list(transaction_descriptions([]))) == 0


def test_card_number_generator_0_to_5() -> None:
    assert list(card_number_generator(0, 5)) == [
        "0000 0000 0000 0000",
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


def test_card_number_generator_with_big_numbers() -> None:
    assert list(card_number_generator(1299999999999999, 1300000000000004)) == [
        "1299 9999 9999 9999",
        "1300 0000 0000 0000",
        "1300 0000 0000 0001",
        "1300 0000 0000 0002",
        "1300 0000 0000 0003",
        "1300 0000 0000 0004",
    ]
