# This function takes last element as pivot, places 
# the pivot element at its correct position in sorted 
# array, and places all smaller (smaller than pivot) 
# to left of pivot and all greater elements to right 
# of pivot 
def partition(arr,low,high, comparator): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        if   comparator(arr[j], pivot)==-1 or comparator(arr[j], pivot)==0: 
          
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 
  
# The main function that implements QuickSort 
# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 
  
# Function to do Quick sort 
def quickSort(arr,low,high, comparator): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high,comparator) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1, comparator) 
        quickSort(arr, pi+1, high, comparator) 

def wordBoxCompare(word1, word2):
    if word1.bounding_box.vertices[4]<word2.bounding_box.vertices[4]:
        return -1

    if word1.bounding_box.vertices[4]>word2.bounding_box.vertices[4]:
        return 1

    else:
        return 0

def wordBoxSort(words):
    quickSort(words, 0, len(words)-1, wordBoxCompare)