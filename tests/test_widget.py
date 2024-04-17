import pytest

from src.widget import object_masking, get_date


@pytest.fixture
def date():
    return "2018-07-11T02:26:18.671407"


@pytest.mark.parametrize("object_to_mask, expected", [
    ("Visa Platinum 7000 7922 8960 6361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
])
def test_object_masking(object_to_mask, expected):
    assert object_masking(object_to_mask) == expected


def test_get_date(date):
    assert get_date(date) == "11.07.2018"
