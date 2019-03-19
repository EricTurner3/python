# # # # # # # # # # # #
# File Name: predict_house.py
# Purpose: Project 2 - Predict the selling price of a house
# Author: Eric Turner
# Original Date Created: 17 Oct 2018
# Modification History:
#   17 Oct 2018 - Code Created for Project 1 - Network Intrusion Analysis
#   8 Nov 2018 - Code refactored for Project 2
# # # # # # # # # # # #

# Sources:
# Dataset: https://www.kaggle.com/harlfoxem/housesalesprediction
# [1]: https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
# [2]: https://stackoverflow.com/questions/40217369/python-linear-regression-predict-by-date

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import datetime as dt
# Original Source 1 is outdated with the validation import, this is the correct one
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics

# Linear Regression Model throws a RuntimeWarning to console, this suppress the warning
import warnings
warnings.filterwarnings(action="ignore", module="sklearn", message="^internal gelsd")

# Load data from csv
print("Importing .CSV... \n")
dirty_data = pd.read_csv('kc_house_data.csv', header=0, sep=',')

# linear regression does not work with date data, it needs to be converted [ Source 2]
dirty_data['date'] = pd.to_datetime(dirty_data['date'])
dirty_data['date'] = dirty_data['date'].map(dt.datetime.toordinal)

# input the factors that will be used for the model
factors = ['date',           # Date the house was sold
           'bedrooms',       # Total # of Bedrooms
           'bathrooms',      # Total # of Bathrooms
           'sqft_living',    # Original  SqFootage of home
           'sqft_lot',       # Original SqFootage of lot
           'floors',         # Number of floors
           'waterfront',     # 1 - Waterfront Property
           'view',           # Property has been viewed
           'condition',      # Overall condition
           'grade',          # Grade given based on King County Grading System
           'sqft_above',     # SqFootage Above Ground
           'sqft_basement',  # SqFootage of Basement (above 0 indicates basement)
           'yr_built',       # Original year built
           'yr_renovated',   # Year house was renovated
           'zipcode',        # USPS ZIP code
           'lat',            # Latitude of lot
           'long',           # Longitude of Lot
           'sqft_living15',  # SqFootage of home in 2015 (adding any renovations)
           'sqft_lot15'      # SqFootage of lot in 2015 (adding any renovations)
           ]


# setup the model

print("Initialization of Linear Regression Model \n")
lm = LinearRegression()

# train and test the data against the target [Source 1]
print("Loading Training and Test Factors... \n")
house_data = dirty_data[factors]
target = dirty_data['price']
# test_size is how the data should be split: 0.1 is 90/10 in training to test
data_train, data_test, target_train, target_test = train_test_split(house_data, target, test_size=0.1)
correct_predictions = target_test.values

print("Training algorithm... \n")
# fit the model
model = lm.fit(data_train, target_train)

# predict what the label should be based off the factors using the model
print("Predicting test data... \n")
predictions = lm.predict(data_test)


print("Generating Dataframe of Correct vs Predicted Test Data... \n")
# Print out a table of the correct vs the predicted side by side
pred = pd.DataFrame({'Correct': correct_predictions, 'Predicted': predictions})
# print(pred) # Predictions
print("Exporting dataframe to CSV... \n")
# Export the table to a CSV in this working directory to see full results
pred.to_csv('model_results.csv', index=False)

# Show the predictions vs actual known test label in a visualization
plt.scatter(correct_predictions, predictions, s=70, alpha=0.25)

plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.title("Accuracy of Predictions vs True Values")
plt.show()

# Print out Accuracy Score
print("Accuracy Score: " + str(model.score(data_test, target_test)))

# without doing cross-validation, model only is 70% accurate
scores = cross_val_score(model, house_data, target, cv=6)
print ("Cross-validated scores:", scores)

# Make cross validated predictions
predictions = cross_val_predict(model, house_data, target, cv=6)
plt.scatter(target, predictions, s=70, alpha=0.25)
plt.title("Cross-Validation Accuracy of Predictions vs True Values")
plt.show()

accuracy = metrics.r2_score(target, predictions)
print ("Cross-Predicted Accuracy:", accuracy)
# Even with cross-validation, 70% is as accurate as we can get with only these factors
