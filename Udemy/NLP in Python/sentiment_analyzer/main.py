import nltk
import numpy as np
from future.utils import iteritems
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import LogisticRegression
from bs4 import BeautifulSoup

wordnet_lemmatizer = WordNetLemmatizer()

# from http://www.lextek.com/manuals/onix/stopwords1.html
stopwords = set(w.rstrip() for w in open('../data/stopwords.txt'))

# data courtesy of http://www.cs.jhu.edu/~mdredze/datasets/sentiment/index2.html

# open the .review file for the positive reviews
# pass 'features="lxml"' to supress the UserWarning: No parser was explicitly specified
positive_reviews = BeautifulSoup(open('../data/electronics/positive.review').read(), features="lxml")
# we only need to look at the review_text key
positive_reviews = positive_reviews.findAll('review_text')

# do the same for the negative reviews
# pass 'features="lxml"' to supress the UserWarning: No parser was explicitly specified
negative_reviews = BeautifulSoup(open('../data/electronics/negative.review').read(), features="lxml")
# we only need to look at the review_text key
negative_reviews = negative_reviews.findAll('review_text')

# we have more positive reviews than negative, so we will shuffle the positive and cap it so both sets will always be the same length
# shuffle the dataset
np.random.shuffle(positive_reviews)
# this will only grab the same number of rows that is in the negative_reviews
positive_reviews = positive_reviews[:len(negative_reviews)]

# perform some actions on the reviews
def my_tokenizer(s):
    s = s.lower() # downcase
    tokens = nltk.tokenize.word_tokenize(s) # split string into words (tokens)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords
    return tokens # return out for the for loop

# create a word-to-index map so that we can create our word-frequency vectors later
word_index_map = {}
current_index = 0

# save the tokenized arrays for later use (since we have to make two passes)
positive_tokenized = []
negative_tokenized = []
# save a copy of the original reviews
orig_reviews = []

# tokenization
# go through each review in the positive_reviews
for review in positive_reviews:
    # save a copy of the original reviews
    orig_reviews.append(review.text)
    # parse out the tokens
    tokens = my_tokenizer(review.text)
    # append to the tokenized array
    positive_tokenized.append(tokens)
    # check if the token is already in our dictionary
    for token in tokens:
        if token not in word_index_map:
            word_index_map[token] = current_index
            current_index += 1

# go through each review in the negative_reviews
for review in negative_reviews:
    # save a copy of the original reviews
    orig_reviews.append(review.text)
    # parse out the tokens
    tokens = my_tokenizer(review.text)
    # append to the tokenized array
    negative_tokenized.append(tokens)
    # check if the token is already in our dictionary
    for token in tokens:
        if token not in word_index_map:
            word_index_map[token] = current_index
            current_index += 1

# create input matrices
def tokens_to_vector(tokens, label):
    x = np.zeros(len(word_index_map) + 1) # last element is for the label
    for t in tokens:
        i = word_index_map[t]
        x[i] += 1
    x = x / x.sum() # normalize before setting the label
    x[-1] = label # set the last element to the passed label
    return x

N = len(positive_tokenized) + len(negative_tokenized)
data = np.zeros((N, len(word_index_map) + 1))
i = 0

for tokens in positive_tokenized:
    xy = tokens_to_vector(tokens, 1) # these are positive so make the vector 1
    data[i,:] = xy
    i += 1

for tokens in negative_tokenized:
    xy = tokens_to_vector(tokens, 0) # these are negative so make the vector 0
    data[i,:] = xy
    i += 1

np.random.shuffle(data)

# all the rows and everything but the last column
X = data[:, :-1]
# the last column is the labels
Y = data[:, -1]

Xtrain = X[:-100,]
Ytrain = Y[:-100,]

Xtest = X[-100:,]
Ytest = Y[-100:,]

# pass solver parameter to supress FutureWarning: Default solver will be changed to 'lbfgs' in 0.22.
model = LogisticRegression(solver='liblinear')
model.fit(Xtrain, Ytrain)
print("Classification rate:", model.score(Xtest, Ytest))


# print out words which cross a certain threshold
threshold = 0.5
for word, index in iteritems(word_index_map):
    weight = model.coef_[0][index]
    if weight > threshold or weight < -threshold:
        print(word, weight)
