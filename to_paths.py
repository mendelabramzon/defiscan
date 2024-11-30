from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from concurrent.futures import ThreadPoolExecutor
import crypto_tools as cr
import datetime
import time

w3 = Web3(Web3.IPCProvider('~/.bor/data/bor.ipc'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def run_io_tasks_in_parallel(tasks):
    results = []
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            results.append(running_task.result())
        return results

p_abi = '''
[{"type":"constructor","stateMutability":"nonpayable","payable":false,"inputs":[]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":true},{"type":"address","name":"spender","internalType":"address","indexed":true},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"Burn","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1","internalType":"uint256","indexed":false},{"type":"address","name":"to","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"Mint","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"Swap","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0In","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1In","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount0Out","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1Out","internalType":"uint256","indexed":false},{"type":"address","name":"to","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"Sync","inputs":[{"type":"uint112","name":"reserve0","internalType":"uint112","indexed":false},{"type":"uint112","name":"reserve1","internalType":"uint112","indexed":false}],"anonymous":false},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":true},{"type":"address","name":"to","internalType":"address","indexed":true},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"DOMAIN_SEPARATOR","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"MINIMUM_LIQUIDITY","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"PERMIT_TYPEHASH","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"","internalType":"address"},{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"uint256","name":"amount0","internalType":"uint256"},{"type":"uint256","name":"amount1","internalType":"uint256"}],"name":"burn","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"factory","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint112","name":"_reserve0","internalType":"uint112"},{"type":"uint112","name":"_reserve1","internalType":"uint112"},{"type":"uint32","name":"_blockTimestampLast","internalType":"uint32"}],"name":"getReserves","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"initialize","inputs":[{"type":"address","name":"_token0","internalType":"address"},{"type":"address","name":"_token1","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"kLast","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"mint","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"nonces","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"permit","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"price0CumulativeLast","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"price1CumulativeLast","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"skim","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"swap","inputs":[{"type":"uint256","name":"amount0Out","internalType":"uint256"},{"type":"uint256","name":"amount1Out","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"bytes","name":"data","internalType":"bytes"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"sync","inputs":[],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token0","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token1","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false}]
'''

with open("flash20abi.txt", "r") as x:
    our_contr_abi = json.load(x)
our_contr_add = ""
our_contract = w3.eth.contract(address=our_contr_add, abi=our_contr_abi)

with open("big_pools.json", "r") as x:
    pools = json.load(x)
for pool in pools:
    print(pool[2])

pools_info = {}
balances = {}
for i, pool in enumerate(pools):
    add = pool[2]
    exec("contract_pool_{} = w3.eth.contract(address=add, abi=p_abi)".format(pool[2]))
    tok0, tok1, amn0, amn1, dec0, dec1 = our_contract.caller.pairInfo(add)[:]
    pools_info.update({add: [tok0, tok1, amn0, amn1, dec0, dec1]})
    balances.update({pools[i][2]: [amn0 / 10 ** dec0, amn1 / 10 ** dec1]})

with open("pools_base.json", "w") as f:
    json.dump(pools_info, f)

liquidities, courses = cr.pool_liquidities(pools, balances)

print("liqs", len(liquidities))
for x in liquidities:
    print(x, liquidities[x])

wmatic_add ='0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
weth_add = '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619'
usdc_add = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
wbtc_add = '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6'
usdt_add = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'
dai_add = '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'

paths_toks, paths_pairs = cr.paths(pools, 3, toks=[weth_add, usdc_add, wbtc_add, wmatic_add, usdt_add, dai_add])
# path_toks = [..., [tok_add_i1, tok_add_i2, tok_add_i3, tok_add_i1], ...]
# path_pairs = [..., [pool_add_i1, pool_add_i2, pool_add_i3], ...]
print("paths_toks", len(paths_toks))
print("paths_pairs", len(paths_pairs))

stable_pools = []
i = 0
print("pools", len(pools))
while i < len(pools):
    pool = pools[i][2]
    if abs(1 - balances[pool][0] / balances[pool][1]) < 0.01:
        stable_pools.append(pools[i])
        pools.pop(i)
    else:
        i += 1
print("pools", len(pools))
print("stables", len(stable_pools))

pool_adds = [pool[2] for pool in pools]
stable_adds = [pool[2] for pool in stable_pools]

start = datetime.datetime.now()
while True:
    ratios = {}

    for i, pool in enumerate(pools):
        try:
            ratios.update({pool[2]: [balances[pool[2]][1] / balances[pool[2]][0]]})
        except Exception as e:
            print(e)
    end = datetime.datetime.now()
    time_taken = end.timestamp() - start.timestamp()

    t_wait = 4
    if (time_taken < t_wait):
        print("waiting", t_wait)
        time.sleep(t_wait - time_taken)
    start = datetime.datetime.now()
    pool_values = {}
    for i, pool in enumerate(pools):
        add = pool[2]
        tok0, tok1, amn0, amn1, dec0, dec1 = our_contract.caller.pairInfo(add)[:]
        balances.update({add: [amn0 / 10 ** dec0, amn1 / 10 ** dec1]})
        ratios[add].append(balances[add][1] / balances[add][0])
        try:
            pool_values.update({add: liquidities[add]})
        except Exception as e:
            print(e)
            pool_values.update({add: 0})

    paths_values = {}
    for i, path_pairs in enumerate(paths_pairs):
        S = 0
        for pool in path_pairs:
            if pool in pool_adds:
                S += 1/pool_values[pool]
            elif pool in stable_adds:
                S += 0
            else:
                raise ValueError("can't find such pool!")
        try:
            paths_values.update({1/S: [paths_toks[i], path_pairs]})
        except: pass

    vals = list(paths_values.keys())
    print("length of paths_values", len(vals))
    vals.sort()
    vals = vals[::-1]
    used_pools = set()
    unused_pools = pool_adds[:]
    current_number = 0
    paths_toks_to_write = [] #set()
    paths_pools_to_write = [] #set()

    best_paths_for_pool = {}
    s=0
    for add in pool_adds:
        for i in range(len(vals)):
            val = vals[i]
            path_pairs = paths_values[val][1]
            S = 0
        #for pool_add in path_pairs:
            #if pool_add in unused_pools:
            if add in path_pairs:
                S += 1
                unused_pools.remove(add)
                used_pools.add(add)
                best_paths_for_pool.update({add: paths_values[val]})
                break
        if S > 0:
            # print("good path", path_pairs)
            path_toks = paths_values[val][0]
            if path_toks not in paths_toks_to_write:
                paths_toks_to_write.append(path_toks)
                paths_pools_to_write.append(path_pairs)
            if len(unused_pools) == 0:
                print(i)
                s=1
                break
    if s == 0:
        print("remained unused", len(unused_pools))
    for i, path_pairs in enumerate(paths_pools_to_write):
        path_toks = paths_toks_to_write[i]
        for j, add in enumerate(path_pairs):
            contract_pair = w3.eth.contract(address=add, abi=p_abi)
            fac = contract_pair.caller.factory()
            tok_0 = contract_pair.caller.token0()
            tok_1 = contract_pair.caller.token1()
            if not ((tok_0 == path_toks[j] and tok_1 == path_toks[j + 1]) or
                                            (tok_1 == path_toks[j] and tok_0 == path_toks[j + 1])):
                print("facs, toks and pairs do not coincide")
    # global_dict = {"toks": paths, "facs": factories, "routs": routers, "pools": paths_pools}
    global_dict = {"toks": paths_toks_to_write, "pools": paths_pools_to_write}

    with open("big_dict.json", "w") as f:
        json.dump(global_dict, f)

    with open("best_path_for_pool.json", "w") as f:
        json.dump(best_paths_for_pool, f)
