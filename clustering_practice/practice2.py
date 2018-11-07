# Source: https://www.learndatasci.com/tutorials/k-means-clustering-algorithms-python-intro/
from sklearn import cluster
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_rand_score

# import the dataset from networkx
graph = nx.karate_club_graph()
positioning = nx.spring_layout(graph)

# function to visualize the dataset
def draw_communities(graph, membership, positioning):
    """ Draws the nodes to a plot with assigned colors for each individual cluster
        Parameters
        ----------
        graph : networkx graph
        membership : list
            A list where the position is the student and the value at the position is the student club membership.
            E.g. `print(membership[8]) --> 1` means that student #8 is a member of club 1.
        positioning : positioning as a networkx spring layout
            E.g. nx.spring_layout(G)
        """
    figure, axis = plt.subplots(figsize=(16, 9))

    # Convert membership list to a dict where key=club, value = list of students in club
    club_dict = defaultdict(list)
    for student, club in enumerate(membership):
        club_dict[club].append(student)

    norm = colors.Normalize(vmin=0, vmax=len(club_dict.keys()))

    for club, members in club_dict.items():
        nx.draw_networkx_nodes(graph, positioning,
                               nodelist=members,
                               node_color=cm.jet(norm(club)),
                               node_size=500,
                               alpha=0.8,
                               ax=axis)


    # Draw edges (social connections) and show final plot
    plt.title("Zachary's Karate Club")
    nx.draw_networkx_edges(graph, positioning, alpha=0.5, ax=axis)
