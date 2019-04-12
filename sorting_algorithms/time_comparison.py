# Use the three methods we created and import time to compare how long each takes
from numpy.random import randint
import time

def bubble_sort(arr):
    start = time.time()
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

    end = time.time()
    return arr, end-start

def selection_sort(array):
    start = time.time()
    # loop through the entire array
    for index in range(len(array)):
        # set the first number we see as the minimum (because it IS the lowest number we have seen thus far)
        minimum = index

        # begin the sorting logic
        # grab another index, after the current index, but not more than is in the array
        for next_index in range(index + 1, len(array)):
            # if this new index is lower than the already set minimum
            if array[next_index] < array[minimum]:
                # then make this new number the new minimum
                minimum = next_index

        # with the actual minimum set from iterating through the entire array, create a new array and place the minimum in the front
        array[minimum], array[index] = array[index], array[minimum]
    end = time.time()
    return array, end-start

def insertion_sort(array):
    start = time.time()

    # for an index in the total length of the array
    for index in range(len(array)):
        # grab the current number and store it
        current_number = array[index]
        # grab the current index and store it
        current_position = index

        # loop through and keep going as long as the current index position is greater than 0
        # and if the current number is LESS than the number before it
        while current_position > 0 and array[current_position - 1] > current_number:
            # move the number down an index towards the beginning of the list
            array[current_position] = array[current_position - 1]
            # decrement the current position index
            current_position = current_position - 1
        # break the while loop for the final swap
        array[current_position] = current_number

    end = time.time()
    return array, end-start

# let's create an array to test the sorting
# randint(min_value, max_value, size_of_array)
# so here we generate a list of 200 values between 0 and 1000


for i in range(5):
    # load up 2000 random integers from 0 - 10000
    array = randint(0, 10000, 2000)
    print('=============================================================')
    print("\nSorted with Bubble Sort: Time required %10.7f seconds \n"%bubble_sort(array)[1])
    print("Sorted with Selection Sort: Time required %10.7f seconds \n"%selection_sort(array)[1])
    print("Sorted with Insertion Sort: Time required %10.7f seconds \n"%insertion_sort(array)[1])