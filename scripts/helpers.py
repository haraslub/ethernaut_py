from brownie import accounts, network, config

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def deploy_contract(contract, account):
    print("Deploying contract..")
    contract_deployment = contract.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False))
    return contract_deployment


def get_instance_address(instance_name, contract_to_deploy=None):
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS) & (contract_to_deploy != None):
        deploying_account = get_account(1)
        print("Deploying contract to local network: {}".format(network.show_active()))
        contract_deployed = contract_to_deploy.deploy({"from": deploying_account})
        contract_to_deployed_address = contract_deployed.address
    else:
        contract_to_deployed_address = config["networks"][network.show_active()][instance_name]
    
    return contract_to_deployed_address