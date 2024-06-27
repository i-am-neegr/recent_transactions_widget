from typing import Any, Dict, Hashable, List
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.transactions import csv_transaction, xlsx_transaction


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "description": "Перевод организации",
        },
        {
            "id": "3598919",
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": "29740",
            "currency_name": "Peso",
            "currency_code": "COP",
            "description": "Перевод с карты на карту",
        },
    ]


def test_csv_transaction(transactions: List[Dict[str, Any]]) -> None:
    mock_csv_data = """id;state;date;amount;currency_name;currency_code;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Перевод организации
3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;Перевод с карты на карту"""
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result: List[Dict[str, Any]] = csv_transaction("mocked_path.csv")
        expected_result: List[Dict[str, Any]] = transactions

        assert result == expected_result


def test_xlsx_transaction(transactions: List[Dict[str, Any]]) -> None:
    mock_xlsx_data: pd.DataFrame = pd.DataFrame(
        {
            "id": ["650703", "3598919"],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
            "amount": ["16210", "29740"],
            "currency_name": ["Sol", "Peso"],
            "currency_code": ["PEN", "COP"],
            "description": ["Перевод организации", "Перевод с карты на карту"],
        }
    )
    with patch("pandas.read_excel", return_value=mock_xlsx_data):
        result: List[Dict[Hashable, Any]] = xlsx_transaction("mocked_path.xlsx")
        expected_result: List[Dict[str, Any]] = transactions
        assert result == expected_result
