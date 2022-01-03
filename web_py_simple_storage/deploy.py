from re import S
import re
from sys import stdout
from solcx import compile_standard
import json
import os
from dotenv import load_dotenv, dotenv_values

from web3 import Web3

# config = dotenv_values(".env")
load_dotenv(override=True)


def compile():
    with open("web_py_simple_storage/SimpleStorage.sol", "r") as file:
    # with open("./SimpleStorage.sol", "r") as file:
        simple_storage_file = file.read()
    # print(simple_storage_file)

    compile_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {
                "SimpleStorage.sol": {"content": simple_storage_file},
            },
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.6.0",
    )

    return compile_sol


compile_sol = compile()


with open("compiled_file.json", "w") as file:
    json.dump(compile_sol, file)

# get bytecode
byte_code = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]


# get ABI
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# w3.middleware_onion.inject(geth_poa, layer=0)
chain_id = 1337
# chain_id = 4

my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# my_address = "0xAb0f1BF68826b2742dA807f690135a143362aCD5"

# For connecting to Rinkeby
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# w3 = Web3(
#     Web3.HTTPProvider("https://rinkeby.infura.io/v3/499a94b7e262453b99296a2d937c98a8")
# )


# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

private_key = os.getenv("PRIVATE_KEY")
# 1. Build a Transaction
# 2. Sign a Transaction
# 3. Send a Transaction

def build():
    # Create the contract in python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=byte_code)

    print("Deploying contract ....")
    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "from": my_address,
            "gasPrice": w3.eth.gas_price,
            "nonce": nonce,
        }
    )
    # Signed Transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Send Transaction
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return txn_hash

transaction_hash = build()

tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print("Contract Deployed successfully ...")

# Working with the contract now
# Needs : Contract Address and Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Initial value of the contract..
print("Initialize contract value ")
# print(simple_storage.functions.retrieve().call())
print("Updating value .. ")
# simple_storage.functions.store(30).transact({"from": my_address})

def retrieveFunction():
    return simple_storage.functions.retrieve().call()

def storeFunction(number : int):
    nonce = w3.eth.getTransactionCount(my_address)
    print("This is the new nonce ", nonce)
    store_transaction = simple_storage.functions.store(number).buildTransaction(
        {
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce ,
            "gasPrice": w3.eth.gas_price,
        }
    )

    signed_store_tnx = w3.eth.account.sign_transaction(
        store_transaction, private_key=private_key
    )
    send_store_txn = w3.eth.send_raw_transaction(signed_store_tnx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)

    return "successful"

# storeFunction(100)

# print("Value updated")
# print(retrieveFunction())
