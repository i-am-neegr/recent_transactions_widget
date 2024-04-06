from src.masks import bank_card_masking as card_masks, bank_account_masking as account_masks
# импортируем две функции и во избежание проблем с импортом в будущем, присваиваем локальные имена

def object_masking(subject: str) -> str:
    """
    Needs either bank card or bank account and
    returns its masked version
    """
    numbers_sequence = ''.join([c for c in subject if c.isdigit()])
    typename = ''.join([c for c in subject if not c.isdigit()]).strip()

    if len(numbers_sequence) == 16:
        return f"{typename} {card_masks(numbers_sequence)}"
    else:
        return f"{typename} {account_masks(numbers_sequence)}"


def get_date(date_and_time: str) -> str:
    """
    Needs date with time in "2018-07-11T02:26:18.671407" format
    and returns date
    """
    date, _ = date_and_time.split("T")
    date = date.split("-")
    return f"{date[2]}.{date[1]}.{date[0]}"