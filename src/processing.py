def sorted_by_state(original_list: list[dict], state: str = 'EXECUTED') -> list[dict]:
    '''
    gets your list with dictionaries and optional parameter "state" and
    returns its sorted version by the value of "state"in your dictionaries.
    The default function will return your list with only EXECUTED dictionaries.
    '''
    return [info_dict for info_dict in original_list if info_dict.get("state") == state]


def sorted_by_date(original_list: list[dict], descending: bool = True) -> list[dict]:
    '''
    gets your list with dictionaries and optional parameter "descending" and
    returns its sorted version by the value of "date"in your dictionaries.
    The default function will return your list with only date-sorted dictionaries.
    '''
    if descending:
        return sorted(original_list, key=lambda x: x["date"], reverse=True)
    return sorted(original_list, key=lambda x: x["date"])
