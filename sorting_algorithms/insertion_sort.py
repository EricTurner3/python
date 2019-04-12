# Insertion Sort
# Description: Insertion Sort is similar to how people sort cards in their hands, you take an element, pop it from the array and move it to the place it needs to go
from numpy.random import randint


def insertion_sort(array):
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

    return array

# let's create an array to test the sorting
# randint(min_value, max_value, size_of_array)
# so here we generate a list of 200 values between 0 and 1000
array = randint(0, 1000, 200)
print("Unsorted Array: ")
print(array)
print("Sorted with Insertion Sort: ")
print(insertion_sort(array))
