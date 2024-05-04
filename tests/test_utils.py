import pytest

from decimal import Decimal

from src.utils import calc_to_rubles, decimal_rub_course, json_transactions_from, transaction_sum

import json

from unittest.mock import patch

def test_calc_to_rubles():
    assert calc_to_rubles(5, 100) == 500


def test_decimal_rub_course():
    assert decimal_rub_course("RDRyvyFY 102,55 ₽") == Decimal('102.55')


@pytest.fixture
def sample_json_file(tmp_path):
    data = [
        {"operationAmount": {"amount": 100, "currency": {"code": "RUB"}}},
        {"operationAmount": {"amount": 50, "currency": {"code": "USD"}}}
    ]
    file_path = tmp_path / "sample.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return file_path


def test_json_transactions_from(sample_json_file):
    json_list = json_transactions_from(sample_json_file)
    assert len(json_list) == 2
    assert isinstance(json_list, list)


@patch('my_module.requests.get')
def test_transaction_sum(mock_get):
    json_transaction_usd = {"operationAmount": {"amount": 50, "currency": {"code": "USD"}}}
    mock_get.return_value.text = "<html>USD to RUB: 75</html>"

    assert transaction_sum(json_transaction_usd) == 3750