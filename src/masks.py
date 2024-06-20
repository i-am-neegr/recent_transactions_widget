from logger import setup_logger

logger = setup_logger('masks_logger', 'masks.log')

def bank_card_masking(card_number: str | int) -> str:
    """
    function that needs card number as param, and returns masked card
    """
    try:
        card_number = str(card_number)
        masked_card = ""
        for num in range(len(card_number)):
            if num < 6 or num >= 12:
                adding_el = card_number[num]
            else:
                adding_el = "*"
            if (num + 1) % 4 == 0 and (num + 1) != 16:
                adding_el += " "

            masked_card += adding_el
        logger.info('Маска успешно применена к номеру карты')
        return masked_card
    except Exception as e:
        logger.error(f'Ошибка при применении маски{e}')


def bank_account_masking(account_number: str | int) -> str:
    """
    function that needs account number as param, and returns masked account number
    """
    try:
        account_number = str(account_number)
        logger.info('Маска успешно применена к номеру счета')
        return "**" + account_number[-4:]
    except Exception as e:
        logger.error(f'Ошибка при применении маски{e}')
