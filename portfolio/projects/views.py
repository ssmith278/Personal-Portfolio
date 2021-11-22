from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
import os
from .static.multithread_sort.run_csort import get_random_arr, spawn_and_sort

# Create your views here.
def index(request):

    if (request.POST.get('reset') and request.session.get('data', None)):
        request.session['data'] = []
        request.session.modified = True
        return HttpResponseRedirect('/projects/')

    return render(request, 'projects.html')

def sorter_chart(request):
    if not request.session.get('data', None):

        module_dir = os.path.dirname(__file__)
        csort_filepath = os.path.join(module_dir, 'static/multithread_sort/csort.so')

        unsorted_data = get_random_arr(50)
        sorted_data = spawn_and_sort(unsorted_data, 2, debug_setting=False, lib_filepath=csort_filepath)
        request.session['data'] = {
            'unsorted_data': unsorted_data,
            'sorted_data': sorted_data,
        }
    else:
        sorter_data = request.session['data']
        unsorted_data = sorter_data.get('unsorted_data')
        sorted_data = sorter_data.get('sorted_data')

    return JsonResponse(data={
        'unsorted_data': unsorted_data,
        'sorted_data': sorted_data,
    })
