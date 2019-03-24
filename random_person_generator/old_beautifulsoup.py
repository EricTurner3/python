# Generate a profile for a non-existent individual
from bs4 import BeautifulSoup #Import beautifulsoup for web scraping
import requests # grab the html from the url for parsing
import random # for getting a random number
import os # for clearing the screen
import urllib, json # json 


os.system('cls' if os.name=='nt' else 'clear') # clear the screen

# generate a random first name and last name by scraping popular baby names and a list of surnames
def gen_name():
    # ====================
    # FIRST NAME RETRIEVER
    # ====================
    # top 50 baby names for the week URL
    print('Loading top 50 first names...')
    baby_names_url = requests.get("https://www.babynames.com/Names/top-baby-names-of-the-week.php").text
    # get the html from the website
    baby_names = BeautifulSoup(baby_names_url, features="html.parser")
    # the baby names are all stored in a table with a class="mostpopular"
    table = baby_names.find('table', 'mostpopular')
    # use a random number to get a random index of a first name from the table
    random_firstname = random.randint(1, len(table.find_all('a'))-1)
    # print out all of the baby names from the table
    #for link in table.find_all('a'):
        #print(link.contents[0])
    # grab one of those names and assign it to a first name variable
    print('Picking random first name from list...')
    firstname = table.find_all('a')[random_firstname].contents[0].lower().capitalize()




    # =================
    # SURNAME RETRIEVER
    # =================
    surnames_url = requests.get("http://www.genealogycenter.info/treece/surnames-all.php?tree=").text
    print('Loading list of surnames...')
    surnames = BeautifulSoup(surnames_url, features="html.parser")
    # surnames are stored in several tables with the class sntable
    surnames_tables = surnames.findAll('table', {"class":"sntable"})
    # use a random number generator to pick a random table from the list
    random_table = random.randint(1, len(surnames_tables)-1)
    # use a random number generator to pick a random link from the tables
    random_surname = random.randint(2, len(surnames_tables[random_table].find_all('a'))-1)
    # use those random numbers to access the specfic table and index of surname 
    print('Picking random surname from list...')
    surname = surnames_tables[random_table].find_all('a')[random_surname].contents[0].lower().capitalize()

    return {"firstname":firstname, "surname":surname}

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

    return lastname.lower() + random.choice(punctuation) + firstname.lower() + str(random.randrange(9)) + random.choice(mailproviders)

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



# call the methods to grab the information
name = gen_name()
phone = gen_phone()
email = gen_email(name["firstname"], name["surname"])
address = gen_address()
# output
os.system('cls' if os.name=='nt' else 'clear') # clear the screen
print('========================')
print('RANDOM PERSON GENERATOR v1.0')
print('========================')
print("Name: " + name["firstname"] + " " + name["surname"])
print("Phone Number: " + phone)
print("Email: " + email)
print("Address: " + address.address1 + " " + address.address2)
print('\n\n\n')

