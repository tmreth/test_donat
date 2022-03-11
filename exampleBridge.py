import json
from web3 import Web3
import eth_abi.abi
from web3.auto import w3
from web3.middleware import geth_poa_middleware
#Подключение к тестовому блокчейну где лежит смарт контракт
url_poligon = "http://127.0.0.1:8545"
w3_poligon = Web3(Web3.HTTPProvider(url_poligon))
address = w3_poligon.eth.account.privateKeyToAccount(PRIVATE_KEY).address
abi_poligon = '[ { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "address", "name": "sender", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "astate", "type": "uint256" } ], "name": "status", "type": "event" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "allReState", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "reSatate", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "seeState", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "update", "type": "uint256" }, { "internalType": "address", "name": "updater", "type": "address" } ], "name": "updateState", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" } ]'
w3_poligon.middleware_onion.inject(geth_poa_middleware, layer=0)
conAddress_poligon = '0x60048c3d1562c22FC20E72974733535E89d064d3'
contract_Poligon = w3_poligon.eth.contract(address=conAddress_poligon, abi=abi_poligon)

#Подключение к тестовому блокчейну где лежит смарт контракт
url_rinkeby = "wss://eth-rinkeby.alchemyapi.io/v2/rHsv2KyJ01ncUv3_q1JCdZJ7kGSUFlvm"
w3_rinkeby= Web3(Web3.WebsocketProvider(url_rinkeby))
abi_rinkeby = '[ { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "address", "name": "sender", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "astate", "type": "uint256" } ], "name": "status", "type": "event" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "allReState", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "reSatate", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "seeState", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "update", "type": "uint256" }, { "internalType": "address", "name": "updater", "type": "address" } ], "name": "updateState", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" } ]'
w3_rinkeby.middleware_onion.inject(geth_poa_middleware, layer=0)
conAddress_rinkeby = '0x288aB4EAb8cC56A03f6187fE661688b0C5b90006'#Адрес смарт контракта
contract_Rinkeby = w3_rinkeby.eth.contract(address=conAddress_rinkeby, abi=abi_rinkeby)


# Состояние контракта в сети Poligon
def statePoligon():
    state = contract_Poligon.functions.seeState().call()
    print(state)
statePoligon()

# Состояние контракта в сети Rinkeby
def stateRinkeby():
    state = contract_Rinkeby.functions.seeState().call()
    print(state)
stateRinkeby()

# Поиск последнего изменения состояния в тестовой сети1
def examination():
    poligon_state = contract_Poligon.events.status.createFilter(fromBlock='latest').get_all_entries()
    print(poligon_state)
    if (len(poligon_state) > 0):
        for state in poligon_state:
            poligon_stat = state['args']['sender']
            changed_poligon = state['args']['astate']
            return changed_poligon



add = 0
# Поиск последнего изменения состояния в тестовой сети2
def examination2():
    rinkeby_state = contract_Rinkeby.events.status.createFilter(fromBlock=1 , toBlock="latest").get_all_entries()
    print(rinkeby_state)
    if (len(rinkeby_state) > 0):
        for state in rinkeby_state:
            global add
            add = state['args']['sender']
            changed_rinkeby = state['args']['astate']
            return changed_rinkeby


def sync():
    # Условия синхронизации
    if examination() > examination2():
        tx = contract_Poligon.functions.updateState(examination(),add).buildTransaction({
            'nonce': w3_poligon.eth.getTransactionCount(address),
            'maxFeePerGas': w3_poligon.toWei('20', 'gwei'),
            'maxPriorityFeePerGas': w3_poligon.toWei('11', 'gwei'),
        })
        signed_txn = web3.eth.account.signTransaction(tx, private_key=address)
        web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print("success")

    if examination() < examination2():
        tx = contract_Rinkeby.functions.updateState(examination2(),add).buildTransaction({
            'nonce': w3_rinkeby.eth.getTransactionCount(address),
            'maxFeePerGas': w3_rinkeby.toWei('20', 'gwei'),
            'maxPriorityFeePerGas': w3_rinkeby.toWei('11', 'gwei'),
        })
        signed_txn = web3.eth.account.signTransaction(tx, private_key=address)
        web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print("success")
sync()
