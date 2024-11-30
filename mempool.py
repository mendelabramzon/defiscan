
from web3 import Web3
from web3.middleware import geth_poa_middleware
import datetime
import web3.datastructures as wd
import json
import time
import ast
import pickle
# import copy

def output(x, a, b, fee):
    return fee * a * x / (b + fee * x)

def new_a(x,a,b,fee):
    return a - output(x,a,b,fee)

def new_b(x, b, fee):
    return b + x * fee

# matic_provider = Web3.IPCProvider('~/.bor/data/bor.ipc')
# matic = Web3(matic_provider)
# matic.middleware_onion.inject(geth_poa_middleware, layer=0)

#create contratc instance

# router_abi = '''
# [{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"_factory","internalType":"address"},{"type":"address","name":"_WETH","internalType":"address"}]},{"type":"function",">
# '''
# router_add = matic.toChecksumAddress('0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff')

# router = matic.eth.contract(address=router_add, abi=router_abi)

with open('pools.txt', 'r') as f:
    pools = ast.literal_eval(f.read())

with open('balances', 'rb') as file:
    pools_balances = pickle.load(file)
# print(pools_balances)
# exit()
fee = 0.997
while True:
    with open('balances', 'rb') as f:
        pools_balances = pickle.load(f)
    # new_balances = copy.deepcopy(pools_balances)
    try:
        #start = datetime.datetime.now()
        stat_dict = matic.geth.txpool.content()['pending']
        stat_dict = dict(stat_dict)
        list_add = list(stat_dict.keys())
        list_txs = []
        for add in list_add:
            str_num = dict(stat_dict[add]).keys()
            str_num = list(str_num)
            for num in str_num:
                parsed_tx = stat_dict[add][num]
                parsed_tx = dict(parsed_tx)
                inp = parsed_tx['input']
                add_to = parsed_tx['to']
                hsh = parsed_tx['hash']
                with open("hshs.txt","r") as f:
                    hshs = f.read()

                if str(add_to)==str(router_add).lower():
                    decoded_input = router.decode_function_input(inp)
                    if ('removeLiquidity' in str(list(decoded_input)[0])) and not (
                            'ETH' in str(list(decoded_input)[0])):
                        amount_A = decoded_input[1]['amountAMin']
                        amount_B = decoded_input[1]['amountBMin']
                        path = [decoded_input[1]['tokenA'], decoded_input[1]['tokenB']]
                        new_list = [amount_A, amount_B, path, 'removeLiquidity']
                        list_txs.append(new_list)
                        print(new_list)
                    elif ('removeLiquidity' in str(list(decoded_input)[0])) and ('ETH' in str(list(decoded_input)[0])):
                        amount_A = decoded_input[1]['amountTokenMin']
                        amount_MATIC = decoded_input[1]['amountETHMin']
                        path = [decoded_input[1]['token'], '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270']
                        new_list = [amount_A, amount_MATIC, path, 'removeLiquidityETH']
                        list_txs.append(new_list)
                        print(new_list)
                    if 'swapExactTokensForTokens' in str(list(decoded_input)[0]):
                        amount_A = decoded_input[1]['amountIn']
                        amount_out = decoded_input[1]['amountOutMin']
                        path = decoded_input[1]['path']
                        new_list = [amount_in, amount_out, path, 'swapExactTokensForTokens']
                        list_txs.append(new_list)
                    elif 'swapETHForExactTokens' in str(list(decoded_input)[0]):
                        amount_in = decoded_input[1]['amountIn']
                        amount_out = decoded_input[1]['amountOutMin']
                        path = decoded_input[1]['path']
                        new_list=[amount_in, amount_out, path, 'swapETHForExactTokens']
                        list_txs.append(new_list)
                    elif 'swapTokensForExactTokens' in str(list(decoded_input)[0]):
                        amount_in = decoded_input[1]['amountIn']
                        amount_out = decoded_input[1]['amountOutMin']
                        path = decoded_input[1]['path']
                        new_list=[amount_in, amount_out, path, 'swapTokensForExactTokens']
                        list_txs.append(new_list)
                    elif 'swapTokensForExactETH' in str(list(decoded_input)[0]):
                        amount_in = decoded_input[1]['amountIn']
                        amount_out = decoded_input[1]['amountOutMin']
                        path = decoded_input[1]['path']
                        new_list=[amount_in, amount_out, path, 'swapTokensForExactETH']
                        list_txs.append(new_list)
                    elif 'swapExactTokensForETH' in str(list(decoded_input)[0]):
                        amount_in = decoded_input[1]['amountIn']
                        amount_out = decoded_input[1]['amountOutMin']
                        path = decoded_input[1]['path']
                        new_list=[amount_in, amount_out, path, 'swapExactTokensForETH']
                        list_txs.append(new_list)
                    elif 'swapExactETHForTokens' in str(list(decoded_input)[0]):
                        amount_in = decoded_input[1]['amountIn']
                        amount_out = decoded_input[1]['amountOutMin']
                        path = decoded_input[1]['path']
                        new_list=[amount_in, amount_out, path, 'swapExactETHForTokens']
                        list_txs.append(new_list)
        print(list_txs)
        if len(list_txs) > 0:
            for txs in list_txs:
                amount_A, amount_B, path, func = txs
                if 'removeLiquidity' in func:
                    b = True
                    tok1 = path[0]
                    tok2 = path[1]
                    for pool in pools:
                        if (pool[0] == tok1 and pool[2] == tok2):
                            b = False
                            name = pool[4]
                            for s, pool_balances in enumerate(pools_balances):
                                if pool_balances[-1] == name:
                                    pool_balances[0] = pool_balances[0] - amount_A
                                    pool_balances[1] = pool_balances[1] - amount_B
                                    pools_balances[s] = pool_balances
                        elif (pool[2] == tok1 and pool[0] == tok2):
                            b = False
                            name = pool[4]
                            for s, pool_balances in enumerate(pools_balances):
                                if pool_balances[-1] == name:
                                    pool_balances[1] = pool_balances[1] - amount_A
                                    pool_balances[0] = pool_balances[0] - amount_B
                                    pools_balances[s] = pool_balances
                elif (func == 'swapExactTokensForTokens' or func == 'swapExactTokensForETH' or func == 'swapExactETHForTokens'):
                    for i in range(len(path) - 1):
                        tok1 = path[i]
                        tok2 = path[i+1]
                        b = True
                        for pool in pools:
                            if (pool[0] == tok1 and pool[2] == tok2):
                                b = False
                                name = pool[4]
                                for s, pool_balances in enumerate(pools_balances):
                                    if pool_balances[-1] == name:
                                        pool_balances[0] = new_b(amount_A, pool_balances[0], fee)
                                        pool_balances[1] = new_a(amount_A, pool_balances[1], pool_balances[0], fee)
                                        amount_A = output(amount_A, pool_balances[1], pool_balances[0], fee)
                                        pools_balances[s] = pool_balances
                            elif (pool[2] == tok1 and pool[0] == tok2):
                                b = False
                                name = pool[4]
                                for s, pool_balances in enumerate(pools_balances):
                                    if pool_balances[-1] == name:
                                        pool_balances[1] = new_b(amount_A, pool_balances[1], fee)
                                        pool_balances[0] = new_a(amount_A, pool_balances[0], pool_balances[1], fee)
                                        amount_A = output(amount_A, pool_balances[0], pool_balances[1], fee)
                                        pools_balances[s] = pool_balances
                        if b:
                            break
                elif (func == 'swapTokensForExactETH' or func == 'swapTokensForExactTokens' or func == 'swapETHForExactTokens'):
                    for i in range(len(path) - 1):
                        tok1 = (path[::-1])[i+1]
                        tok2 = (path[::-1])[i]
                        b = True
                        for pool in pools:
                            if (pool[0] == tok1 and pool[2] == tok2):
                                b = False
                                name = pool[4]
                                for s, pool_balances in enumerate(pools_balances):
                                    if pool_balances[-1] == name:
                                        pool_balances[0] = pool_balances[0] + pool_balances[0] * amount_B / (pool_balances[1] - amount_out)
                                        pool_balances[1] = pool_balances[1] - amount_B
                                        amount_B = pool_balances[0] * amount_B / (fee * (pool_balances[1] - amount_B))
                                        pools_balances[s] = pool_balances
                            elif (pool[2] == tok1 and pool[0] == tok2):
                                b = False
                                name = pool[4]
                                for s, pool_balances in enumerate(pools_balances):
                                    if pool_balances[-1] == name:
                                        pool_balances[1] = pool_balances[1] + pool_balances[1] * amount_B / (pool_balances[0] - amount_out)
                                        pool_balances[0] = pool_balances[0] - amount_B
                                        amount_B = pool_balances[1] * amount_B / (fee * (pool_balances[0] - amount_B))
                                        pools_balances[s] = pool_balances
                        if b:
                            break
        with open('new_balances', 'wb') as fp:
            pickle.dump(pools_balances, fp)
    except Exception as e:
        print(e)
    time.sleep(0.5)

