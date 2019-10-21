from sklearn.naive_bayes import MultinomialNB
import pandas as pd 
import numpy as np

# import the data
print('Importing dataset ./spambase.data...')
# video uses .as_matrix() which is being deprecated, using .values instead
data = pd.read_csv('./Udemy/NLP in Python/data/spambase.data').values

# shuffle the data
print('Shuffling Data...')
np.random.shuffle(data)

# grab data for input (x) and target (y)
# the first index is for row numbers and second index is for columns

# for X parameter 1, we use : to indicate to use ALL of the rows
# for X parameter 2, we use :48 to indicate to use the first 48 columns
X = data[:, :48]
# for Y parameter 1, we use : to indicate to use ALL of the rows
# for Y parameter 2, we use -1 to indicate to use the LAST column
Y = data[:, -1]

print("Prepare test and train data...")
# we shuffled the data up above, use this to grab the first 100 rows for train (:-100)
Xtrain = X[:-100,]
Ytrain = Y[:-100,]
# grab the LAST 100 rows for test (-100:)
Xtest = X[-100:,]
Ytest = Y[-100:,]

model = MultinomialNB()
print('Fit the model...')
model.fit(Xtrain, Ytrain)

print ("Classification rate for NB: " +  str(model.score(Xtest, Ytest)))

