import csv
from typing import Any, Dict, Hashable, List

import pandas as pd


def csv_transaction(filepath: str) -> List[Dict[str, Any]]:
    """
    Returns a list of transactions from a CSV file, where each transaction is a dictionary.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return list(reader)


def xlsx_transaction(filepath: str) -> list[dict[Hashable, Any]]:
    """
    Returns a list of transactions from an XLSX file, where each transaction is a dictionary.
    """
    df = pd.read_excel(filepath)
    return df.to_dict(orient="records")
