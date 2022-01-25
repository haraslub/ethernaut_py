import web3
from brownie import network, Delegate, Delegation, interface
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.delegation import initial_setup, deploy_attack_on_delegate_contract

if network.show_active() == "rinkeby": from web3.auto.infura.rinkeby import w3 
else: from web3.auto import w3


def check_web3_connection(w3):
    if w3.isConnected():
        print("Connection successful: {}".format(w3.isConnected()))
        print("Connected to: {}".format(w3.clientVersion))
        return True
    return False


def test_attack_delegate_contract():
    # Arrange
    hacking_account = get_account()
    delegate_contract = initial_setup(Delegate, interface.IDelegate, "delegation_instance")
    # Act
    if check_web3_connection(w3):
        original_contract_owner = w3.eth.get_storage_at(delegate_contract.address, 0, "latest").hex()
        deploy_attack_on_delegate_contract(Delegation, delegate_contract)
        current_contract_owner = w3.eth.get_storage_at(delegate_contract.address, 0, "latest").hex()
    # Assert
    assert original_contract_owner != current_contract_owner
    assert current_contract_owner == hacking_account


def main():
    test_attack_delegate_contract


