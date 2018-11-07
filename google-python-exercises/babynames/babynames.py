# Source https://developers.google.com/edu/python/exercises/baby-names?authuser=1

import sys
import re


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    # Open the file and read it
    htmlfile = open(filename, 'r')
    text = htmlfile.read()

    summary = []

    # # # # # # # # # # # # # # # # # # # # # # # #
    # Milestone 1: Extract the year and print it  #
    # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Using regex, this searches for the string 'Popularity in XXXX' and then grabs just the year using a group
    # .group(0) is the whole string
    # The parenthesis around \d\d\d\d create group 1, which can be accessed with .group(1) and returns the year
    year = re.search(r'Popularity\sin\s(\d\d\d\d)', text).group(1)

    summary.append(year)

    # # # # # # # # # # # # # # # # # # # # # # # #
    # Milestone 2: Extract the names and rank #s  #
    # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # My original plan does grab the names, but no way to tell the rank nor boy or girl
    # names = re.findall(r'<td>([a-zA-Z]+)</td>', text)
    # This method grabs the whole string, and in groups sets the rank, boy and then girl name
    tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)

    # Milestone 3: loop through the tuple and package the name + rank
    ranks = {}
    for rank_tuple in tuples:
        (rank, boyname, girlname) = rank_tuple  # unpack the tuple into 3 vars
        # discard duplicate values (if the same name appears another time)
        # the key becomes [eric] = 256, so if the name is called then it returns the rank
        if boyname not in ranks:
            ranks[boyname] = rank
        if girlname not in ranks:
            ranks[girlname] = rank

    # sort the names alphabetically (remember the names are the KEYS and the ranks are the VALUES)
    # so we need to specify the keys in the sorted method
    sorted_names = sorted(ranks.keys())

    # append the names and ranks to the summary
    for name in sorted_names:
        summary.append(name + ' ' + ranks[name])

    return summary


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    # For each filename, get the names, then either print the text output
    # or write it to a summary file
    if not summary:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)
    else:
        for filename in args:
            # Call the function to parse the .HTML File
            results = extract_names(filename)
            # Create the file to export the summary
            results_file = open(filename+".summary", "w+")
            # Turn the dict into text, each index getting its own line
            text = '\n'.join(results)
            # Output the text to file
            results_file.write(text)
            # Close the file
            results_file.close()

            sys.exit(0)


if __name__ == '__main__':
    main()
