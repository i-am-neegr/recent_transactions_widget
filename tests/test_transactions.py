from typing import Any, Iterator, List, Tuple, Union
from unittest.mock import mock_open, patch

import pandas as pd

from src.transactions import csv_transaction, xlsx_transaction


def test_csv_transaction_list() -> None:
    mock_csv_data: str = "transaction_id,amount,date\n1,100,2023-01-01\n2,200,2023-01-02\n"
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):  # Удалите "as mock_file"
        result: Union[List[List[str]], Tuple[Tuple[str, ...], ...], Iterator[Any]] = csv_transaction(
            "mocked_path.csv", list
        )
        expected_result: List[List[str]] = [
            ["transaction_id", "amount", "date"],
            ["1", "100", "2023-01-01"],
            ["2", "200", "2023-01-02"],
        ]
        assert isinstance(result, list)  # Ensure result is a list
        assert result == expected_result


def test_csv_transaction_tuple() -> None:
    mock_csv_data: str = "transaction_id,amount,date\n1,100,2023-01-01\n2,200,2023-01-02\n"
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):  # Удалите "as mock_file"
        result: Union[List[List[str]], Tuple[Tuple[str, ...], ...], Iterator[Any]] = csv_transaction(
            "mocked_path.csv", list
        )
        result_as_tuple: Tuple[Tuple[str, ...], ...] = tuple(tuple(row) for row in result)  # Convert to tuple
        expected_result: Tuple[Tuple[str, ...], ...] = (
            ("transaction_id", "amount", "date"),
            ("1", "100", "2023-01-01"),
            ("2", "200", "2023-01-02"),
        )
        assert result_as_tuple == expected_result


def test_csv_transaction_reader() -> None:
    mock_csv_data: str = "transaction_id,amount,date\n1,100,2023-01-01\n2,200,2023-01-02\n"
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):  # Удалите "as mock_file"
        result: Union[List[List[str]], Tuple[Tuple[str, ...], ...], Iterator[Any]] = csv_transaction(
            "mocked_path.csv", str
        )
        assert isinstance(result, Iterator)


def test_xlsx_transaction() -> None:
    mock_xlsx_data: pd.DataFrame = pd.DataFrame(
        {"transaction_id": [1, 2], "amount": [100, 200], "date": ["2023-01-01", "2023-01-02"]}
    )
    with patch("pandas.read_excel", return_value=mock_xlsx_data):  # Удалите "as mock_read_excel"
        result: pd.DataFrame = xlsx_transaction("mocked_path.xlsx")
        pd.testing.assert_frame_equal(result, mock_xlsx_data)
