# Generate a profile for a non-existent individual
# this file loads from .json files locally to minimize loading time instead of calling beautiful soup to load the webpages
from bs4 import BeautifulSoup #Import beautifulsoup for web scraping
import requests # grab the html from the url for parsing
import random # for getting a random number
import os # for clearing the screen
import urllib, json # json 
import sys # for arguments
import string # for the password generation


os.system('cls' if os.name=='nt' else 'clear') # clear the screen

# generate a random first name and last name by scraping popular baby names and a list of surnames
def gen_name():
    print("Loading Names List...")
    with open('names.json') as json_file:  
        names = json.load(json_file)
        random_firstname = random.randrange(len(names['firstnames']))
        random_surname = random.randrange(len(names['surnames']))
        print("Picking random first name and last name")
    return {"firstname":names['firstnames'][random_firstname].lower().capitalize(), "surname":names['surnames'][random_surname].lower().capitalize()}

# from https://stackoverflow.com/questions/26226801/making-random-phone-number-xxx-xxx-xxxx
def gen_phone():
    print('Generating random phone number...')
    first = str(random.randint(100,999))
    second = str(random.randint(1,888)).zfill(3)

    last = (str(random.randint(1,9998)).zfill(4))
    while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
        last = (str(random.randint(1,9998)).zfill(4))

    return '{}-{}-{}'.format(first,second, last)

# generate an email based off lastname_firstname@randomprovider.com
def gen_email(firstname, lastname):
    punctuation = ['.', '_', '']
    mailproviders = ['@yahoo.com', '@gmail.com', '@aol.com', '@outlook.com', '@hotmail.com']
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    password = ''.join(random.choice(chars) for i in range(8))

    return {"email": lastname.lower() + random.choice(punctuation) + firstname.lower() + str(random.randrange(9)) + random.choice(mailproviders), "password": password}

# generate a random address
def gen_address():
    # load the random addresses from this json file
    print("Loading Address List...")
    with open('addresses.json') as json_file:  
        addresses = json.load(json_file)
        print("# of Addresses: " + str(len(addresses['addresses'])))
        randomNumber = random.randrange(len(addresses['addresses']))
        print("Picking random address")
        return addresses['addresses'][randomNumber]

# generate a random bank account
def gen_account():
    account_number = ''.join(random.choice(string.digits) for i in range(10))
    print("Loading Banks List...")
    with open('banks.json') as json_file:  
        banks = json.load(json_file)
        print("Picking random bank")
        bank = random.choice(banks)
    return {"bank": bank, "account_num": account_number}


# print the results to the console for print
def consoleprint():
    # call the methods to grab the information
    name = gen_name()
    phone = gen_phone()
    email = gen_email(name["firstname"], name["surname"])
    address = gen_address()
    bank = gen_account()
    # output
    os.system('cls' if os.name=='nt' else 'clear') # clear the screen
    print('=============================')
    print('RANDOM PERSON GENERATOR v1.0')
    print('=============================')
    print("Name: " + name["firstname"] + " " + name["surname"])
    print("Phone Number: " + phone)
    print("Email: " + email["email"])
    print("Password: " + email["password"])
    print("Address: " + address['address1'] + " " + address['address2'])
    print("City: " + address['city'] + ", " + address['state'])
    print("Postal Code: " + address['postalCode'])
    print("Bank: " + bank["bank"])
    print("Account Number: " + bank["account_num"])
    print('\n\n\n')

# export the results to a json file
def json_export():
    # call the methods to grab the information
    name = gen_name()
    phone = gen_phone()
    email = gen_email(name["firstname"], name["surname"])
    address = gen_address()
    bank = gen_account()
    
    data = {"name": name, "phone": phone, "email": email, "address": address, "bank": bank}
    data_json = json.dumps(data, indent=4)

    print('Writing to file...')
    f = open("person.json", "w")
    f.write(data_json) 
    f.close()

    print('Names JSON exported!')

# output the results to the console in JSON format
def json_output():
    # call the methods to grab the information
    name = gen_name()
    phone = gen_phone()
    email = gen_email(name["firstname"], name["surname"])
    address = gen_address()
    bank = gen_account()
    
    data = {"name": name, "phone": phone, "email": email, "address": address, "bank": bank}
    data_json = json.dumps(data, indent=4)

    os.system('cls' if os.name=='nt' else 'clear') # clear the screen
    return data_json 

# options
# if no argument is passed or console, then display the easy console view
if(len(sys.argv) == 1):
    pass
elif (sys.argv[1] == "console"):
    consoleprint() # print out to an easily human-readable format
# if jsonexport is passed then export the data to person.json
elif (sys.argv[1] == "json_export"):
    json_export()
# if json_output is passed then output the data to the console in JSON format (could also be called from another script for use)
elif (sys.argv[1] == "json_output"):
    data = json_output()
    json = json.loads(data) # this is how you need to actually parse the JSON for other applications (unused)
    print(data) # this is just for showing it in the console
