import json
from decimal import Decimal
from pathlib import Path
from unittest.mock import Mock, patch

from src.utils import calc_to_rubles, decimal_rub_course, json_transactions_from, transaction_sum


def test_calc_to_rubles() -> None:
    assert calc_to_rubles(5, 100) == 500


def test_decimal_rub_course() -> None:
    assert decimal_rub_course("RDRyvyFY 102,55 ₽") == Decimal("102.55")


# Тест для функции json_transactions_from
def test_json_transactions_from(tmp_path: Path) -> None:
    test_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]
    test_file = tmp_path / "test_transactions.json"
    with open(test_file, "w") as f:
        json.dump(test_data, f)

    transactions = json_transactions_from(str(test_file))
    assert len(transactions) == len(test_data)
    assert transactions[0]["operationAmount"]["amount"] == "31957.58"


# Тест для функции transaction_sum
@patch("src.utils.requests.get")
def test_transaction_sum(mock_get: Mock) -> None:
    mock_response = Mock()
    mock_response.text = "1 USD = 75.5 ₽"
    mock_get.return_value = mock_response

    test_transaction = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    expected_rub_amount = Decimal("741717.285")  # 100 USD * 75.5

    rub_amount = transaction_sum(test_transaction)
    assert rub_amount == expected_rub_amount
