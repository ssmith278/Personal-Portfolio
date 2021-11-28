from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
import os
from .static.multithread_sort.run_csort import get_random_arr, spawn_and_sort

# TODO: Add a form field for setting the length, threads, min, and max values of the array. 
# Create your views here.
def index(request):

    if request.method == 'POST':
        request.session['data'] = request.POST
        return HttpResponseRedirect('/projects/')

    return render(request, 'projects.html')

def sorter_chart(request):

    LENGTH_NAME = 'length'
    NUM_THREADS_NAME = 'num_threads'
    MIN_VALUE_NAME = 'min_value'
    MAX_VALUE_NAME = 'max_value'
    UNSORTED_DATA_NAME = 'unsorted_data'
    SORTED_DATA_NAME = 'sorted_data'

    default_length = 50
    default_num_threads = 2
    default_min_value = 0
    default_max_value = 1000

    data = request.session.get('data', {})

    # First check posts, then sessions, and use default if none found
    length = int(request.POST.get(LENGTH_NAME, data.get(LENGTH_NAME, default_length)))
    num_threads = int(request.POST.get(NUM_THREADS_NAME, data.get(NUM_THREADS_NAME, default_num_threads)))
    min_value = float(request.POST.get(MIN_VALUE_NAME, data.get(MIN_VALUE_NAME, default_min_value)))
    max_value = float(request.POST.get(MAX_VALUE_NAME, data.get(MAX_VALUE_NAME, default_max_value)))

    # Validate num_threads value
    # assert (length and num_threads and length%num_threads==0), 'N must be divisible by number of threads'
    
    data = request.session.get('data', {})

    if not (data.get(UNSORTED_DATA_NAME) and data.get(SORTED_DATA_NAME)):        
        _set_data(request, length, min_value, max_value, num_threads)

    return JsonResponse(data = request.session['data'])

def _set_data(request, length, min_value, max_value, num_threads):
    module_dir = os.path.dirname(__file__)
    csort_filepath = os.path.join(module_dir, 'static/multithread_sort/csort.so')
    unsorted_data = get_random_arr(length, min=min_value, max=max_value)
    sorted_data = spawn_and_sort(unsorted_data, num_threads, debug_setting=False, lib_filepath=csort_filepath)

    request.session['data'] = {
        'length': length,
        'min_value': min_value,
        'max_value': max_value,
        'num_threads': num_threads,
        'unsorted_data': unsorted_data,
        'sorted_data': sorted_data,
    }