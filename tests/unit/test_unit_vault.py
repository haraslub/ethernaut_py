from scripts.vault import init_vault_deployment, get_info_from_slots, attack_vault_contract


def test_unlock_vault():
    # Arrange
    vault_contract = init_vault_deployment()
    # Act
    password_extracted, locked_extracted = get_info_from_slots(vault_contract)
    attack_vault_contract(vault_contract, password_extracted)
    _, locked_hacked = get_info_from_slots(vault_contract)
    # Assert
    assert locked_extracted != locked_hacked
