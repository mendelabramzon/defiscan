from web3 import Web3
from web3.middleware import geth_poa_middleware
import requests
import datetime
import time
import json

matic = Web3(Web3.IPCProvider('~/.bor/data/bor.ipc'))
matic.middleware_onion.inject(geth_poa_middleware, layer=0)
add = matic.toChecksumAddress('')

with open("abis.json", "r") as x:
    abi = json.load(x)

abi_pair = '''
[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sync","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]
'''

add_pair = ''

file_name = "log.txt"
cntr = matic.eth.contract(address=add, abi=abi)
def check_trans(block_start, block_finish):
    str1 = 'https://api.polygonscan.com/api?module=account&action=txlist&address=0xbedfB43a182083b30171408952232b253eFc2028&startblock='
    str2 = '&endblock='
    str3 = '&sort=asc&apikey=FRPBPDXQQJVIUBX8UEBFX4BYGW7JAQA9ZW'
    url = str1 + str(block_start) + str2 + str(block_finish) + str3
    print("getting url")
    x = requests.get(url).json()
    print("got url")
    pair = matic.eth.contract(address=add_pair, abi=abi_pair)
    for i in range(len(x['result'])):
        try:
            tx = x['result'][i]
            hsh = tx['hash']
            print(hsh)
            our_gas = float(tx['gasPrice'])/10**9
            txdict = matic.eth.get_transaction(hsh)
            txinput = txdict['input']
            decoded_input = cntr.decode_function_input(txinput)
            for block in range(int(tx['blockNumber'])-20, int(tx['blockNumber'])+20):
                print("block", block)
                for i, rout in enumerate(decoded_input[1]['stocks']):
                    toks_our = decoded_input[1]['path'][i:i+2]
                    fac_our = decoded_input[1]['factories'][i]
                    txs = matic.eth.get_block(block)
                    for trans in txs['transactions']:
                        try:
                            receipt = matic.eth.get_transaction_receipt(trans)
                            L = len(pair.events.Swap().processReceipt(receipt, errors='DISCARD'))
                            for i in range(L):
                                pool_add = pair.events.Swap().processReceipt(receipt, errors='DISCARD')[i]['args']['address']
                                gas = int(receipt['effectiveGasPrice'], 16)/10**9
                                contract_pair = matic.eth.contract(address=pool_add, abi=abi_pair)
                                fac = contract_pair.caller.factory()
                                tok_0 = contract_pair.caller.token0()
                                tok_1 = contract_pair.caller.token1()
                                if fac == fac_our and ((tok_0 == toks_our[0] and tok_1 == toks_our[1]) or
                                                      (tok_1 == toks_our[0] and tok_0 == toks_our[1])):
                                    print("maybe a competitor")
                                    with open(file_name, 'a') as x:
                                        if gas < our_gas:
                                            print("Our gas was bigger")
                                            x.write("Our gas was bigger\n")
                                        else:
                                            print("We were outplayed")
                                            x.write("We were outplayed\n")
                                        print("pool {}\nour trans {}\nhis trans {}".format(pool_add, hsh, receipt['transactionHash'].hex()))
                                        x.write("pool {}\nour trans {}\nhis trans {}\n".format(pool_add, hsh, receipt['transactionHash'].hex()))
                                        print("gas: our {}, their {}\n".format(our_gas, gas))
                                        x.write("gas: our {}, their {}\n".format(our_gas, gas))
                        except: # Exception as e:
                            pass
        except Exception as e:
            print(e)


def find_disbalance(contract_add, tx_hash):
    pair = matic.eth.contract(address=add_pair, abi=abi_pair)
    txdict = matic.eth.get_transaction(tx_hash)
    tx_block = txdict['blockNumber']
    receipt = matic.eth.get_transaction_receipt(tx_hash)
    L = len(pair.events.Swap().processReceipt(receipt, errors='DISCARD'))
    for i in range(L):
        pool_add = pair.events.Swap().processReceipt(receipt, errors='DISCARD')[i]['args']['to']
        contract_pair = matic.eth.contract(address=pool_add, abi=abi_pair)
        fac = contract_pair.caller.factory()
        tok_0 = contract_pair.caller.token0()
        tok_1 = contract_pair.caller.token1()
    for i in range(100):
        block = tx_block - i
        txs = matic.eth.get_block(block)
        for tx in txs['transactions']:
