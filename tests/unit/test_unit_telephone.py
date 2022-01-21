from scripts.telephone import deploy_telephone_contracts, hack_telephone_contracts
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network


def test_claim_ownership_of_telephone_contract():
    if network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # Arrange
        account_to_hack = get_account()
        telephone_hack_contract, telephone_contract = deploy_telephone_contracts(account_to_hack)
        original_owner = telephone_contract.owner({"from": account_to_hack})
        # Act
        hack_telephone_contracts(account_to_hack, telephone_hack_contract, telephone_contract_address)
        current_owner = telephone_hack_contract.owner({"from": account_to_hack})
        # Assert
        assert original_owner != current_owner
        assert current_owner == account_to_hack