import copy
import ctypes
from ctypes import POINTER
import numpy as np
import random
import timeit

def longest_str(arr):
    return max(map(len, arr))

def col_print(arr, cols=5, padding=5, sep=','):
    
    format_func = lambda x: ('%0.3f' % x)
    result = []
    max_length = longest_str(map(format_func, arr)) + padding
    cursor = 0
    
    result.append('[')
    result.append([''])
    while cursor < len(arr):
        result[-1] += (format_func(arr[cursor]) + sep).rjust(max_length)
        cursor += 1
        if cursor % cols == 0:
            # Remove extra separator
            if sep:
                result[-1] = result[-1][:-len(sep)]
                
            result.append([''])
    result.append(']')

    return [''.join(line) for line in result]

def get_random_arr(n, min=0, max=1000):
    if not isinstance(n, int):
        message = 'Attempted to create an array with \'{}\' length.\nN must be an integer value'.format(n)
        raise ValueError(message)
    elif n < 0:
        raise ValueError("Attempted to create an array with length {}.\nN cannot be a negative number".format(n))
    
    return list(map(lambda x: round(random.random()*(max-min)+min, 3), range(n)))

def spawn_and_sort(input_arr, num_threads, debug_setting=False, lib_filepath='csort.so'):
    N = len(input_arr)
    T = num_threads
    debugOn = debug_setting

    csort = ctypes.CDLL(lib_filepath)

    pyarr = np.array(input_arr, dtype=float)
    sorted_arr = pyarr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    pyarr = list(copy.deepcopy(pyarr))

    csort.spawnAndSort.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, POINTER(ctypes.c_double)]
    csort.spawnAndSort(N, T, debugOn, sorted_arr)

    sorted_arr = [sorted_arr[i] for i in range(N)]

    return sorted_arr

def compare():
    MIN, MAX = 0, 10
    N = 100
    T = 2
    
    repeat = 3
    iterations = 1000

    setup = '''
gc.enable()
import copy
import ctypes
from ctypes import POINTER
import numpy as np
from run_csort import spawn_and_sort, get_random_arr
lib_filepath = './csort.so'

N = 100000
T = 20

test_arr = get_random_arr(N)

csort = ctypes.CDLL(lib_filepath)

pyarr = np.array(test_arr, dtype=float)
sorted_arr = pyarr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

pyarr = list(copy.deepcopy(pyarr))

csort.spawnAndSort.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, POINTER(ctypes.c_double)]
'''

    csort_result = timeit.timeit('csort.spawnAndSort(N, T, False, sorted_arr)', setup=setup, number=iterations)

    pysort_result = timeit.timeit('sorted(test_arr)', setup=setup, number=iterations)

    print('CSort time: %s'%(csort_result))
    print('PySort time: %s'%(pysort_result))

def main():
    pass

if __name__ == '__main__':
    main()
