# Bubble Sort
# Purpose: Steps through the array and compares adjacent pairs of elements. Elements are swapped if they are in the wrong order.
# Issues: Slowest Sorting Algorithm and it will loop through the array several times to ensure completion. With longer arrays, this becomes problematic
from numpy.random import randint

def bubble_sort(arr):
    # The swapping function
    def swap(index1, index2):
        # this one line re-assigns index1 to index 2 and vice versa
        arr[index1], arr[index2] = arr[index2], arr[index1]

    # grab the length of the array for iterating below
    arr_length = len(arr)
    # place holder to trigger the while loop for the first time
    swapped = True
    
    #start out with a placeholder -1 for the index
    x = -1
    while swapped: 
        # set False to prevent an endless loop once we are done swapping
        swapped = False
        # for every iteration, skip the already swapped index
        x = x+1
        # for all the indexes from the first through array length
        for index in range(1, arr_length-x):
            # if the previous index is larger than the current index
            if arr[index - 1] > arr[index]:
                # call the swap function to swap them
                swap(index-1, index)
                # return true to re trigger the swapped loop
                swapped = True

    return arr


# let's create an array to test the sorting
# randint(minvalue, maxvalue, size of array)
# so here we generate a list of 200 values between 0 and 1000
array = randint(0, 1000, 200)
print("Unsorted Array: ")
print(array)
print("Sorted with Bubble Sort: ")
print(bubble_sort(array))