import matplotlib.pyplot as plt
import numpy as np
from binance.client import Client
from time import sleep
# in all functions below pools come in form
# pools=[
# [add_tok_10, add_tok_11, add_pair_1],
# [add_tok_20, add_tok_21, add_pair_2],
# ...
# [add_tok_n0, add_tok_n1, add_pair_n]]
#
# balances in form
# balances = {
# add_pair_1: [bal_tok10, bal_tok11],
# add_pair_2: [bal_tok20, bal_tok21],
# ...
# add_pair_n: [bal_tokn0, bal_tokn1]}
#
#
# stock_data has a form [factory address, factory abi, pair_abi]


def pools_and_bals(provider, stock_data):
    factory_contract = provider.eth.contract(address=stock_data[0], abi=stock_data[1])
    N = factory_contract.caller.allPairsLength()
    print(N)
    pair_abi = stock_data[2]
    pools = []
    balances = {}
    for i in range(N):
        print(i)
        try:
            add_contr_fac = factory_contract.caller.allPairs(i)
            contract_pool = provider.eth.contract(address=add_contr_fac, abi=pair_abi)
            contract_token0 = provider.eth.contract(address=contract_pool.caller.token0(), abi=pair_abi)
            contract_token1 = provider.eth.contract(address=contract_pool.caller.token1(), abi=pair_abi)
            dec1 = contract_token0.caller.decimals()
            dec2 = contract_token1.caller.decimals()
            res = contract_pool.caller.getReserves()
            am1 = res[0] / 10 ** (dec1)
            am2 = res[1] / 10 ** (dec2)
            pools.append([contract_pool.caller.token0(), contract_pool.caller.token1(), add_contr_fac])
            balances.update({add_contr_fac:[am1, am2]})
        except Exception as e:
            print(e)
    return pools, balances


def real_pools(pools, balances, threshold):
    # if len(pools) != len(balances):
    #     raise ValueError ("Number of pools and balances must be the same")
    # else:
    m = 0
    while m < len(pools):
        pool = pools[m]
        if (balances[pool[2]])[0] < threshold or (balances[pool[2]])[1] < threshold:
            balances.pop(pool[2])
            pools.pop(m)
        else:
            m += 1
    return pools, balances


def pool_liquidities(pools, balances, tok_add="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"):
    # if len(pools) != len(balances):
    #     raise ValueError ("Number of pools and balances must be the same")
    # else:
        # USDC_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    liquidities = dict()
    courses = dict()
    courses.update({tok_add: 1})
    l1 = 0
    l2 = 1
    while l1 != l2:
        l1 = l2
        for m in range(len(pools)):
            pool = pools[m]
            keys = list(courses.keys())
            if keys.count(pool[0]) == 1:
                if keys.count(pool[1]) == 0:
                    courses.update({pool[1]: courses[pool[0]] * balances[pool[2]][0] / balances[pool[2]][1]})
                    l2 += 1
                liquidities.update({pool[2]: 2 * courses[pool[0]] * balances[pool[2]][0]})
            elif keys.count(pool[1]) == 1:
                courses.update({pool[0]: courses[pool[1]] * balances[pool[2]][1] / balances[pool[2]][0]})
                liquidities.update({pool[2]: 2 * courses[pool[1]] * balances[pool[2]][1]})
                l2 += 1
    return liquidities, courses


def path_liquidities(paths, liquidities): # paths as paths_pairs, not _toks
    path_liqs = {}
    for path in paths:
        S = 0
        for pool in path:
            S += 1 / liquidities[pool]
        path_liqs.update({tuple(path):1 / S})
    return path_liqs


def big_pools(pools, liquidities, threshold):
    # if len(pools) != len(liquidities):
    #     raise ValueError("Number of pools and balances must be the same")
    # else:
    m = 0
    while m < len(pools):
        try:
            pool = pools[m]
            if liquidities[pool[2]] < threshold:
                pools.pop(m)
            else:
                m += 1
        except:
            pools.pop(m)
    return pools


def big_paths(paths, path_liquidities, threshold):
    m = 0
    while m < len(paths):
        path = paths[m]
        if path_liquidities[tuple(path)] < threshold:
            paths.pop(m)
        else:
            m += 1
    return paths


