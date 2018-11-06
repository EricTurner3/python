# # # # # # # # # # # #
# File Name: main.py
# Purpose: Decision Tree Classification of the KDDCUP dataset for network intrustion
# Author: Eric Turner, part of a group in CIT 49900 for Project 1 (code entirely written by me)
# Original Date Created: 17 Oct 2018
# # # # # # # # # # # #


import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from matplotlib import pyplot as plt
from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
import pydotplus

# Sources
# [1] https://secdevops.ai/learning-packet-analysis-with-data-science-5356a3340d4e -  Original Guide
# [2] https://stackoverflow.com/questions/45681387/predict-test-data-using-model-based-on-training-data-set -  Using two files for training and testing data
# [3] https://stackoverflow.com/questions/34007308/linear-regression-analysis-with-string-categorical-features-variables - Converting Categorical into Numerical Values
# [4] https://stackabuse.com/decision-trees-in-python-with-scikit-learn/ - Decision Trees in Python
# [5] https://medium.com/@rnbrown/creating-and-visualizing-decision-trees-with-python-f8e8fa394176 - Visualizing Decision Trees
# [6] http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html - Learning bout the Classifier
# [7] http://intelligentonlinetools.com/blog/2018/02/10/how-to-create-data-visualization-for-association-rules-in-data-mining/ - Usage of a applying a random number to prevent scatter plot overlapping
# [8] https://stackoverflow.com/questions/42891148/changing-colors-for-decision-tree-plot-created-using-export-graphviz - Changing colors of decision tree

# Load training and test data from csv [Source 2]
print("Importing .CSVs... \n")
training = pd.read_csv('kddcup.data_subset_training.csv', header=0, sep=',')
test = pd.read_csv('kddcup.data_subset_test.csv', header=0, sep=',')

# input the factors that will be used for the model
factors = ['src_bytes', 'dst_bytes', 'srv_count', 'logged_in', 'dst_host_count', 'hot', 'num_failed_logins', 'dst_host_rerror_rate', 'rerror_rate', 'dst_host_srv_count']

# convert categories into num codes on both training and test sets
# the integers will correspond with the below categories array [Source 3]
#                0              1            2         3          4
categories = ['normal.', 'guess_passwd.', 'smurf.', 'spy.', 'ftp_write.']

print("Converting Categorical Data Types to Numeric... \n")
training["Codes"] = training["Label"].astype(pd.api.types.CategoricalDtype(categories=categories)).cat.codes
test["Codes"] = test["Label"].astype(pd.api.types.CategoricalDtype(categories=categories)).cat.codes

# setup the model
# used a decision tree classifier because the many factors can have an effect on the path taken to classify correctly [Source 4, 6]
print("Initialization DecisionTreeClassifier Model \n")
model = DecisionTreeClassifier(criterion='entropy')

# train and test the data against the target [Source 2]
print("Loading Training and Test Factors... \n")
train_data = training[factors]
test_data = test[factors]
target = training['Codes']
correct_predictions = test['Codes'].values

print("Training algorithm... \n")
# fit the model
model.fit(train_data, target)

# predict what the label should be based off the factors using the model
print("Predicting test data... \n")
predictions = model.predict(test_data)

# convert the integers back into categorical labels for easy human-readable results
print("Converting numerical predicted data back into categories... \n")
correct_predictions_category = []
predictions_category = []
for val in correct_predictions:
    correct_predictions_category.append(categories[val])

for val in predictions:
        predictions_category.append(categories[val])

print("Generating Dataframe of Correct vs Predicted Test Data... \n")
# Print out a table of the correct vs the predicted side by side
pred = pd.DataFrame({'Correct': correct_predictions_category, 'Predicted': predictions_category})
# print(pred) # Predictions
print("Exporting dataframe to CSV... \n")
# Export the table to a CSV in this working directory to see full results
pred.to_csv('model_results.csv', index=False)

print("Generating Statistics on Model... \n")
print("=============================\n")
# Calculate the accuracy score (data predicted vs actual known values)
print("Accuracy Score:", model.score(test_data, correct_predictions))

print("Confusion Matrix: ")
print(confusion_matrix(predictions, correct_predictions))

print("Classification Report: ")
print(classification_report(predictions, correct_predictions))
print("=============================\n")

print("Creating Scatter Plot of Model Accuracy...\n")

# Show the predictions vs actual known test label in a visualization
plt.scatter(correct_predictions_category, predictions_category, s=70, alpha=0.25)

plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

print("Creating Decision Tree..\n")
# Display Decision Tree [Source 5]
dot_data = StringIO()
export_graphviz(model, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True, feature_names=factors, class_names=categories)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

print("Exporting Decision Tree to File...\n")
graph.write_png('tree.png')
print("Analysis Complete\n")


