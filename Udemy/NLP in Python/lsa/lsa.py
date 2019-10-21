import nltk
import numpy as np 
import matplotlib.pyplot as plt 

from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import TruncatedSVD

wordnet_lemmatizer = WordNetLemmatizer()

titles = [line.rstrip() for line in open('../data/all_book_titles.txt')]

stopwords = set(w.rstrip() for w in open('../data/stopwords.txt'))
# lets add some of our own stopwords
stopwords = stopwords.union({
    'introduction', 'edition', 'series', 'application',
    'approach', 'card', 'access', 'package', 'plus', 'etext',
    'brief', 'vol', 'fundamental', 'guide', 'essential', 'printed',
    'third', 'second', 'fourth'})

# derived from the sentiment_analyzer 
def my_tokenizer(s):
    s = s.lower() # downcase
    tokens = nltk.tokenize.word_tokenize(s) # split string into words (tokens)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords
    tokens = [t for t in tokens if not any(c.isdigit() for c in t)] # remove any numbers like in "3rd edition"
    return tokens # return out for the for loop

word_index_map = {}
current_index = 0
all_tokens = []
all_titles = []
index_word_map = []
error_count = 0
for title in titles:
    try:
        title = title.encode('ascii', 'ignore').decode('utf-8') # this will throw exception if bad characters
        all_titles.append(title)
        tokens = my_tokenizer(title)
        all_tokens.append(tokens)
        for token in tokens:
            if token not in word_index_map:
                word_index_map[token] = current_index
                current_index += 1
                index_word_map.append(token)
    except Exception as e:
        #print(e)
        #print(title)
        error_count += 1


print("Number of errors parsing file:", error_count, "number of lines in file:", len(titles))
if error_count == len(titles):
    print("There is no data to do anything with! Quitting...")
    exit()

# convert the tokens to a vector
def tokens_to_vector(tokens):
    x = np.zeros(len(word_index_map)) 
    for t in tokens:
        i = word_index_map[t]
        x[i] += 1
    return x

N = len(all_tokens)
D = len(word_index_map)
X = np.zeros((D,N)) #create an empty matrix, rows are of length of word_index_map, columns for all_tokens
i = 0 # placeholder for column index

# replace each column to the vector from the token
for tokens in all_tokens:
    X[:,i] = tokens_to_vector(tokens)
    i += 1 # increment column index\

# set up the model
svd = TruncatedSVD()
Z = svd.fit_transform(X)

# display a plot
plt.scatter(Z[:, 0], Z[:,1])
# annotate the plot with the actual words
for i in range(D):
    plt.annotate(s=index_word_map[i], xy=(Z[i,0], Z[i,1]))
# show the plot
plt.show()