import re
from src.transactions_filtering import filter_transactions_by_description, count_transactions_by_category
import pytest
from unittest.mock import patch, Mock

@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {
                "amount": "48223.05",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
    ]

@pytest.fixture
def sample_categories():
    return {
        "Transfer": ["перевод", "transfer"],
        "Deposit": ["вклад", "deposit"],
        "Payment": ["оплата", "payment"]
    }

def test_filter_transactions_by_description(sample_transactions):
    with patch('src.transactions_filtering.re.compile') as mock_compile:
        mock_pattern = Mock()
        mock_compile.return_value = mock_pattern
        mock_pattern.search.side_effect = lambda x: "перевод" in x.lower()

        search_string = "перевод"
        expected = [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589"
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188"
            }
        ]

        assert filter_transactions_by_description(sample_transactions, search_string) == expected
        mock_compile.assert_called_once_with(search_string, re.IGNORECASE)

def test_count_transactions_by_category(sample_transactions, sample_categories):
    with patch('src.transactions_filtering.re.search', side_effect=re.search) as mock_search:
        expected = {
            "Transfer": 2,
            "Deposit": 1,
            "Payment": 0
        }

        assert count_transactions_by_category(sample_transactions, sample_categories) == expected
        assert mock_search.call_count == 5