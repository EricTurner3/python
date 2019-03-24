import main # import the main.py
import json
# call the json_output function to retrieve a new user in json
random_person = json.loads(main.json_output())

# now we can use the randomly generated information however we want to
print(random_person["name"]["firstname"] + " " + random_person["name"]["surname"] + " is being hacked")



