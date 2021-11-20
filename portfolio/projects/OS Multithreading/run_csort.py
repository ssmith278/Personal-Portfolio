import copy
import ctypes
from ctypes import POINTER
import numpy as np
import random

def cjust(line, linewidth):
    return line.rjust((len(line)) + (linewidth - len(line) + 1)//2)

def longest_str(arr):
    return max(map(len, arr))

def col_print(arr, cols):
    
    max_length = longest_str(map(str, arr))
    cursor = 0
    print('[')
    while cursor < len(arr):
        print(cjust(str(arr[cursor]), max_length), end=' ')
        cursor += 1
        if cursor % cols == 0:
            print('\n')
    print(']\n')

def main():
    MIN, MAX = 0, 10
    N = 100
    T = 2
    debugOn = True
    lib_filepath = "./csort.so"

    csort = ctypes.CDLL(lib_filepath)

    # csort.spawnAndSortRandom.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
    # csort.spawnAndSortRandom(N, T, debugOn)

    pyarr = np.array([choice for choice in map(lambda x: random.randrange(MIN, MAX), range(N))], dtype=float)
    arr = pyarr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    pyarr = list(copy.deepcopy(pyarr))

    csort.spawnAndSort.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, POINTER(ctypes.c_double)]
    csort.spawnAndSort(N, T, debugOn, arr)

    arr = [arr[i] for i in range(N)]

    col_print(pyarr, cols=5)
    col_print(arr, cols=5)

if __name__ == '__main__':
    main()
