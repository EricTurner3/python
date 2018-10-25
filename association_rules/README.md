Association Rules
==
This directory was my experimentation with the apyori and mlxtend libraries in analyzing a dataset using association rules.
My first tests were with the apyori library, but I found mlxtend to be much better in doing what I wanted to accomplish.

The mlxtend_association.py file is commented with each step that the code executes and also spits out what step it is executing in 
the console. This can be a very good learning tool for others and helps show my thought process in the coding and understanding of 
the material.

The mlxtend_association.py file ALSO exports some of the files it has done manipulations to in the outputs folder. Opening these CSV
files allows you to see the one-hot encoding, frequent itemsets discovered by apyori and the rules. I discovered there can be way
too many outputs in the console if your min_support variable is very low (like mine is) so the file output is the best way to be able
to dissect what the code is actually doing in it's manipulations.