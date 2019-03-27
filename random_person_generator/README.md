Random Person Generator
===
Original v1.0 Build:
This is the directory for a collection of scripts to generate a random, non-existant person. I get a lot of spam emails,
so this is useful to generate spam data and I can use it to then generate fake emails or people to spam out for whatever need I have.

Update: v1.1 (27 Mar 2019)
I added a birthdate generator and social security num generator. Unfortunately, the method I used does not support Python 2.x so Python 3+ must be used. I also better formatted the console output.

Description of Files:
* **addresses.json** - This is a copy of addresses-us-all.json from RRAD on GitHub (https://github.com/EthanRBrown/rrad)
* **banks.json** - A list of banks to be randomly chosen from
* **generate_data.py** - This script, when run, will use beautiful soup to grab the top 50 baby names and list of 3000 surnames and export to names.json
* **main.py** - This is the main file that can generate fake users. You can pass console, json_export, json_output as arguments to return the data in different ways
* **names.json** - This is the output of names from the generate_data.py script
* **person.json** - If you run `main.py json_export` then the JSON data will be output to this person.json file for use wherever
* **test.py** - This is a demonstration of importing the main.py script into another file, and calling the json_output function to use the JSON data for other uses. Here I just output some generic information about the user that could be used in an email to a scammer
* **old_beautifulsoup.py** - Originally, I was using beautiful soup to grab a new list at runtime each time but it caused the execution to take around 5s each time. By splitting this file into generate_data.py and main.py, execution and reading from pre-made JSON files is near instantaneous

Usage
===

```python
python3 /file/directory/main.py [argument]
```
Arguments: 
* console - Print out the randomly generated user information to the console
* json_export - Export out the randomly generate user information to person.json to be used
* json_output - Call this function in another script (import main and then call main.json_output()) to use the data in json

Examples
===
Using the console argument

```python
python3 /file/directory/main.py console


Output:
--------------
=============================
RANDOM PERSON GENERATOR v1.1
=============================
Name: Fabian Cross
Phone Number: +1 (859) 478-0711
Birth Date: 06/18/1934

Email: cross_fabian8@outlook.com
Password: goXYL!gw

Address: 3601 South Portland Avenue 
City: Oklahoma City, OK
Postal Code: 73119

Bank: Compass Bank
Account Number: 7910367977

Soc Sec Number: 231-52-2627

```



Using the JSON output argument in another file
```python
import main # import the main.py (must be in same directory)
import json
# call the json_output function to retrieve a new user in json
random_person = json.loads(main.json_output())

# now we can use the randomly generated information however we want to
print(random_person["name"]["firstname"] + " " + random_person["name"]["surname"] + " is being hacked")

Output:
--------------
Iris Mulvehill is being hacked

```



