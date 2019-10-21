import numpy as np 
import pandas as pd 

#load the data from file
print('Loading data from: ./data/airfoil_self_noise.dat')
df = pd.read_csv('./Udemy/NLP in Python/data/airfoil_self_noise.dat', sep='\t', header=None)

# overview of the data
print('Preview of the dataset: ')
print(df.head())
print('Info about the dataset: ')
df.info()

# get the inputs
data = df[[0, 1, 2, 3, 4]].values
# get the target
target = df[5].values

# usually put inputs up at top of file, import the method to split data into train and test
from sklearn.model_selection import train_test_split

# split the data into train and test (33% is for test)
print('Split data into train and test sets')
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.33)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
print('Train the model')
model.fit(X_train, y_train)

# evaluate the models performance
print('R^2 of the model with TRAIN data')
print(model.score(X_train, y_train))
print('R^2 of the model with TEST data')
print(model.score(X_test, y_test))

# predict
print('Make Predictions with Model')
predictions = model.predict(X_test)

# view the predictions
print('Display Predictions: ')
print(predictions)