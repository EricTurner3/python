# Selection Sort 
# Description: Selection Sort is simple but usually outperforms bubble sort as it divides the sorted list into a separate array to increase efficiency
from numpy.random import randint


def selection_sort(array):
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

    return array


# let's create an array to test the sorting
# randint(min_value, max_value, size_of_array)
# so here we generate a list of 200 values between 0 and 1000
array = randint(0, 1000, 200)
print("Unsorted Array: ")
print(array)
print("Sorted with Selection Sort: ")
print(selection_sort(array))
