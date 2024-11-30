from eth_typing import abi
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
from web3.middleware import geth_poa_middleware
import numpy as np
import json
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import time
import csv
import requests
import traceback
from concurrent.futures import ThreadPoolExecutor
matic = Web3(Web3.IPCProvider('~/.local/share/openethereum/jsonrpc.ipc'))
matic.middleware_onion.inject(geth_poa_middleware, layer=0)

def get_mempool():
    headers = {
}
    json_data = {
    'method': 'parity_pendingTransactions',
    'params': [],
    'id': 1,
    'jsonrpc': '2.0',
            }
    mempool = requests.post('http://127.0.0.1:8545', headers=headers, json=json_data).json()['result']
    return mempool


with open("pools.json", "r") as x:
    pools = json.load(x)

with open("best_path_for_pool.json", "r") as x:
    bpfp = json.load(x)

with open("flash20abi.txt", "r") as x:
    our_abi = json.load(x)

with open("liquidities.json", "r") as x:
    liquidities = json.load(x)

qq = csv.reader(open('address_list.txt'), delimiter='\n')
accounts = [l[0] for l in qq]
pp = csv.reader(open('pk_list.txt'), delimiter='\n')
pks = [l[0] for l in pp]
address_flash = ''
flash20 = matic.eth.contract(address=address_flash, abi=our_abi)

with open('abis_new.json') as abis:
    flash_abi = json.load(abis,)['flash']
with open('abis_new.json') as abis:
    router_abi = json.load(abis,)['router_honey']
with open('abis_new.json') as abis:
    factory_abi = json.load(abis,)['factory']
router = matic.eth.contract(abi=router_abi)
flash = matic.eth.contract(address="", abi=flash_abi)

threshold = 0.0003
C = 0.035
def swap_scan(from_block=0, to_block=0, latest='True'):
    hashes = []
    start_hsh = time.time()
    num = 0
    while True:
            start = time.time()
            mempool = get_mempool()
            Q=0
            for tx in mempool:
                try:
                    if tx['hash'] not in hashes:
                        decode = router.decode_function_input(tx['input'])
                        name = str(decode[0])
                        if "swap" in name:
                            Q+=1
                            log = decode[1]
                            hashes.append(tx['hash'])
                            log['router']=tx['to']
                            log['type']=tx['type']
                            if str(log['type']) == '0x0':
                                log['gasprice']=tx['gasPrice']
                                #print(int(log['gasprice'], 16)/10**9)
                            else:
                                log['gasprice']=tx['gasPrice']
                                log['maxFeePerGas'] = tx['maxFeePerGas']
                                log['maxPriorityFeePerGas'] = tx['maxPriorityFeePerGas']
                                #print([int(log['gasprice'], 16)/10**9, int(log['maxFeePerGas'], 16)/10**9, int(log['maxPriorityFeePerGas'], 16)/10**9])
                            router1 = matic.eth.contract(address=matic.toChecksumAddress(log['router']), abi=router_abi)
                            factory_address = router1.caller.factory()
                            amount = log['amountIn']
                            for i in range(len(log['path'])-1):
                                tok0 = log['path'][i]
                                tok1 = log['path'][i + 1]
                                for pool in pools:
                                   # print(pool)
                                   # exit()
                                    if tok0==pool["token0"] and tok1==pool["token1"] and pool["factory"] == factory_address:
                                        res0 = pool["reserve0"] #/ 10 ** pool["dec0"]
                                        res0_norm = pool["reserve0"] / 10 ** pool["dec0"]
                                        res1 = pool["reserve1"] #/ 10 ** pool["dec1"]
                                        res1_norm = pool["reserve1"] / 10 ** pool["dec1"]
                                        address = pool["address"]
                                        break
                                    elif tok0==pool["token1"] and tok1==pool["token0"] and pool["factory"] == factory_address:
                                        res0 = pool["reserve1"] #/ 10 ** pool["dec1"]
                                        res0_norm = pool["reserve1"] / 10 ** pool["dec1"]
                                        res1 = pool["reserve0"] #/ 10 ** pool["dec0"]
                                        res1_norm = pool["reserve0"] / 10 ** pool["dec0"]
                                        address = pool["address"]
                                        break
                                path_toks, path_pools = bpfp[address]
                                # liqs = [liquidities[pool] for pool in path_pools]
                                # condition = threshold + np.sqrt(2*C*sum([1/x for x in liqs]))

                                if (amount / res0 > threshold) and (int(log['gasprice'], 16) > 10**9+1):
                                    print("A trigger!")
                                    path_toks, path_pools = bpfp[address]
                                    print('found best pool')
                                    ind = path_pools.index(address)
                                    print('got index')
                                    if tok1 == path_toks[ind+1] and tok0 == path_toks[ind]:
                                        path_toks = path_toks[::-1]
                                        path_pools = path_pools[::-1]
                                    print('got path order')
                                    nonce = matic.eth.getTransactionCount(accounts[num % len(pks)])
                                    print('got nonce')
                                    #gas_price = max(int(log['gasprice'], 16)-2, 1)
                                    #print('got gasprice', gas_price, type(gas_price))
                                    #maxFee = matic.toWei(500, 'gwei')
                                    gasLimit = int(1000000)
                                    #print([path_toks, path_pools,gas_price/10**9,amount / res0])
                                    if str(log['type']) == '0x0':
                                        print('type0')
                                        gas_price = int(log['gasprice'], 16)
                                        trx = flash20.functions.poehali(path_toks, path_pools).buildTransaction(dict(gasPrice=gas_price, gas=gasLimit, nonce=nonce))
                                    else:
                                        print('type2')
                                        maxFee = int(log['maxFeePerGas'], 16)
                                        maxPriorFee = int(log['maxPriorityFeePerGas'], 16)
                                        trx = flash20.functions.poehali(path_toks, path_pools).buildTransaction(dict(maxFeePerGas=maxFee, maxPriorityFeePerGas=maxPriorFee, gas=gasLimit, nonce=nonce))
                                    signed_tx = matic.eth.account.signTransaction(trx, private_key=pks[num % len(pks)])
                                    print([path_toks, path_pools, gas_price/10**9, amount / res0])
                                    print('pre final')
                                    matic.eth.sendRawTransaction(signed_tx.rawTransaction)
                                    print("final")
                                amount = amount * res1 / res0

                except Exception as e:
                    if 'selector' or '0x3425638f494a9968a551cD6F001725E39CBD6F1A' in str(e): pass
                    else: print(traceback.format_exc())
                num += 1
            end = time.time()
            time_spent = end-start
            #time_hsh = end-start_hsh
            #print("t", time_spent, len(hashes))
            #print("Q", Q)
            if len(hashes) > 100:
                with open('hashes.json','w') as hashes_json:
                    json.dump(hashes[:50],hashes_json)
                hashes = hashes[50:]
            if time_spent < 0.0001:
                time.sleep(0.0001-time_spent)


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

