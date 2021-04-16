"""
Wikipedia - All US Police Departments Scrape
13 Apr 2021
This scraper scrapes two main pages on Wikipedia, List of Law Enforcement Agencies & List of United States state and local law enforcement agencies
to download a json formatted list of all agencies in the United States

https://github.com/EricTurner3
"""
from bs4 import BeautifulSoup
import requests
import re
import json

# all federal agencies are listed here under the United States subheader
federal_link = 'https://en.wikipedia.org/wiki/List_of_law_enforcement_agencies#United_States'
# each state has its own link here that will need to be recursed through
state_local_directory = 'https://en.wikipedia.org/wiki/List_of_United_States_state_and_local_law_enforcement_agencies'

# federal agencies are just listed between the United States and Territorial police headers
# grab the full HTML of all countries first
resp = requests.get(federal_link)
html = resp.text
soup = BeautifulSoup(html, 'html.parser')
# now find our beginning and end elements (which are spans inside of h3, so grab the parent)
start = soup.find(class_='mw-headline', string='United States').parent
end = soup.find(class_='mw-headline', string='Territorial police').parent
# now wipe away all the html except just US related stuff
shortened_html = html[html.find(str(start))+1 : html.find(str(end))]
# set that back up with beautiful soup
soup = BeautifulSoup(shortened_html, 'html.parser')
agencies = {}

# now we are ready to format
federal = []
for agency in soup.find_all('li'):
    # some of the agency names are nested or no longer in use
    # make sure to filter those here
    exclusion_list = [
        "Bureau of Diplomatic Security",
        "Marine Corps Provost Marshal's Office",
        "Bureau of Narcotics and Dangerous Drugs (1968–73)",
        "Federal Bureau of Narcotics (1930–68)",
        "Bureau of Prohibition (1927–33)",
        "Bureau of Drug Abuse Control (1966–68)",
        "Bureau of Investigation (BOI) (1908–35)",
        "Library of Congress Police (Dissolved 2009)"
    ]
    # the html sometimes joins agencies with \n so let's make sure we parse them out
    for real_agency in agency.text.split('\n'):
        if real_agency not in federal and real_agency not in exclusion_list:
            federal.append(real_agency)

agencies.update({'federal': federal})

# for state agencies, we query the list page then 
# request through each state and grab the data from there

state_list = requests.get(state_local_directory)
soup = BeautifulSoup(state_list.text, 'html.parser')
links = soup.find_all('a', text=re.compile(r'List of law enforcement agencies'))

for link in links:
    # grab the state page
    print('\n----------------------------------')
    print('Fetching {}'.format(link['href']))
    state_link = requests.get('https://en.wikipedia.org' + link['href'])
    html = state_link.text
    state_soup = BeautifulSoup(html, 'html.parser')
    
    state = state_soup.find(id='firstHeading').text.split('List of law enforcement agencies in ')[1]
    print(state)

    # we only want the agency links so like before I am going to crop the html
    start = state_soup.find(class_='mw-headline').parent  # first main h2
    end = state_soup.find(class_='mw-headline', string='References').parent 
    # not every state has defunct agencies so references is the best place to stop
    # now wipe away all the html except just US related stuff
    shortened_html = html[html.find(str(start))+1 : html.find(str(end))]
    # set that back up with beautiful soup
    state_soup = BeautifulSoup(shortened_html, 'html.parser')
    # each state may be one of the following variations
    all_li = state_soup.find_all('li')
    agency_list = []
    for agency in all_li:
        # sometimes there are bunched up duplicate lines with \n in them
        if '\n' not in agency.text:
            agency_list.append(agency.text)
    
    agencies.update({str(state): agency_list})


out_file = open("agencies.json", "w")
json.dump(agencies, out_file, indent = 4)
out_file.close()
