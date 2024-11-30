from eth_typing import abi
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
from web3.middleware import geth_poa_middleware
import numpy as np
import json
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import time
import csv
matic_provider = Web3.IPCProvider('~/.bor/data/bor.ipc')
matic.middleware_onion.inject(geth_poa_middleware, layer=0)

with open("pools_base.json", "r") as x:
    pools_info = json.load(x)

with open("best_path_for_pool.json", "r") as x:
    bpfp = json.load(x)

with open("flash20abi.txt", "r") as x:
    our_abi = json.load(x)

with open("liquidities.json", "r") as x:
    liquidities = json.load(x)
#with open("/flashswap3/address_list.txt", "r") as x:
#    add_list = json.load(x)

#with open("/flashswap3/pk_list.txt", "r") as x:
#     pk_list = json.load(x)

qq = csv.reader(open('/flashswap3/address_list.txt'), delimiter='\n')
accounts = [l[0] for l in qq]
pp = csv.reader(open('/flashswap3/pk_list.txt'), delimiter='\n')
pks = [l[0] for l in pp]
address_flash = ''
flash20 = matic.eth.contract(address=address_flash, abi=our_abi)


#latest_block = 0
threshold = 0.0045
C = 0.035
def swap_scan(from_block=0, to_block=0, latest='True'):
    latest_block = 0
    with open('abis.json') as abis:
        pair_abi = json.load(abis,)['pair_abi']
    pair = matic.eth.contract(abi=pair_abi)
    if latest=='True':
        num = 0
        while True:
            try:
                start = time.time()
                block = matic.eth.get_block('latest')
                block_n = block['number']
                print("block", type(block_n))
                if (block_n > latest_block):
                    start1 = time.time()
                    with open("triggers.json", "r") as x:
                        triggers = json.load(x,)
                    triggers.update({block_n: []})
                    with open("swaps.json", "r") as x:
                        swaps = json.load(x,)
                    swaps.update({block_n:[]})
                    txs = block['transactions']
                    for tx in txs:
                        receipt = matic.eth.get_transaction_receipt(tx)
                        log = pair.events.Swap().processReceipt(receipt, errors=DISCARD)
                        if len(log) > 0:
                            for log_n in log:
                                amount0In = log_n['args']['amount0In']
                                amount0Out = log_n['args']['amount0Out']
                                amount1In = log_n['args']['amount1In']
                                amount1Out = log_n['args']['amount1Out']
                                gas_price = receipt['effectiveGasPrice']
                                address = log_n['address']
                                swaps[block_n].append([Web3.toHex(tx), address, amount0In, amount1In, amount0Out, amount1Out, gas_price])
                                tok0, tok1, amn0, amn1, dec0, dec1 = pools_info[address][:]
                                liq = amn0/10**dec0
                                path_toks, path_pools = bpfp[address]
                                liqs = [liquidities[pool] for pool in path_pools]
                                condition = threshold + np.sqrt(2*C/liq*sum(liqs))
                                if (amount0In == 0 and amount1In / amn1 > condition) or (amount1In == 0 and amount0In / amn0 > condition):
                                    print("A trigger!")
                                    path_toks, path_pools = bpfp[address]
                                    triggers[block_n].append(
                                        [Web3.toHex(tx), address, amount0In, amount1In, amount0Out, amount1Out])
                                    try:
                                        if amount0In == 0:
                                            ind = path_pools.index(address)
                                            if tok1 == path_toks[ind] and tok0 == path_toks[ind+1]:
                                                path_toks = path_toks[::-1]
                                                path_pools = path_pools[::-1]
                                        else:
                                            ind = path_pools.index(address)
                                            if tok0 == path_toks[ind] and tok1 == path_toks[ind+1]:
                                                path_toks = path_toks[::-1]
                                                path_pools = path_pools[::-1]
                                        nonce = matic.eth.getTransactionCount(accounts[num % len(pks)])
                                        gas_price = matic.toWei(55,'gwei')
                                        gasLimit = int(1000000)
                                        tx = flash20.functions.poehali(path_toks, path_pools).buildTransaction(dict(gasPrice=gas_price, gas=gasLimit, nonce=nonce))
                                        signed_tx = matic.eth.account.signTransaction(tx, private_key=pks[num % len(pks)])
                                        matic.eth.sendRawTransaction(signed_tx.rawTransaction)
                                    except Exception as e:
                                        print(e)
                                    num += 1
                    with open("swaps.json", "w") as x:
                        json.dump(swaps, x)
                    with open("triggers.json", "w") as x:
                        json.dump(triggers, x)
                    end = time.time()
                    time_spent = end-start
                    t1 = end - start1
                    print("t0", time_spent)
                    print("t1", t1)
            except Exception as e: print(e)
    else:
        for block_n in range(from_block, to_block+1):
            start = time.time()
            logs = dict()
            block = matic.eth.get_block(block_n)
            block_n = block['number']
            print(block_n)
            txs = block['transactions']
            for tx in txs:
                receipt = matic.eth.get_transaction_receipt(tx)
                log = pair.events.Swap().processReceipt(receipt, errors=DISCARD)
                if len(log) > 0:
                    for log_n in log:
                        amount0In = log_n['args']['amount0In']
                        amount0Out = log_n['args']['amount0Out']
                        amount1In = log_n['args']['amount1In']
                        amount1Out = log_n['args']['amount1Out']
                        gas_price = receipt['effectiveGasPrice']
                        sender = log_n['args']['sender']
                        to = log_n['args']['to']
                        address = log_n['address']
                        position = log_n['logIndex']
                        add_pool(address)
                        logs.update({'block': block_n, 'address': address, 'amount0In': amount0In, 'amount1In': amount1In, 'amount0Out': amount0Out,
                                    'amount1Out': amount1Out, 'gasPrice': Web3.toInt(hexstr=gas_price), 'sender': sender, 'to': to, 'position': position, 'hash': Web3.toHex(tx)})
            with open('swaps.json', 'r') as swaps:
                events = json.load(swaps,)
            events.append(logs)
            with open('swaps.json', 'w') as swaps:
                json.dump(events, swaps)
            end = time.time()
            time_spent = end-start
            print(time_spent)

def add_pool(pair_address):
    with open('pools.json','r') as pools_json:
        pools=json.load(pools_json,)
    if search_dict(pair_address,'address',pools)==True:
        pass
    else:
        print('new pool')
        with open('abis.json') as abis:
            pair_abi = json.load(abis,)['pair_abi']
        contract = matic.eth.contract(address=pair_address,abi=pair_abi)
        token0=contract.caller.token0()
        token1=contract.caller.token1()
        factory=contract.caller.factory()
        pools.append({"address":pair_address,"token0":token0,"token1":token1, "factory":factory})
    with open('pools.json','w') as pools_json:
        json.dump(pools,pools_json)

def search_dict(value_to,key_to,data):
    k=0
    try:
        for dat in data:
            if value_to in dat[key_to]:
                k+=1
    except Exception as e:
        print(e)
    if k!=0: return True
    else: return False
swap_scan()
