def bank_card_masking(card_number: str | int) -> str:
    """
    function that needs card number as param, and returns masked card
    """
    card_number = str(card_number)
    masked_card = ""
    for num in range(len(card_number)):
        if num < 6 or num >= 12:
            adding_el = card_number[num]
        else:
            adding_el = "*"
        if (num + 1) % 4 == 0:
            adding_el += " "

        masked_card += adding_el

    return masked_card


def bank_account_masking(account_number: str | int) -> str:
    """
    function that needs account number as param, and returns masked account number
    """
    account_number = str(account_number)

    return "**" + account_number[-4:]
