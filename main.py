import sys
import dateutil.parser
from src.utils import json_transactions_from, transaction_sum
from src.processing import sorted_by_date, sorted_by_state
from src.generators import filter_by_currency
from src.transactions import csv_transaction, xlsx_transaction
from src.transactions_filtering import filter_transactions_by_description
from src.masks import bank_card_masking, bank_account_masking


def main() -> None:
    types = {1: 'json', 2: 'csv', 3: 'xlsx'}
    filtering_statuses = ('EXECUTED', 'CANCELED', 'PENDING')

    print(f'''Привет! Добро пожаловать в программу работы с банковскими транзакициями. 
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из {types[1]} файла
2. Получить информацию о транзакциях из {types[2]} файла
3. Получить информацию о транзакциях из {types[3]} файла\n''')

    filetype = int(input())

    match filetype:
        case 1:
            filepath = "data/operations.json"
            transactions = json_transactions_from(filepath)
            print(f'Для обработки выбран {types[filetype]} файл.\n')
        case 2:
            filepath = "data/transactions.csv"
            transactions = csv_transaction(filepath)
            print(f'Для обработки выбран {types[filetype]} файл.\n')
        case 3:
            filepath = "data/transactions_excel.xlsx"
            transactions = xlsx_transaction(filepath)
            print(f'Для обработки выбран {types[filetype]} файл.\n')
        case _:
            print("Неверный выбор.")
            sys.exit(1)

    while True:
        print('''Введите статус по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n''')

        status = input().upper()
        if status not in filtering_statuses:
            print(f'Статус операции "{status}" недоступен.\n')
        else:
            filtered_transactions = sorted_by_state(transactions, status)
            print(f'Операции отфильтрованы по статусу {status}')
            break

    sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_choice == 'да':
        filtered_transactions = sorted_by_date(filtered_transactions, descending=False)

    direction = bool(int(input("Отсортировать по возрастанию или по убыванию?(1, если да, иначе 0): ")))
    if direction:
        filtered_transactions = sorted(filtered_transactions, key=lambda x: transaction_sum(x))

    rub_only_choice = input("Выводить только рублевые тразакции? Да/Нет: ").strip().lower()
    if rub_only_choice == 'да':
        filtered_transactions = filter_by_currency(filtered_transactions, 'RUB')

    search_choice = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    if search_choice == 'да':
        search_str = input("Введите слово для поиска в описании: ").strip()
        filtered_transactions = filter_transactions_by_description(filtered_transactions, search_str)

    print("Распечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(list(filtered_transactions))}")
        for transaction in list(filtered_transactions):
            date = dateutil.parser.isoparse(transaction['date']).strftime('%d.%m.%Y')
            description = transaction['description']
            match filetype:
                case 1:
                    amount = transaction['operationAmount']['amount']
                    currency = transaction['operationAmount']['currency']['name']
                case 2:
                    amount = transaction['amount']
                    currency = transaction['currency_name']
                case 3:
                    amount = transaction['amount']
                    currency = transaction['currency_name']
            if 'from' in transaction and 'to' in transaction:
                from_account = bank_card_masking(transaction['from']) if 'карта' in transaction.get('from', '').lower() else bank_account_masking(transaction['from'])
                to_account = bank_card_masking(transaction['to']) if 'карта' in transaction['to'].lower() else bank_account_masking(transaction['to'])
                print(f"{date} {description}\n{from_account} -> {to_account}\nСумма: {amount} {currency}\n")
            else:
                account = bank_account_masking(transaction['to'])
                print(f"{date} {description}\nСчет {account}\nСумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
