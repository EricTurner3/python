# Dataset source: https://www.kaggle.com/xvivancos/transactions-from-a-bakery
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules


# Import the dataset
dataset = pd.read_csv("BreadBasket_DMS.csv", header=0)
data = pd.DataFrame(data=dataset)
# Current Data Overview:
#        Date      Time  Transaction           Item
#  2016-10-30  10:07:57            3  Hot chocolate
#  2016-10-30  10:07:57            3            Jam
#  2016-10-30  10:07:57            3        Cookies

# Choose the columns we will need for the data pre-processing
# Date and time are irrelevant for association rules
columns = ['Transaction', 'Item']
# Set the data variable to only the data we need
data = data[columns]

# The data is currently one item per row, and 'n' number of rows can belong to a single transaction
# We need to combine the data so each row is a single transaction
data = data.groupby('Transaction').agg({'Item': ', '.join}).reset_index()

# Current Data Overview:
#   Transaction                         Item
#             3  Hot chocolate, Jam, Cookies

# Split the aggregated data into one item per column
data = data['Item'].str.split(', ', expand=True)
# Export this to CSV and then re-import as a new datafile for OHT
data.to_csv('aggregated_data.csv', index=False, header=False)

aggregated_data = pd.read_csv('aggregated_data.csv', header=None)

# Remove the none or NaN values
aggregated_data = aggregated_data.replace(np.nan, '', regex=True)
aggregated_data = aggregated_data.replace('NONE', '', regex=True)

records = []
for i in range(0, len(aggregated_data)):
    records.append([str(aggregated_data.values[i, j]) for j in range(0, 12)])

# Take the new lists and one hot encode
# This will take the lists, and take EVERY unique item as a column and then for the records
# it will spit out TRUE or FALSE if that record has that item in it

# Original Guide uses OnehotTransactions (deprecated)
# Using TransactionEncoder now: https://rasbt.github.io/mlxtend/user_guide/preprocessing/TransactionEncoder/


print("Applying One-Hot Encoding to the nested-list dataset..." + "\n")
te = TransactionEncoder()
te_ary = te.fit(records).transform(records)
oht_data = pd.DataFrame(te_ary, columns=te.columns_)

# The first column is actually of null values, so we will remove that column as it is dirty data
oht_data = oht_data.drop(oht_data.columns[0], axis=1)

print("Encoding Complete. Dropping File..." + "\n")
oht_data.to_csv('outputs/breadbasket_oht.csv', index=False)

# Applying Apriori
print("Applying Apriori for Frequent Itemsets..." + "\n")
# The first column is actually null values, and is True all the way down. We will omit that column
frequent_itemsets = apriori(oht_data, min_support=0.005, use_colnames=True)
print("Discovered " + str(len(frequent_itemsets)) + " frequent itemsets. Dropping file..." + "\n")
pd.DataFrame(frequent_itemsets).to_csv('outputs/breadbasket_freq_itemsets.csv', index=False)

rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
print("Discovered " + str(len(rules)) + " rules. Dropping file..." + "\n")
pd.DataFrame(rules).to_csv('outputs/breadbasket_rules.csv', index=False)
