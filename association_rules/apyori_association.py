import random
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from mlxtend.frequent_patterns import association_rules

# Association Rules Using Apyori's Apriori
# https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/

# Import data set
store_data = pd.read_csv("store_data.csv", header=None)

store_data.head()

# Data pro-processing
# Apriori requires data set to be in a list of lists
records = []
for i in range(0, len(store_data)):
    records.append([str(store_data.values[i, j]) for j in range(0, 20)])

# Applying Apriori
#
# Min_Support - Trying to find items purchased 5 times a day.
# Data set is a week so 5 x 7 = 35. 7500 items in the list
# so 35 / 7500 = 0.0045
#
# Min_Confidence filters 20%
#
# Min_Length because we want at least 2 products in the rules
rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
as_rules = association_rules(rules, metric="lift", min_threshold=1.2)
association_results = list(rules)


# Simple Print to console the total number of rules mined by apriori
# print("Total Rules Mined: " + str(len(association_results)))
# print("Sample of First Rule: " + str(association_results[0]))

# For loop to go through the association results and easily print results to console
support = []
confidence = []
for item in association_results:

    # first index of the inner list
    # Contains base item and add item
    pair = item[0]
    items = [x for x in pair]
    print("Rule: " + items[0] + " -> " + items[1])

    # second index of the inner list
    print("Support: " + str(item[1]))
    support.append(item[1])

    # third index of the list located at 0th
    # of the third index of the inner list

    print("Confidence: " + str(item[2][0][2]))
    confidence.append(item[2][0][2])

    print("Lift: " + str(item[2][0][3]))
    print("=====================================")

# Visualizing Association Rules
# http://intelligentonlinetools.com/blog/2018/02/10/how-to-create-data-visualization-for-association-rules-in-data-mining/

# Apply a SMALL random int to the values in order to prevent overlap and see the points better
for i in range(len(support)):
    support[i] = support[i] + 0.0025 * (random.randint(1, 10) - 5)
    confidence[i] = confidence[i] + 0.0025 * (random.randint(1, 10) - 5)

# Plot the support and confidence and show the plot
plt.scatter(support, confidence, alpha=0.5, marker="*")
plt.xlabel('support')
plt.ylabel('confidence')
plt.show()