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
    
    max_length = longest_str(map(str, arr)) + 5
    cursor = 0
    print('\t[\n\t', end='')
    while cursor < len(arr):
        print(cjust(str(arr[cursor]), max_length), end=' ')
        cursor += 1
        if cursor % cols == 0:
            print('\n\t', end='')
    print(']\n')

def get_random_arr(n, min=0, max=1000):
    if not isinstance(n, int):
        message = 'Attempted to create an array with \'{}\' length.\nN must be an integer value'.format(n)
        raise ValueError(message)
    elif n < 0:
        raise ValueError("Attempted to create an array with length {}.\nN cannot be a negative number".format(n))
    
    return list(map(lambda x: random.randrange(min, max), range(n)))

def spawn_and_sort(input_arr, tinput, debug_setting=False):
    N = len(input_arr)
    T = tinput
    debugOn = debug_setting
    lib_filepath = "./csort.so"

    csort = ctypes.CDLL(lib_filepath)

    try:
        pyarr = np.array(input_arr, dtype=float)
    except Exception as e:
        print(e)

    sorted_arr = pyarr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    pyarr = list(copy.deepcopy(pyarr))

    csort.spawnAndSort.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, POINTER(ctypes.c_double)]
    csort.spawnAndSort(N, T, debugOn, sorted_arr)

    sorted_arr = [sorted_arr[i] for i in range(N)]

    return sorted_arr

def main():
    MIN, MAX = 0, 10
    N = 100
    T = 2
    debugOn = False
    lib_filepath = "./csort.so"

    csort = ctypes.CDLL(lib_filepath)

    # csort.spawnAndSortRandom.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
    # csort.spawnAndSortRandom(N, T, debugOn)

    pyarr = np.array(get_random_arr(N, MIN, MAX), dtype=float)
    arr = pyarr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    pyarr = list(copy.deepcopy(pyarr))

    csort.spawnAndSort.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, POINTER(ctypes.c_double)]
    csort.spawnAndSort(N, T, debugOn, arr)

    arr = [arr[i] for i in range(N)]

    col_print(pyarr, cols=5)
    col_print(arr, cols=5)

if __name__ == '__main__':
    main()
