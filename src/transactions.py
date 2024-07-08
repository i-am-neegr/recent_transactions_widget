import pandas as pd
from typing import List, Dict


def csv_transaction(filepath: str) -> List[Dict]:
    try:
        df = pd.read_csv(filepath)
        transactions = df.to_dict(orient='records')
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        return []


def xlsx_transaction(filepath: str) -> List[Dict]:
    try:
        df = pd.read_excel(filepath)
        transactions = df.to_dict(orient='records')
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении XLSX файла: {e}")
        return []
