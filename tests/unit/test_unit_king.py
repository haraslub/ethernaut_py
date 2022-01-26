import pytest
from scripts.helpers import get_account
from scripts.king import init_king_deployment, attack_king_contract, claim_throne
from brownie import interface, King, KingAttack, config, network, exceptions
from web3 import Web3


def test_claim_throne():
    # Assert
    king_contract = init_king_deployment(King, contract_interface=interface.IKing)
    first_king = king_contract._king()
    # Act
    claiming_account = get_account(2)
    claim_throne(claiming_account, king_contract, Web3.toWei("1", "ether"))
    new_king = king_contract._king()
    # Assert
    # Claim successfuly a throne
    assert first_king != new_king
    # Unsuccessful claim of a throne
    with pytest.raises(exceptions.VirtualMachineError):
        new_claimer = get_account(3)
        claim_throne(new_claimer, king_contract, Web3.toWei("0.1", "ether"))


def main():
    test_claim_throne()