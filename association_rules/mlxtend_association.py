import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules


# Association Rules Using mlxtend's Apriori (referred to as Original Guide in further comments)
# http://intelligentonlinetools.com/blog/2018/02/10/how-to-create-data-visualization-for-association-rules-in-data-mining/

# Import store data set from CSV with pandas
print("Parsing CSV into dataset..." + "\n")
# Dataset from https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/
dataset = pd.read_csv("store_data.csv", header=None)

# Data pro-processing
# Take the dataset and turn it into a list of lists
print("Converting dataset into nested list for manipulation..." + "\n")

print(dataset.values)
records = []
for i in range(0, len(dataset)):
    records.append([str(dataset.values[i, j]) for j in range(0, 20)])

# Records Output Example:
# records[0]: ['almonds', 'avocado','green grapes']
# records[1]: ['asparagus', 'bacon']
# ..

# Take the new lists and one hot encode
# This will take the lists, and take EVERY unique item as a column and then for the records
# it will spit out TRUE or FALSE if that record has that item in it

# Original Guide uses OnehotTransactions (deprecated)
# Using TransactionEncoder now: https://rasbt.github.io/mlxtend/user_guide/preprocessing/TransactionEncoder/
print("Applying One-Hot Encoding to the nested-list dataset..." + "\n")
te = TransactionEncoder()
te_ary = te.fit(records).transform(records)
store_data = pd.DataFrame(te_ary, columns=te.columns_)

# export manipulated data to csv for easier consumption
print("Encoding Complete. Dropping File..." + "\n")
store_data.to_csv('outputs\store_data_oht.csv', index=False)

# Example of possible output using above records output example
#
# almonds   avocado  asparagus  bacon   green grapes ..
# TRUE      TRUE     FALSE      FALSE   TRUE
# FALSE     FALSE    TRUE       TRUE    FALSE
# ..        ..       ..         ..      ..

# Applying Apriori
#
# Min_Support - Trying to find items purchased 5 times a day.
# Data set is a week so 5 x 7 = 35. 7500 items in the list
# so 35 / 7500 = 0.0045
print("Applying Apriori for Frequent Itemsets..." + "\n")
frequent_itemsets = apriori(store_data, min_support=0.0045, use_colnames=True)
print("Discovered " + str(len(frequent_itemsets)) + " frequent itemsets. Dropping file..." + "\n")
pd.DataFrame(frequent_itemsets).to_csv('outputs\store_data_freq_itemsets.csv', index=False)

association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
print("Discovered " + str(len(rules)) + " rules. Dropping file..." + "\n")
pd.DataFrame(rules).to_csv('outputs\store_data_rules.csv', index=False)


# Simple Print to console the total number of rules mined by apriori
# print("Total Rules Mined: " + str(len(association_results)))
# print("Sample of First Rule: " + str(association_results[0]))

# For loop to go through the association results and easily print results to console
# Original guide was using .as_matrix which will be deprecated, converted to using .values
support = rules['support'].values
confidence = rules['confidence'].values

# Visualizing Association Rules
# http://intelligentonlinetools.com/blog/2018/02/10/how-to-create-data-visualization-for-association-rules-in-data-mining/

# Apply a SMALL random int to the values in order to prevent overlap and see the points better
print("Applying variance to support and confidence values..." + "\n")
for i in range(len(support)):
    support[i] = support[i] + 0.0025 * (random.randint(1, 10) - 5)
    confidence[i] = confidence[i] + 0.0025 * (random.randint(1, 10) - 5)

# Plot the support and confidence and show the plot
plt.scatter(support, confidence, alpha=0.5, marker="*")
plt.xlabel('support (frequency the itemset occurs)')
plt.ylabel('confidence (how often rule is true)')
plt.title("Scatter Plot of Support v Confidence")
print("Displaying scatter plot..." + "\n")
plt.show()

# Pass the rules created above and the number of rules you wish to show in the graph


def draw_graph(rules, rules_to_show):
    print("Generating Node Graph with " + str(rules_to_show) + " rules ..." + "\n")
    import networkx as nx
    G1 = nx.DiGraph()

    color_map = []
    N = 50
    colors = np.random.rand(N)
    strs = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11']

    for i in range(rules_to_show):
        G1.add_nodes_from(["R" + str(i)])

        for a in rules.iloc[i]['antecedents']:
            G1.add_nodes_from([a])

            G1.add_edge(a, "R" + str(i), color=colors[i], weight=2)

        for c in rules.iloc[i]['consequents']:
            G1.add_nodes_from([c])

            G1.add_edge("R" + str(i), c, color=colors[i], weight=2)

    for node in G1:
        found_a_string = False
        for item in strs:
            if node == item:
                found_a_string = True
        if found_a_string:
            color_map.append('yellow')
        else:
            color_map.append('green')

    edges = G1.edges()
    colors = [G1[u][v]['color'] for u, v in edges]
    weights = [G1[u][v]['weight'] for u, v in edges]

    pos = nx.spring_layout(G1, k=16, scale=1)
    nx.draw(G1, pos, edges=edges, node_color=color_map, edge_color=colors, width=weights, font_size=16,
            with_labels=False)

    for p in pos:  # raise text positions
        pos[p][1] += 0.07
    nx.draw_networkx_labels(G1, pos)
    print("Generation Complete, Displaying Graph..." + "\n")
    plt.title("Node Chart")
    plt.show()


# Execute the function with the association_rules variable
draw_graph(rules, 10)
