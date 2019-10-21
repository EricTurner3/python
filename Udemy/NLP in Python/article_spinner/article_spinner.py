from future.utils import iteritems
import nltk
import random
import numpy as np
from future.utils import iteritems
from bs4 import BeautifulSoup # parse XML

# load the methods I built for the precode exercises
from trigram_methods import find_trigrams, find_trigram_probabilities

# load the reviews (like done in the precode excerise)
positive_reviews = BeautifulSoup(open('../data/electronics/positive.review').read(), features="lxml")
positive_reviews = positive_reviews.findAll('review_text')

# placeholders 
trigrams = {}
trigram_probabilities = {}

# run the placeholders through the methods i built
find_trigrams(positive_reviews, trigrams)
find_trigram_probabilities(trigrams, trigram_probabilities)

def random_sample(d):
    r = random.random()
    cumulative = 0
    for w, p in iteritems(d):
        cumulative += p
        if r < cumulative: 
            return w

# randomly choose a review and spin for comparison

def test_spinner():
    review = random.choice(positive_reviews) # pick a random review
    s = review.text.lower() # lowercase all the text
    print("Original Review: " + s) # print the original review for comparison
    tokens = nltk.tokenize.word_tokenize(s)
    for i in range(len(tokens) - 2):
        # random probability to replace the token with another word
        if random.random() < 0.2:
            k = (tokens[i], tokens[i+2])
            if k in trigram_probabilities:
                w = random_sample(trigram_probabilities[k])
                tokens[i+1] = w
    print("Spun Review: ")
    print(" ".join(tokens).replace(" .", ".").replace(" '", "'").replace(" ,", ",").replace("$ ", "$").replace(" !", "!"))


# run the tes
test_spinner()

