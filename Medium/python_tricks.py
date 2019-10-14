# From https://towardsdatascience.com/python-tricks-101-what-every-new-programmer-should-know-c512a9787022
# I went through and more heavily notated what was outlined in the article

#*#*#*#*#*#*#*#*#*#*#*#*#*#
# 1 - String Manipulation
#*#*#*#*#*#*#*#*#*#*#*#*#*#

my_string = "This is a test"

# you can multiply the string to make several copies of it, i.e
print(my_string * 2) # This is a testThis is a test

# use + to concatenate
print(my_string + " I love Python" * 2) # This is a test I love Python I love Python

# use [::-1] to reverse strings 
print(my_string[::-1]) # tset a si sihT

# ... or reverse lists
my_list = [1,2,3,4,5]
print(my_list[::-1]) # [5, 4, 3, 2, 1]

# ... or even arrays of words (join each word with a space then add a !)
word_list = ["awesome", "is", "this"]
print(' '.join(word_list[::-1]) + '!') # this is awesome!

#*#*#*#*#*#*#*#*#*#*#*#*#*#
# 2 - List Conditionals
#*#*#*#*#*#*#*#*#*#*#*#*#*#

# list comprenhension follows this syntax: [ expression for item in list if conditional ]
# here's a function that will take a number and multiply by 2 then add 5
def our_algorithm(x):
     return x**2 + 5
# if we want to do that to every item in the list, we do it with a list conditional
    #  expression - we want every item to be passed through our function
    #     for
    #  item - use a placeholder variable for each iteration, x or i .etc
    #     in
    #  list - our array (defined up above) 
    #     if (optional conditional statement)
    #  conditional - ex. we only want to apply the expression to ODD numbers
print([our_algorithm(x) for x in my_list if x % 2 != 0]) # [6, 14, 30]

# if the function is super simple (like the one liner above) you can just place that right in the conditional, ex.
print([x ** 2 + 5 for x in my_list if x % 2 != 0]) # [6, 14, 30]

#*#*#*#*#*#*#*#*#*#*#*#*#*#
# 3 - Lambda & Map
#*#*#*#*#*#*#*#*#*#*#*#*#*#

# lambdas are used for doing small / simple operations like a simple function would do

my_list = [2, 1, 0, -1, -2]

# by default, sorted sorts from least to greatest
print(sorted(my_list)) #[-2, -1, 0, 1, 2]

# by using lambda, we can use another argument to change how sorted sorts its items
# in this case, we order by least to greatest if all of the items were squared
print(sorted(my_list, key = lambda x : x ** 2))

# using map, we can apply a function that interacts with multiple lists
# let's break this down: 
    # in the map() function, we have several arguments:
        # the lambda (how we want to manipulate the lists)
        # arguments 2 and 3 are the lists
    # in this case, we are taking an item from the first list (x) and an item from the second list (y) and multiplying them together
    # once we get our results, we wrap it in list() so it retuns back to us as a list
    # our result is essentally [(1 * 4), (2 * 5), (3 * 6)] and lambda just does all the math for us
print(list(map(lambda x, y : x * y, [1, 2, 3], [4, 5, 6]))) # [4, 10, 18]

#*#*#*#*#*#*#*#*#*#*#*#*#*#
# 4 - if, elif, and else one-liners
#*#*#*#*#*#*#*#*#*#*#*#*#*#

# instead of having a multi-line if / elif / else conditional, it can be simplified to just one line
    # this will print:
        # "Horse" if x is greater than / equal to 10
        # "Duck" if x is between 1 and 10 (exclusive)
        # "Baguette" if x is less than / equal to 1
x = int(input())
print("Horse" if x >= 10 else "Duck" if 1 < x < 10 else "Baguette")

#*#*#*#*#*#*#*#*#*#*#*#*#*#
# 5 -  zip()
#*#*#*#*#*#*#*#*#*#*#*#*#*#

# for use when we need to merge two lists together
first_names = ["Eric", "Christian", "Peter"]
last_names = ["Nistrup", "Smith", "Turner"]
# this will print them out as strings
print([' '.join(x) for x in zip(first_names, last_names)]) # ['Eric Nistrup', 'Christian Smith', 'Peter Turner']
# you can still apply something like a modifier to an array (like [::-1])
print([' '.join(x) for x in zip(first_names, last_names[::-1])]) # ['Eric Turner', 'Christian Smith', 'Peter Nistrup']
# and enclose in list() to convert them to a list
list([' '.join(x) for x in zip(first_names, last_names[::-1])]) # ['Eric Turner', 'Christian Smith', 'Peter Nistrup'] (doesn't print to console)