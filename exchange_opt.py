import numpy as np
from scipy import optimize
from scipy.optimize import LinearConstraint
import time
import copy

start_time = time.time()

fee = 0.997

def output(x, a, b, fee):
    return fee * a * x / (b + fee * x)

def new_a(x,a,b,fee):
    return a - output(x,a,b,fee)

def new_b(x, b, fee):
    return b + x * fee

def path_of_n(x, p, fee):
    n = len(p)
    out = x
    for i in range(n):
        b, a = balances_copy[p[i]]
        A = new_a(out, a, b, fee)
        B = new_b(out, b, fee)
        out = output(out, a, b, fee)
        balances_copy[p[i]] = B, A
    return out - x


def opt_func(x, p, fee):
    profit = 0
    n = len(x)
    for i in range(n):
        profit += path_of_n(x[i], p[i], fee)
    for key in balances_copy.keys():
        balances_copy[key] = balances.copy()[key]
    return -profit

balances = {'a': (500, 2000),                    # bk--wh
            'b': (400, 1000),                    # wh--bl
            'c': (100, 1000),                    # bl--bk
            'd': (100, 110),                     # wh--r
            'e': (220, 100),                     # r--bk
            'f': (700, 800),                     # wh--gr
            'g': (400, 50),                      # gr--bk
            'h': (107, 140),                     #
            'i': (27, 75)}                       #

balances_copy = balances.copy()
paths = [['a', 'b', 'c'],
         ['a', 'd', 'e'],
         ['a', 'f', 'g'],
         ['b', 'i', 'd']]

path_combinations = []
vals = []
xs = []

Sol = optimize.minimize(opt_func, 10*np.ones(4), args=([paths[0], paths[3], paths[1], paths[3]], fee),
            bounds=((0, None), (0, None), (0, None), (0, None)))
print(Sol)
# print(Sol.success)
# for i1, path1 in enumerate(paths):
#     paths1 = copy.deepcopy(paths)
#     paths1.remove(path1)
#     for i2, path2 in enumerate(paths1):
#         paths2 = copy.deepcopy(paths1)
#         paths2.remove(path2)
#         for i3, path3 in enumerate(paths2):
#             paths3 = copy.deepcopy(paths2)
#             paths3.remove(path3)
#             for i4, path4 in enumerate(paths3):
#                 # print([path1, path2, path3, path4])
#                 path_combinations.append([path1, path2, path3, path4])
#                 c = optimize.minimize(opt_func, 20 * np.ones(4), args=([path1, path2, path3, path4], fee),
#                                       bounds=((0, None), (0, None), (0, None), (0, None)))
#                 # print(path_combinations[-1])
#                 xs.append(c.x)
#                 vals.append(c.fun)
# ind = vals.index(min(vals))
# print('path', path_combinations[ind])
# print('x', xs[ind])
# print('val', vals[ind])
# print("--- %s seconds ---" % (time.time() - start_time))
