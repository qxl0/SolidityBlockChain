import json
from solcx import compile_standard, install_solc
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()  # load env from .env
install_solc("0.6.0")
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to rinkeby
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/291b0311bd82418bbe2a7c00198c240a")
)
chain_id = 4
my_address = "0x975c5666d75913834d00f21b32D12997b557E230"
private_key = os.getenv("PRIVATE_KEY")
# print(private_key)
# create contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)
# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)
# build trx
# sign trx
# send a trx
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_recipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!!")
# working with the contract
simple_storage = w3.eth.contract(address=tx_recipt.contractAddress, abi=abi)
# Call -> Simulate making call get a return
# Transact --> Actually make state change
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_stored_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_recipt = w3.eth.wait_for_transaction_receipt(send_stored_tx)
print("updated!!")
print(simple_storage.functions.retrieve().call())
