from brownie import accounts, config, SimpleStorage
import os


def deploy_simple_storage():
    # account = accounts.load("qiang-account")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    account = accounts.add(config["wallets"]["from_key"])
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(13, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def main():
    deploy_simple_storage()
