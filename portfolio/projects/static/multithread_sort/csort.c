#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void parseArgs(int argc, char *argv[], int *n, int *t, int *debugOn);
void spawnAndSortRandom(int n, int t, int debugOn);
void spawnAndSort(int n, int t, int debugOn, double *dArr);
void getUnsortedArray(int n, double *pArr);
void *sortArray(void *arg);
void *mergeArrays(void *arg);
void printArray(int n, double *pArr);

#define DEBUG 1

typedef struct Sortable{

    int n;
    double *dArr;
} Sortable;

typedef struct Mergable{

    int t;
    Sortable *sorts;
} Mergable;

/*
 *  Takes an integer and creates an unsorted array with random double values. 
 *  Then splits the array into T subarrays and hands them to separate threads to sort
 *  using insertion sort. T is 1 by default but can be set by inputting a second integer
 *  command line argument
 */
int main(int argc, char *argv[])
{
    int *n = (int*)malloc(sizeof(int));
    int *t = (int*)malloc(sizeof(int));
    int *debugOn = (int*)malloc(sizeof(int));

    parseArgs(argc, argv, n, t, debugOn);

    if(*debugOn)
    {

        printf("Running with the following values: \n\tN: %d \n\tT: %d \n", *n, *t);
    }

    spawnAndSortRandom(*n, *t, *debugOn);

    free(n);
    free(t);
    free(debugOn);
    exit(EXIT_SUCCESS);
}

void parseArgs(int argc, char *argv[], int *n, int *t, int *debugOn)
{
    if (argc > 3)
    {
        *debugOn = atoi(argv[3]);
    }

    if (argc > 2)
    {
        *n = atoi(argv[1]);
        *t = atoi(argv[2]);
    }
    else if (argc > 1)
    {
        fprintf(stderr, "No second argument provided. T will default to 1 thread.\n");
        *n = atoi(argv[1]);        
        *t = 1;
    }
    else
    {
        fprintf(stderr, "No arguments provided.\nUsage: csort <list length> [number of threads]\n");
        exit(EXIT_FAILURE);    
    }

    if(*t == 0 || *n % *t != 0)
    {
        fprintf(stderr, "Invalid N/T combination: %d/%d.\n"
                "Please enter a combination where T is NOT 0 and N is divisible by T\n",
                *n, *t);
        exit(EXIT_FAILURE);
    }
}

void spawnAndSortRandom(int n, int t, int debugOn)
{    
    Sortable *arr = (Sortable*)malloc(sizeof(Sortable));

    if(arr == NULL)
    {
        fprintf(stderr, "Failed to malloc Sortable");
        exit(EXIT_FAILURE);
    }    
    arr->dArr = (double*)malloc(sizeof(double)*n);
    if(arr->dArr == NULL)
    {
        fprintf(stderr, "Failed to malloc dArray");
        exit(EXIT_FAILURE);
    }
    arr->n = n;
 
    getUnsortedArray(n, arr->dArr);

    spawnAndSort(n, t, debugOn, arr->dArr);

    free(arr->dArr);
    free(arr);  
}

void spawnAndSort(int n, int t, int debugOn, double *dArr)
{    
    int i;
    struct timespec start, end;
    double elapsed;
    
    if(debugOn)
    {
        printf("Unsorted array: \n");
        printArray(n, dArr);
    }

    //Split the arrays
    Sortable slices[t];
    for(i = 0; i < t; i++)
    {
        slices[i].n = n/t;
        slices[i].dArr = dArr+(n/t)*i;
    }

    //Time the sorting
    clock_gettime(CLOCK_MONOTONIC, &start);

    //Sort array slices
    pthread_t tid[t];
    for(i = 0; i < t; i++)
    {
        pthread_create(&tid[i], NULL, sortArray, (void*)&slices[i]);
    }

    for(i = 0; i < t; i++)
    {
        pthread_join(tid[i], NULL);
    }
    
    //Merge array slices
    Mergable mArr = { t, slices };
    Sortable *result; 
    pthread_t mtid;
    pthread_create(&mtid, NULL, mergeArrays, (void*)&mArr);
    pthread_join(mtid, (void**)&result);
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    
    for(i = 0; i < n; i++)
    {
        dArr[i] = result->dArr[i];
    }

    if(debugOn)
    {
        printf("Sorted array: \n");
        printArray(n, dArr);
        
        elapsed = (end.tv_sec - start.tv_sec) * 1000.0;
        elapsed += (end.tv_nsec - start.tv_nsec) / 1000000.0;
        printf("\nExecution time: %f ms\n", elapsed);
    }

    free(result->dArr);
    free(result);
}

void getUnsortedArray(int n, double *pArr)
{
    double min = 1.0;
    double max = 1000.0;
    int i;

    double range = max - min;
    double div = RAND_MAX / range;
    
    srand(time(0));
    for(i = 0; i < n; i++)
    {        
        pArr[i] = (rand() / div) + min;
    }
}

void *sortArray(void *arg)
{
    Sortable *tmpArr = (Sortable*)arg;
    double *dArr = tmpArr->dArr;

    //Insertion Sort
    int i, j;
    double k;
    for(i = 1; i < tmpArr->n; i++)
    {
        k = dArr[i];
        j = i-1;

        while(j >= 0 && dArr[j] > k)
        {
            dArr[j+1] = dArr[j];
            j = j-1;
        }
        dArr[j+1] = k;
    }    

    return NULL;
}


void *mergeArrays(void *arg)
{
    Mergable *mArr = (Mergable*)arg;
    int t = mArr->t;
    Sortable *slices = mArr->sorts;
    int n = slices[0].n;

    int i;
    int totalN = t*n;
    int resultIdx = 0;
    int currentIdx[t];

    for(i = 0; i < t; i++)
    {
        currentIdx[i] = 0;
    }

    Sortable *result = (Sortable*)malloc(sizeof(Sortable));
    result->dArr = (double *)malloc(sizeof(double) * totalN);
    double *dArr = result->dArr;

    while(resultIdx < totalN)
    {
        int minSlice = -1;
        
        //Loop through slices
        for(i = 0; i < t; i++)
        {
            //Get slice idx for min element
            if(currentIdx[i] < n)
            {
                if(minSlice < 0) minSlice = i;
                if(slices[i].dArr[currentIdx[i]] < slices[minSlice].dArr[currentIdx[minSlice]])
                {
                    minSlice = i;
                }
            }
        }
        // Add minimum element to new array
        dArr[resultIdx] = slices[minSlice].dArr[currentIdx[minSlice]];
        currentIdx[minSlice]++;
        resultIdx++;       
    }

    return (void*)result;
}

void printArray(int n, double *pArr)
{
    int i;
    
    for(i = 0; i < n; i++)
    {
        if(i != 0 && i%4 == 0)
        {
            printf("\n");
        }    
        if(i ==0)
        {
            printf("\t[");
        }
        else
        {
            printf("\t");
        }

        printf("%06.3f", pArr[i]);
       
        if(i == n-1)
        {
            printf("]\n");
        }
        else
        {
            printf(", ");
        }
    }
}
