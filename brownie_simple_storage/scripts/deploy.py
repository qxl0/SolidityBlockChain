from brownie import accounts
import os


def deploy_simple_storage():
    # account = accounts.load("qiang-account")
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    print(account)


def main():
    deploy_simple_storage()
