import csv
from typing import Any, Callable, Iterator, List, Tuple, Union

import pandas as pd


def csv_transaction(
    filepath: str, data_type: Callable = list
) -> Union[List[List[str]], Tuple[Tuple[str, ...], ...], Iterator[Any], Any]:
    """
    Returns your transaction list from csv file, but there is additional arguement "datatype"
    where you can write what type of collection do you want to get your transactions in.
    Only list and tuple are accepted, but you can get csv.reader object if you will place str as datatype
    """
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        if data_type == str:
            return iter(reader)
        else:
            return data_type(reader)


def xlsx_transaction(filepath: str) -> pd.DataFrame:
    """
    Returns your transaction as pandas dataframe
    """
    df = pd.read_excel(filepath)
    return df
