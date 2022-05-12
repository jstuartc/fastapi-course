from app.calculations import add, BankAccount, InsufficientFund
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),(7,8,15),(-50,-30,-80)
])
def test_add(num1,num2,expected):   # Naming of functions matter
    assert add(num1,num2) == expected


def test_initialising_bank(bank_account):
    assert bank_account.balance == 50

def test_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0 

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55


@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (200,100,100),(1000,333,667),(50,20,30)
])
def test_bank_transaction(zero_bank_account,deposited,withdrawn,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFund):  # Expecting an exception fails if no Exception
        zero_bank_account.withdraw(200)