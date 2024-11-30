from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
import crypto_tools as cr

w3 = Web3(Web3.IPCProvider('~/.bor/data/bor.ipc'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

p_abi = '''
[{"type":"constructor","stateMutability":"nonpayable","payable":false,"inputs":[]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":true},{"type":"address","name":"spender","internalType":"address","indexed":true},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"Burn","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1","internalType":"uint256","indexed":false},{"type":"address","name":"to","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"Mint","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"Swap","inputs":[{"type":"address","name":"sender","internalType":"address","indexed":true},{"type":"uint256","name":"amount0In","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1In","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount0Out","internalType":"uint256","indexed":false},{"type":"uint256","name":"amount1Out","internalType":"uint256","indexed":false},{"type":"address","name":"to","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"Sync","inputs":[{"type":"uint112","name":"reserve0","internalType":"uint112","indexed":false},{"type":"uint112","name":"reserve1","internalType":"uint112","indexed":false}],"anonymous":false},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":true},{"type":"address","name":"to","internalType":"address","indexed":true},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"DOMAIN_SEPARATOR","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"MINIMUM_LIQUIDITY","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"PERMIT_TYPEHASH","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"","internalType":"address"},{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"uint256","name":"amount0","internalType":"uint256"},{"type":"uint256","name":"amount1","internalType":"uint256"}],"name":"burn","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"factory","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint112","name":"_reserve0","internalType":"uint112"},{"type":"uint112","name":"_reserve1","internalType":"uint112"},{"type":"uint32","name":"_blockTimestampLast","internalType":"uint32"}],"name":"getReserves","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"initialize","inputs":[{"type":"address","name":"_token0","internalType":"address"},{"type":"address","name":"_token1","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"kLast","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"mint","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"nonces","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"permit","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"price0CumulativeLast","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"price1CumulativeLast","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"skim","inputs":[{"type":"address","name":"to","internalType":"address"}],"constant":false},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"swap","inputs":[{"type":"uint256","name":"amount0Out","internalType":"uint256"},{"type":"uint256","name":"amount1Out","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"bytes","name":"data","internalType":"bytes"}],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[],"name":"sync","inputs":[],"constant":false},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token0","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token1","inputs":[],"constant":true},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[],"constant":true},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false},{"type":"function","stateMutability":"nonpayable","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}],"constant":false}]
'''

with open("pools.json", "r") as x:
    pools_json = json.load(x)

#alive_factories = set()
n_markets = {}
alive = []
dead = []
pools = []                          # [..., [add_tok0, add_tok1, add_pool], ...]
balances = {}                       # {..., add_pool:[amount_tok0, amount_tok1], ...}
for i, pool in enumerate(pools_json):
    try:
        print(i)
        add_pool = pool["address"]
        #contract_pool = w3.eth.contract(address=add_pool, abi=p_abi)
        #a = contract_pool.caller.getReserves()
        #contract_token0 = w3.eth.contract(address=contract_pool.caller.token0(), abi=p_abi)
        #contract_token1 = w3.eth.contract(address=contract_pool.caller.token1(), abi=p_abi)
        tok0 = pool["token0"] #contract_token0.caller.address
        tok1 = pool["token1"] #contract_token1.caller.address
        dec0 = pool["dec0"] #contract_token0.caller.decimals()
        dec1 = pool["dec1"] #contract_token1.caller.decimals()
        amn0 = pool["reserve0"]
        amn1 = pool["reserve1"]
        if amn0/10**dec0 < 5 or amn1/10**dec1 < 5:
            dead.append(add_pool)
        else:
            balances.update({add_pool: [amn0 / 10 ** dec0, amn1 / 10 ** dec1]})
            pools.append([tok0, tok1, add_pool])
            alive.append(pool)
            #alive_factories.add(pool["factory"])
            #try:
            #    n_markets[pool["factory"]]+=1
            #except:
            #    n_markets.update({pool["factory"]:1})
    except Exception as e:
        print(e)

print("alive", len(alive))
#print("alive facs", len(alive_factories))
print(n_markets)

with open("test_numbers", "w") as x:
    json.dump(n_markets, x)

with open("alive_pools.json", "w") as x:
    json.dump(alive, x)

print("pools", len(pools))

pools = cr.connected_pools(pools)
print("pools", len(pools))

liquidities, courses = cr.pool_liquidities(pools, balances)
print("liqs", len(list(liquidities.keys())))

pools = cr.big_pools(pools, liquidities, 3000)
print("big pools", len(pools_json))

pools = cr.connected_pools(pools)
print("pools", len(pools))

stables = []
for pool in pools:
    if abs(1 - courses[pool[0]]) < 0.015:
        stables.append(pool)

s = 0
while s < len(stables):
    stable = stables[s]
    l = s + 1
    ss = 0
    while l < len(stables):
        if stables[s][:2] == stables[l][:2]:
            if liquidities[stables[s][2]] > liquidities[stables[l][2]]:
                pools.remove(stables[l])
                stables.pop(l)
            else:
                pools.remove(stables[s])
                stables.pop(s)
                ss = 1
                break
        else:
            l += 1
    if ss == 0:
        s += 1

pools = cr.connected_pools(pools)
print("big pools without extra stables", len(pools))

with open("big_pools.json", "w") as x:
    json.dump(pools, x)