def pools_connected_to_usd(pools, toks=["0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"]):
    coins = set(toks)
    l = 0
    while l < len(coins):
        l = len(coins)
        for pool in pools:
            if len(coins.intersection(pool)) == 1:
                if pool[0] in coins:
                    coins.add(pool[1])
                elif pool[1] in coins:
                    coins.add(pool[0])
                else:
                    raise ValueError("Some nonsense, structure of pools is not what it is supposed to be")
    l = 0
    while l < len(pools):
        pool = pools[l]
        if len(coins.intersection(pool)) == 0:
            pools.pop(l)
        else:
            l += 1
    return pools


def pools_making_paths(pools):
    coins = [pool[0] for pool in pools] + [pool[1] for pool in pools]
    n = 1
    while n > 0:
        n = 0
        m = 0
        while m < len(pools):
            pool = pools[m]
            if coins.count(pool[0]) < 2 or coins.count(pool[1]) < 2:
                pools.pop(m)
                coins.remove(pool[0])
                coins.remove(pool[1])
                n = 1
            else:
                m += 1
    return pools


def connected_pools(pools, toks=["0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"]):
    pools = pools_connected_to_usd(pools, toks)
    pools = pools_making_paths(pools)
    return pools


def paths(pools, N, toks=[]):
    L_p = len(pools)
    paths_toks = []
    paths_pairs = []
    if N == 2:
        if len(toks)>0:
            for i1, pool1 in enumerate(pools):
                for i2 in range(i1 + 1, L_p):
                    pool2 = pools[i2]
                    pairs = pool1[:2] + pool2[:2]
                    if len(set(pairs)) == 2:
                        pairs = set(pairs)
                        if pairs.intersection(toks) != 0:
                            pairs = list(pairs)
                            if pairs[0] in toks:
                                paths_toks.append(pairs + pairs[0:1])
                            else:
                                paths_toks.append(pairs[1:] + pairs)
                            paths_pairs.append([pool1[2], pool2[2]])
        else:
            for i1, pool1 in enumerate(pools):
                for i2 in range(i1 + 1, L_p):
                    pool2 = pools[i2]
                    pairs = pool1[:2] + pool2[:2]
                    if len(set(pairs)) == 2:
                        pairs = list(set(pairs))
                        paths_toks.append(pairs + pairs[0:1])
                        paths_pairs.append([pool1[2], pool2[2]])
    elif N == 3:
        if len(toks) > 0:
            for i1, pool1 in enumerate(pools):
                for i2 in range(i1 + 1, L_p):
                    pool2 = pools[i2]
                    pairs = pool1[:2] + pool2[:2]
                    if len(set(pairs)) == 2:
                        pairs = set(pairs)
                        if pairs.intersection(toks) != 0:
                            pairs = list(pairs)
                            if pairs[0] in toks:
                                paths_toks.append(pairs + pairs[0:1])
                            else:
                                paths_toks.append(pairs[1:] + pairs)
                            paths_pairs.append([pool1[2], pool2[2]])
                    elif len(set(pairs)) == 3:
                        for i3 in range(i2 + 1, L_p):
                            pool3 = pools[i3]
                            tripples = pairs + pool3[:2]
                            if len(set(tripples)) == 3 and max([tripples.count(x) for x in tripples]) == 2:
                                tripples = list(set(tripples))
                                ch = 0
                                for x in tripples:
                                    if x in toks:
                                        path = [x]
                                        ch = 1
                                        break
                                if ch == 1:
                                    tripples.remove(x)
                                    tripples.append(x)
                                    path += tripples
                                    temp_pairs = [pool1, pool2, pool3]
                                    s = 0
                                    while s < 3:
                                        for pool in temp_pairs:
                                            if path[s] in pool and path[s+1] in pool:
                                                temp_pairs.remove(pool)
                                                temp_pairs.append(pool)
                                                s += 1
                                                break
                                    paths_pairs.append([x[2] for x in temp_pairs])
                                    paths_toks.append(path)
        else:
            for i1, pool1 in enumerate(pools):
                for i2 in range(i1 + 1, L_p):
                    pool2 = pools[i2]
                    pairs = pool1[:2] + pool2[:2]
                    if len(set(pairs)) == 2:
                        pairs = list(set(pairs))
                        paths_toks.append(pairs + pairs[0:1])
                        paths_pairs.append([pool1[2], pool2[2]])
                    elif len(set(pairs)) == 3:
                        for i3 in range(i2 + 1, L_p):
                            pool3 = pools[i3]
                            tripples = pairs + pool3[:2]
                            if len(set(tripples)) == 3 and max([tripples.count(x) for x in tripples]) == 2:
                                tripples = list(set(tripples))
                                path = tripples + tripples[0:1]

                                temp_pairs = [pool1, pool2, pool3]
                                s = 0
                                while s < 3:
                                    for pool in temp_pairs:
                                        if path[s] in pool and path[s + 1] in pool:
                                            temp_pairs.remove(pool)
                                            temp_pairs.append(pool)
                                            s += 1
                                            break
                                paths_pairs.append([x[2] for x in temp_pairs])
                                paths_toks.append(path)
    elif N == 4:
        if len(toks) > 0:
            for i1, pool1 in enumerate(pools):
                for i2 in range(i1 + 1, L_p):
                    pool2 = pools[i2]
                    pairs = pool1[:2] + pool2[:2]
                    if len(set(pairs)) == 2:
                        pairs = set(pairs)
                        if pairs.intersection(toks) != 0:
                            pairs = list(pairs)
                            if pairs[0] in toks:
                                paths_toks.append(pairs + pairs[0:1])
                            else:
                                paths_toks.append(pairs[1:] + pairs)
                            paths_pairs.append([pool1[2], pool2[2]])
                    elif len(set(pairs)) == 3:
                        for i3 in range(i2 + 1, L_p):
                            pool3 = pools[i3]
                            tripples = pairs + pool3[:2]
                            if len(set(tripples)) == 3 and max([tripples.count(x) for x in tripples]) == 2:
                                tripples = set(tripples)
                                for x in tripples:
                                    if x in toks:
                                        path = [x]
                                        break
                                tripples = list(tripples)
                                tripples.remove(x)
                                tripples.append(x)
                                path += tripples
                                temp_pairs = [pool1, pool2, pool3]
                                s = 0
                                while s < 3:
                                    for pool in temp_pairs:
                                        if path[s] in pool and path[s + 1] in pool:
                                            temp_pairs.remove(pool)
                                            temp_pairs.append(pool)
                                            s += 1
                                            break
                                paths_pairs.append([x[2] for x in temp_pairs])
                                paths_toks.append(path)
                            elif len(set(tripples)) == 4 and max([tripples.count(x) for x in tripples]) == 2:
                                for i4 in range(i3 + 1, L_p):
                                    pool4 = pools[i4]
                                    fours = tripples + pool4[:2]
                                    if len(set(fours)) == 4 and max([fours.count(x) for x in fours]) == 2:
                                        path_toks = []
                                        path_pairs = [pool1[2]]
                                        pairs = [pool2[2], pool3[2], pool4[2]]
                                        l = len(pairs)
                                        pair = pool1
                                        while l > 0:
                                            for pair2 in pairs:
                                                insct = set(pair2).intersection(pair)
                                                if len(insct) == 1:
                                                    path_toks.append(list(insct)[0])
                                                    path_pairs.append(pair2[2])
                                                    pair = pair2
                                                    pairs.remove(pair2)
                                                    break
                                            l = len(pairs)
                                        last_token = list(set(pair2).intersection(pool1))[0]
                                        path_toks = [last_token] + path_toks
                                        for i, x in enumerate(path_toks):
                                            if x in toks:
                                                path_toks = path_toks[i:] + path_toks[:i] + [x]
                                                path_pairs = path_pairs[i:] + path_pairs[:i]
                                        paths_pairs.append(path_pairs)
                                        paths_toks.append(path_toks)
                    else:
                        for i3 in range(i2 + 1, L_p):
                            pool3 = pools[i3]
                            tripples = pairs + pool3[:2]
                            if len(set(tripples)) == 4 and max([tripples.count(x) for x in tripples]) == 2:
                                for i4 in range(i3 + 1, L_p):
                                    pool4 = pools[i4]
                                    fours = tripples + pool4[:2]
                                    if len(set(fours)) == 4 and max([fours.count(x) for x in fours]) == 2:
                                        path_toks = []
                                        path_pairs = [pool1[2]]
                                        pairs = [pool2[2], pool3[2], pool4[2]]
                                        l = len(pairs)
                                        pair = pool1
                                        while l > 0:
                                            for pair2 in pairs:
                                                insct = set(pair2).intersection(pair)
                                                if len(insct) == 1:
                                                    path_toks.append(list(insct)[0])
                                                    path_pairs.append(pair2[2])
                                                    pair = pair2
                                                    pairs.remove(pair2)
                                                    break
                                            l = len(pairs)
                                        last_token = list(set(pair2).intersection(pool1))[0]
                                        path_toks = [last_token] + path_toks
                                        for i, x in enumerate(path_toks):
                                            if x in toks:
                                                path_toks = path_toks[i:] + path_toks[:i] + [x]
                                                path_pairs = path_pairs[i:] + path_pairs[:i]
                                        paths_pairs.append(path_pairs)
                                        paths_toks.append(path_toks)
        else:
            for i1, pool1 in enumerate(pools):
                for i2 in range(i1 + 1, L_p):
                    pool2 = pools[i2]
                    pairs = pool1[:2] + pool2[:2]
                    if len(set(pairs)) == 2:
                        print("1")
                        pairs = list(set(pairs))
                        paths_toks.append(pairs + pairs[:1])
                        paths_pairs.append([pool1[2], pool2[2]])
                    elif len(set(pairs)) == 3:
                        for i3 in range(i2 + 1, L_p):
                            pool3 = pools[i3]
                            tripples = pairs + pool3[:2]
                            # print("trip", tripples)
                            if len(set(tripples)) == 3 and max([tripples.count(x) for x in tripples]) == 2:
                                print("2")
                                path_toks = []
                                path_pairs = [pool1[2]]
                                temp_pairs = [pool2, pool3]
                                l = len(temp_pairs)
                                pair = pool1
                                while l > 0:
                                    for pair2 in temp_pairs:
                                        insct = set(pair2).intersection(pair)
                                        if len(insct) == 1:
                                            path_toks.append(list(insct)[0])
                                            path_pairs.append(pair2[2])
                                            pair = pair2
                                            temp_pairs.remove(pair2)
                                            break
                                    l = len(temp_pairs)
                                last_token = list(set(pair2).intersection(pool1))[0]
                                path_toks = [last_token] + path_toks + [last_token]
                                paths_pairs.append(path_pairs)
                                paths_toks.append(path_toks)
                            elif len(set(tripples)) == 4 and max([tripples.count(x) for x in tripples]) == 2:
                                for i4 in range(i3 + 1, L_p):
                                    pool4 = pools[i4]
                                    fours = tripples + pool4[:2]
                                    if len(set(fours)) == 4 and max([fours.count(x) for x in fours]) == 2:
                                        print("3")
                                        path_toks = []
                                        path_pairs = [pool1[2]]
                                        temp_pairs = [pool2, pool3, pool4]
                                        l = len(temp_pairs)
                                        pair = pool1
                                        while l > 0:
                                            for pair2 in temp_pairs:
                                                insct = set(pair2).intersection(pair)
                                                if len(insct) == 1:
                                                    path_toks.append(list(insct)[0])
                                                    path_pairs.append(pair2[2])
                                                    pair = pair2
                                                    temp_pairs.remove(pair2)
                                                    break
                                            l = len(temp_pairs)
                                        last_token = list(set(pair2).intersection(pool1))[0]
                                        path_toks = [last_token] + path_toks + [last_token]
                                        paths_pairs.append(path_pairs)
                                        paths_toks.append(path_toks)
                    else:
                        for i3 in range(i2 + 1, L_p):
                            pool3 = pools[i3]
                            tripples = pairs + pool3[:2]
                            if len(set(tripples)) == 4 and max([tripples.count(x) for x in tripples]) == 2:
                                for i4 in range(i3 + 1, L_p):
                                    pool4 = pools[i4]
                                    fours = tripples + pool4[:2]
                                    if len(set(fours)) == 4 and max([fours.count(x) for x in fours]) == 2:
                                        print("4")
                                        path_toks = []
                                        path_pairs = [pool1[2]]
                                        temp_pairs = [pool2, pool3, pool4]
                                        l = len(temp_pairs)
                                        pair = pool1
                                        while l > 0:
                                            for pair2 in temp_pairs:
                                                insct = set(pair2).intersection(pair)
                                                if len(insct) == 1:
                                                    path_toks.append(list(insct)[0])
                                                    path_pairs.append(pair2[2])
                                                    pair = pair2
                                                    temp_pairs.remove(pair2)
                                                    break
                                            l = len(temp_pairs)
                                        last_token = list(set(pair2).intersection(pool1))[0]
                                        path_toks = [last_token] + path_toks + [last_token]
                                        paths_pairs.append(path_pairs)
                                        paths_toks.append(path_toks)
    return paths_toks, paths_pairs

