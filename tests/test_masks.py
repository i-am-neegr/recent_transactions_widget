import pytest

from src.masks import bank_account_masking, bank_card_masking


@pytest.fixture
def bank_card() -> str:
    return "7000792289606361"


@pytest.fixture
def bank_account() -> str:
    return "73654108430135874305"


def test_bank_card_masking(bank_card: str) -> None:
    assert bank_card_masking(bank_card) == "7000 79** **** 6361"


def test_bank_account_masking(bank_account: str) -> None:
    assert bank_account_masking(bank_account) == "**4305"
