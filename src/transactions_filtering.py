import re
from typing import List, Dict, Any


def filter_transactions_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по строке поиска в описании.

    :param transactions: список словарей с операциями, каждый словарь имеет ключ 'description'
    :param search_string: строка поиска
    :return: отфильтрованный список операций
    """
    pattern = re.compile(search_string, re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction['description'])]


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: Dict[str, List[str]]) -> Dict[
    str, int]:
    """
    Подсчитывает количество операций в каждой категории.

    :param transactions: список словарей с операциями, каждый словарь имеет ключ 'description'
    :param categories: словарь категорий, где ключи - категории, а значения - списки строк для поиска
    :return: словарь с количеством операций в каждой категории
    """
    category_counts = {category: 0 for category in categories}

    for transaction in transactions:
        description = transaction['description']
        for category, keywords in categories.items():
            if any(re.search(keyword, description, re.IGNORECASE) for keyword in keywords):
                category_counts[category] += 1
                break

    return category_counts
