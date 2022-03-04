import json
from web3 import Web3, HTTPProvider
from decouple import config

privatekey = config('PRIVATE_KEY')
blockadd = config('Url')
web3 = Web3(Web3.HTTPProvider(blockadd))
accaunt= '0x49939aeD5D127C2d9a056CA1aB9aDe9F79fa8E81'
compiled_contract_path = './json/donation.json'
deployed_contract_address = '0x474673756595c91d137b68762D66a7658Cf250bb'
abi = json.loads('[ { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "inputs": [], "name": "balanceContract", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "donat", "outputs": [], "stateMutability": "payable", "type": "function" }, { "inputs": [], "name": "seeAddress", "outputs": [ { "internalType": "address[]", "name": "", "type": "address[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "payAdd", "type": "address" } ], "name": "seePay", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "sum", "type": "uint256" }, { "internalType": "address payable", "name": "sender", "type": "address" } ], "name": "withdrawal", "outputs": [], "stateMutability": "nonpayable", "type": "function" } ]')
contract = web3.eth.contract(address=deployed_contract_address, abi=abi)
nonce = web3.eth.get_transaction_count(accaunt)

def see_addr_donated():
    balance = contract.functions.seeAddress().call()
    print(balance)



def seePay():
    addr = str(input("Input checked addres: "))
    checkaddr = contract.functions.seePay(addr).call()
    print(checkaddr)


def donate():
    value = int(input("Input value donate: "))
    tx = contract.functions.donat().buildTransaction({
        'nonce': nonce,
        'value': value,
        'maxFeePerGas': web3.toWei('20', 'gwei'),
        'maxPriorityFeePerGas': web3.toWei('11', 'gwei'),
    })
    signed_txn = web3.eth.account.signTransaction(tx, private_key=privatekey)
    transaction = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    if len(transaction)>0:
        print("Succes")
    else:
        print("Error donate")

def withdrawal():
    sum = int(input("INput Value: "))
    to = str(input("Input address: "))
    tx = contract.functions.withdrawal(sum,to).buildTransaction({
        'nonce': nonce,
        'maxFeePerGas': web3.toWei('20', 'gwei'),
        'maxPriorityFeePerGas': web3.toWei('11', 'gwei'),
    })
    signed_txn = web3.eth.account.signTransaction(tx, private_key=privatekey)
    web3.eth.sendRawTransaction(signed_txn.rawTransaction)


withdrawal()

