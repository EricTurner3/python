import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# import the data
print('Importing dataset ./spam.csv..')
# use encoding as latin-1, otherwise a UnicodeDecodeError is thrown during pre-processing
data = pd.read_csv('../data/spam.csv', encoding='latin-1')

#*#*#*#*#*#*#*#*#*#*#*#*#
# Clean up imported data
#*#*#*#*#*#*#*#*#*#*#*#*#

# drop unnecessary columns
data = data.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)

# rename columns to something better
data.columns = ['labels', 'messages']

messages = data['messages'].values # the SMS messages

# the target needs to be numerical, we will make 1 spam and 0 ham
print('Encoding labels "spam" to 1 and "ham" to 0...')

# could also use one-liner: data['labels_encoded'] = data['labels'].map({'ham': 0, 'spam': 1})
data.loc[(data['labels'] == 'spam'),'labels_encoded'] = 1
data.loc[(data['labels'] == 'ham'),'labels_encoded'] = 0

target = data['labels_encoded'].values # the fixed 1 for spam and 0 for ham target values

# look to ensure the labels_encoded shows up
#print(data.head(5))

#*#*#*#*#*#*#*#*#*#*#*#*#*#
# Split Data and Fit Model
#*#*#*#*#*#*#*#*#*#*#*#*#*#


# split the data into train and test (33% is for test)
print('Split data into train and test sets')
df_train, df_test, y_train, y_test = train_test_split(data['messages'], target, test_size=0.33)

# process the messages using CountVectorizer()
print('Process the text...')
count_vectorizer = CountVectorizer(decode_error='ignore')
x_train = count_vectorizer.fit_transform(df_train)
x_test = count_vectorizer.transform(df_test)

# pass n_estimators=10 to suppress the FutureWarning: The default value of n_estimators will change from 10 in version 0.20 to 100 in 0.22.
model = RandomForestClassifier(n_estimators=10)
print('Train the model')
model.fit(x_train, y_train)

# evaluate the models performance
print('Accuracy of the model with TRAIN data')
print(model.score(x_train, y_train))
print('Accuracy of the model with TEST data')
print(model.score(x_test, y_test))


# predict
print('Make Predictions with test data...')
predictions = model.predict(x_test)

# view the predictions (not really useful for humans to read)
#print('Display Predictions: ')
#print(predictions)


#*#*#*#*#*#*#*#*#*#
# Visualize Words
#*#*#*#*#*#*#*#*#*#


# visualize predictions
# this all works well, but we really have no idea what is actually happening unless we visualize it (this uses a wordcloud)

def visualize(label):
  words = ''
  for msg in data[data['labels'] == label]['messages']:
    msg = msg.lower()
    words += msg + ' '
  wordcloud = WordCloud(width=600, height=400).generate(words)
  plt.imshow(wordcloud)
  plt.axis('off')
  plt.show()

print('Showing Word Cloud for spam messages...')
visualize('spam')
print('Showing Word Cloud for ham messages...')
visualize('ham')

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
# Showing Incorrect Predictions
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#

# run the count vectorizer again over the WHOLE dataset
data_predictions = count_vectorizer.transform(data['messages'])
# add a column to the dataframe to save what the model predicted
data['predictions'] = model.predict(data_predictions)


print('Calculating incorrect predictions...')
print('#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*##*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#')
print('These messages were incorrectly predicted as NOT spam, when they ARE spam:')
# things that should be spam (where the prediction was 0 [ham] but the actual data was 1 [spam])
sneaky_spam = data[(data['predictions'] == 0) & (data['labels_encoded'] == 1)]['messages']
for msg in sneaky_spam:
  print(' * ' + msg)

print('#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*##*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#')
print('These messages were incorrectly predicted AS spam, when they NOT spam:')
# things that should not be spam (where the prediction was 1 [spam] but the actual data was 0 [ham])
not_actually_spam = data[(data['predictions'] == 1) & (data['labels_encoded'] == 0)]['messages']
for msg in not_actually_spam:
  print(' * ' + msg)