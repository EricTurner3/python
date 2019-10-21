import numpy as np

# import test dataset
from sklearn.datasets import load_breast_cancer

print('Load the dataset')
# load the data
data = load_breast_cancer()

print('''
#*#*#*#*#*#*#*#*#*#*#
# Review the dataset
#*#*#*#*#*#*#*#*#*#*#
''')

#*#*#*#*#*#*#*#*#*#*#
# Review the dataset
#*#*#*#*#*#*#*#*#*#*#

# check the type of the data
print('Type of Data:')
type(data)
# it is a sklearn.utils.Bunch object

# lets check the keys
print('Keys in data:')
print(data.keys()) # ['target', 'DESCR', 'target_names', 'feature_names', 'data', 'filename']


# check the shape
print('Shape of data[\'data\']:')
print(data['data'].shape)

# view the data column
print('data[\'data\']:')
print(data['data'])

# check the target column
print('data[\'target\']:')
print(data['target'])

# check the target_names column
print('data[\'target_names\']:')
print(data['target_names'])


# can put this import at the top
#auto split the data in train and test
from sklearn.model_selection import train_test_split

# split the data into train and test (33% is for test)
print('Split data into train and test sets')
X_train, X_test, y_train, y_test = train_test_split(data['data'], data['target'], test_size=0.33)

#*#*#*#*#*#*#*#*#*#*#*#
# Method 1: Classifier
#*#*#*#*#*#*#*#*#*#*#*#

print('''
#*#*#*#*#*#*#*#*#*#*#*#
# Method 1: Classifer
#*#*#*#*#*#*#*#*#*#*#*#
''')


# instantiate a classifier and train it
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
print('Train the model')
model.fit(X_train, y_train)

# evaluate the models performance
print('Accuracy of the model with TRAIN data')
print(model.score(X_train, y_train))
print('Accuracy of the model with TEST data')
print(model.score(X_test, y_test))


# predict
print('Make Predictions with Model')
predictions = model.predict(X_test)

# view the predictions
print('Display Predictions: ')
print(predictions)


#*#*#*#*#*#*#*#*#*#*#*#*#*#
# Method 2: Deep Learning
#*#*#*#*#*#*#*#*#*#*#*#*#*#

print('''
#*#*#*#*#*#*#*#*#*#*#*#*#*#
# Method 2: Deep Learning
#*#*#*#*#*#*#*#*#*#*#*#*#*#
''')

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

print('Set up Scaler, train and test data')
scaler = StandardScaler()
# still use the train set from the split data above
X_train2 = scaler.fit_transform(X_train)
X_test2 = scaler.transform(X_test)

model = MLPClassifier()
print('Fit the Model')
model.fit(X_train2, y_train)

# evaluate the models performance
print('Accuracy of the model with TRAIN data')
print(model.score(X_train2, y_train))
print('Accuracy of the model with TEST data')
print(model.score(X_test2, y_test))