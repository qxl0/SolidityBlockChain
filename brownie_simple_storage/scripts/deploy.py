from brownie import accounts, config, SimpleStorage
import os


def deploy_simple_storage():
    # account = accounts.load("qiang-account")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    account = accounts.add(config["wallets"]["from_key"])
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)


def main():
    deploy_simple_storage()
