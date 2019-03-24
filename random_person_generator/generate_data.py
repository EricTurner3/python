from bs4 import BeautifulSoup #Import beautifulsoup for web scraping
import requests # grab the html from the url for parsing
import random # for getting a random number
import urllib, json # json 


# Create a names.json file in the current directory based off the top 50 baby names this week and a complete list of over 3000 surnames
def gen_names():
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
    # add the first names to an array
    first_names = []

    for link in table.find_all('a'):
        #print(link.contents[0])
        first_names.append(link.contents[0])
    
    print('First Names retrieved!')




    # =================
    # SURNAME RETRIEVER
    # =================
    surnames_url = requests.get("http://www.genealogycenter.info/treece/surnames-all.php?tree=").text
    print('Loading list of surnames...')
    surnames = BeautifulSoup(surnames_url, features="html.parser")
    # surnames are stored in several tables with the class sntable
    surnames_tables = surnames.findAll('table', {"class":"sntable"})
    last_names = []
    for table in surnames_tables:
        for link in table.find_all('a'):
            #print(link.contents[0])
            last_names.append(link.contents[0])

    print('Surnames Retrieved!')
    # encode json
    print('Encoding Names in JSON...')
    names = {"firstnames": first_names, "surnames": last_names}
    names_json = json.dumps(names, indent=4)

    print('Writing to file...')
    f = open("names.json", "w")
    f.write(names_json) 
    f.close()
    print('Names JSON exported!')


# run the function to generate the names.json file
gen_names()