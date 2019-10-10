# # # # # # # # # # # #
# File Name: weather_scoring.py
# Purpose: Generate a score for each type of action and modifier
# Author: Eric Turner
# Original Date Created: 17 April 2019
# Modification History:
#   16 Apr 2019 - Code Created  
# # # # # # # # # # # #

import pandas as pd
from sklearn import linear_model
from sklearn import svm
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import datetime as dt
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics

# Linear Regression Model throws a RuntimeWarning to console, this suppress the warning
import warnings
warnings.filterwarnings(action="ignore", module="sklearn", message="^internal gelsd")

# Load data from csv
print("Importing .CSV... \n")
dirty_data = pd.read_csv('weather_model.csv', header=0, sep=',')

# modifiers will modify the action score by a percentage based on severity
modifiers = {
    "clear": 1,
    "few": 0.900,
    "scattered": 0.875,
    "broken": 0.850,
    "overcast": 0.825,
    "light": 0.350,
    "light intensity": 0.325,
    "moderate": 0.300,
    "ragged": 0.295,
    "freezing": 0.295,
    "whirls": 0.285,
    "heavy": 0.250,
    "heavy intensity": 0.200,
    "very heavy": 0.150,
    "extreme":0.050
}

# assign a score to each action 0.500 being perfect, 0.050 being awful
actions = {
    "sky": 0.500,
    "clouds": 0.475,
    "fog": 0.450,
    "mist": 0.425,
    "drizzle": 0.400,
    "shower": 0.375,
    "rain": 0.350,
    "thunderstorm": 0.300,
    "sleet": 0.275,
    "snow": 0.275,
    "smoke": 0.255,
    "haze": 0.255,
    "dust": 0.225,
    "sand": 0.225,
    "volcanic ash": 0.175,
    "squalls": 0.150,
    "tornado": 0.050
}

# input the factors that will be used for the model 
factors = [
    'Modifier_1',    # Adjective to describe Action_1
    'Action_1',      # The primary action
    'Modifier_2',    # Adjective to describe Action_2
    'Action_2',      # The secondary action
    'Modifier_3',    # Adjective to describe Action_3
    'Action_3'       # The tertiary action
]    

print("Instantiating duplicate DataFrame \n")
weather_data = dirty_data
# convert the string to numerics by iterating through each row
print("Calculating score... \n")

# fill NaN values with 1, because we are multiplying so x 1 will return the same
weather_data = weather_data.fillna(1)

# loop through each row and calculate the score
print("{")
for index, row in weather_data.iterrows():
    # calculate the values
    if row['Modifier_1'] != 1:
        modifier_1 = modifiers[row['Modifier_1']]
    else:
        modifier_1 = 1
    if row['Action_1'] != 1:
        action_1 = actions[row['Action_1']]
    else:
        action_1 = 1

    if row['Modifier_2'] != 1:
        modifier_2 = modifiers[row['Modifier_2']]
    else:
        modifier_2 = 1
    if row['Action_2'] != 1:
        action_2 = actions[row['Action_2']]
    else:
        action_2 = 1

    if row['Modifier_3'] != 1:
        modifier_3 = modifiers[row['Modifier_3']]
    else:
        modifier_3 = 1
    if row['Action_3'] != 1:
        action_3 = actions[row['Action_3']]
    else:
        action_3 = 1

    new_score = (modifier_1 * action_1 * modifier_2 * action_2 * modifier_3 * action_3)
    formatted = "{0:.2f}".format(new_score)
    row['Score'] = formatted
    print(str(row['ID']) + ": " + str(formatted) + ", ")

print("}")

# print(weather_data)
#weather_data.to_csv('scored_weather_model.csv', index=False)

