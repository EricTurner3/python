Random Person Generator
===

This is the directory for a collection of scripts to generate a random, non-existant person. I get a lot of spam emails,
so this is useful to generate spam data and I can use it to then generate fake emails or people to spam out for whatever need I have.

Description of Files:
* **addresses.json** - This is a copy of addresses-us-all.json from RRAD on GitHub (https://github.com/EthanRBrown/rrad)
* **generate_data.py** - This script, when run, will use beautiful soup to grab the top 50 baby names and list of 3000 surnames and export to names.json
* **main.py** - This is the main file that can generate fake users. You can pass console, json_export, json_output as arguments to return the data in different ways
* **names.json** - This is the output of names from the generate_data.py script
* **person.json** - If you run `main.py json_export` then the JSON data will be output to this person.json file for use wherever
* **test.py** - This is a demonstration of importing the main.py script into another file, and calling the json_output function to use the JSON data for other uses. Here I just output some generic information about the user that could be used in an email to a scammer