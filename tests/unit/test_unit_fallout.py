from scripts.fallout import claim_ownership_of_fallout
from scripts.helpers import get_account


def test_claiming_ownership():
    # Arrange
    account_to_deploy = get_account(0)
    account_to_claim = get_account(1)
    # Act
    contract_claimed = claim_ownership_of_fallout(account_to_deploy, account_to_claim)
    # Assert
    assert contract_claimed.owner() == account_to_claim