def graph(pools, coeff, liquidities={}, cols={}):
    if len(liquidities) > 0:
        for pool in pools:
            if list(liquidities.keys()).count(pool[2]) == 0:
                raise ValueError("Every pool must have liquidity")
        toks = set([pool[0] for pool in pools] + [pool[1] for pool in pools])
        N = len(toks)
        toks = list(toks)
        coords = dict()
        coin_map = dict()
        for i in range(len(toks)):
            coords.update({toks[i]: [np.cos(2 * np.pi * i / N), np.sin(2 * np.pi * i / N)]})
            coin_map.update({(coords[toks[i]][0], coords[toks[i]][1]): toks[i]})
        plt.figure()
        for x in coin_map:
            plt.text(x[0], x[1], coin_map[x][:3])
        if len(cols) > 0:
            for pool in pools:
                coin1 = pool[0]
                coin2 = pool[1]
                col = cols[pool[3]]
                plt.plot([coords[coin1][0], coords[coin2][0]], [coords[coin1][1], coords[coin2][1]],
                         linewidth=coeff * liquidities[pool] ** 0.4, color=col)
        else:
            for pool in pools:
                coin1 = pool[0]
                coin2 = pool[1]
                plt.plot([coords[coin1][0], coords[coin2][0]], [coords[coin1][1], coords[coin2][1]],
                         linewidth=coeff * liquidities[pool[2]] ** 0.4)
    else:
        toks = set([pool[0] for pool in pools] + [pool[1] for pool in pools])
        print(pools)
        print(toks)
        N = len(toks)
        toks = list(toks)
        coords = dict()
        coin_map = dict()
        for i in range(len(toks)):
            coords.update({toks[i]: [np.cos(2 * np.pi * i / N), np.sin(2 * np.pi * i / N)]})
            coin_map.update({(coords[toks[i]][0], coords[toks[i]][1]): toks[i]})

        plt.figure()
        for x in coin_map:
            plt.text(x[0], x[1], coin_map[x][:4])
        if len(cols) > 0:
            for pool in pools:
                coin1 = pool[0]
                coin2 = pool[1]
                col = cols[pool[3]]
                plt.plot([coords[coin1][0], coords[coin2][0]], [coords[coin1][1], coords[coin2][1]], color=col)
        else:
            for pool in pools:
                coin1 = pool[0]
                coin2 = pool[1]
                plt.plot([coords[coin1][0], coords[coin2][0]], [coords[coin1][1], coords[coin2][1]])
    plt.show()

def course_binance(ticks):
    api_key = ''
    api_secret = ''
    client = Client(api_key, api_secret)
    tickers = client.get_orderbook_tickers()
    binance_price = {}
    for tick in ticks:
        for ticker in tickers:
            if tick in ticker['symbol']:
                binance_price.update({tick:float((ticker['bidPrice']+ticker['bidPrice'])/2)})
    return binance_price
