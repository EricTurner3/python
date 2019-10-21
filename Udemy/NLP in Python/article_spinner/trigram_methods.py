# build a trigram model
# find all trigram probabilities
import nltk
import random
import numpy as np
from future.utils import iteritems
from bs4 import BeautifulSoup

# test data
#positive_reviews = BeautifulSoup(open('../data/electronics/positive.review').read(), features="lxml")
#positive_reviews = positive_reviews.findAll('review_text')

# grab a string and find the trigrams
# return a dictionary 

#trigrams = {} # placeholder for the function trigram
#trigram_probabilities = {}

# function to find trigrams from an input and output them to a dict
# find_trigrams(positive_reviews, trigrams)
'''
Method: find_trigrams
Parameters:
    * inp - list input of text to analyze
    * out - list variable to output the results
'''
def find_trigrams(inp, out):
    for key in inp:
        s = key.text.lower()
        tokens = nltk.tokenize.word_tokenize(s)
        for i in range(len(tokens) - 2):
            k = (tokens[i], tokens[i+2])
            if k not in out:
                out[k] = []
            out[k].append(tokens[i+1])



# function to find the probabilities from input trigrams and output a probability vector
# find_trigram_probabilities(trigrams, trigram_probabilities)
def find_trigram_probabilities(inp, out):
    for k, words in iteritems(inp):
        # create a dictionary of word -> count
        if len(set(words)) > 1:
            # only do this when there are different possibilities for a middle word
            d = {}
            n = 0
            for w in words:
                if w not in d:
                    d[w] = 0
                d[w] += 1
                n += 1
            for w, c in iteritems(d):
                d[w] = float(c) / n
            out[k] = d


# run our functions
#find_trigrams(positive_reviews, trigrams)
#print(trigrams)
#print('==========================================')
#find_trigram_probabilities(trigrams, trigram_probabilities)
#print(trigram_probabilities)