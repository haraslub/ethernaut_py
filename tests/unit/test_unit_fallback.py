from scripts.fallback import deploy_fallback, claim_ownership_of_fallback, withdraw_fallback_contract
from scripts.helpers import get_account


def test_claiming_ownership():
    # Arrange
    account_to_deploy = get_account(0)
    account_to_break = get_account(1)
    fallback_contract = deploy_fallback(account_to_deploy)
    # Act
    claim_ownership_of_fallback(fallback_contract, account_to_break)
    # Assert
    assert account_to_deploy != account_to_break
    assert fallback_contract.owner() == account_to_break


def test_withdraw_fallback():
    # Arrange
    account_to_deploy = get_account(0)
    fallback_contract = deploy_fallback(account_to_deploy)
    # Act
    withdraw_fallback_contract(fallback_contract, account_to_deploy)
    # Assert
    assert fallback_contract.balance() == 0