# Destiny Application - Log into destiny and prompt for further user interaction

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os




os.system('cls' if os.name=='nt' else 'clear')
print('Loading Browser...')
browser = webdriver.Safari()

# Load Destiny
browser.get(url)
print("Loading Destiny...")

# Find the link for the specfic school specified above and click it
browser.find_element_by_link_text(schoolName).click()
print("Loading School: " + schoolName)


# wait after clicking for the new page to load
browser.implicitly_wait(3)

# in the school page, find the login link and click it
browser.get("")
print("Loading Login Page...")
# wait after clicking for the new page to load
browser.implicitly_wait(3)

# on the login screen we need to find the username and password fields and fill them
browser.find_element_by_name('userLoginName').send_keys(username)
browser.find_element_by_name('userLoginPassword').send_keys(password)
# now click the submit button to login
browser.find_element_by_name('submit').click()
print('Logging In...')

# wait after clicking for the new page to load
browser.implicitly_wait(3)



# methods based on which link is clicked

def circulation_searchAsset(asset):
    browser.find_element_by_name('searchString').send_keys(asset)
    browser.find_element_by_name('go').click()
    # check for next step
    os.system('cls' if os.name=='nt' else 'clear')
    print('===============================')
    print("Available Actions:")
    print('===============================')
    next = raw_input('\nEnter an another asset or type "back" to go back: ')
    if next == 'back':
        # go back a page and then loop through the main page
        browser.find_element_by_id('TopLevelCirculation').click()
        circulation()
    else:
        circulation_searchAsset(next)


def circulation():
    
    os.system('cls' if os.name=='nt' else 'clear')
    print('===============================')
    print('Circulation Functions:')
    print('===============================')
    print('[o] : Check Out a Device')
    print('[i] : Check In a Device')
    print('[s] : Item Status')
    print('[b] : Back to Home')
    print('===============================')
    print('\n')
    # grab the function requested
    circulation_function = raw_input('Enter a letter for the function you want: ')
    # list of items in destiny

    sidebarLinks = {
        "o":"Check Out Items",
        "i":"Check In Items",
        "s":"Item Status",
        "b":"Home"
    }
    # find the option specified in the input and click it
    browser.find_element_by_id(sidebarLinks[circulation_function]).click()
    if circulation_function == 'o' or circulation_function == 'i' or circulation_function == 's':
        os.system('cls' if os.name=='nt' else 'clear')
        asset = raw_input('Enter the asset you are working with: ')
        circulation_searchAsset(asset)
    else:
        main_menu()




def catalog():
    os.system('cls' if os.name=='nt' else 'clear')
    print('===============================')
    print('Catalog Functions:')
    print('===============================')





# after authenticated load the menu of options for input
def main_menu():
    os.system('cls' if os.name=='nt' else 'clear')
    print('===============================')
    print('Main Menu:')
    print('===============================')
    print('Choose a Function:')
    print('[a]: Catalog')
    print('[i]: Circulation')
    main_function = raw_input('Enter a letter for the function you want: ')
    # known pages to choose
    links = {
        # page : ID of element on webpage
        "i": "TopLevelCirculation", 
        "a": "TopLevelCatalog"
    }

    # find the link we want from the input
    linkToClick = links[main_function]
    #If the circulation link is specified
    if linkToClick == "TopLevelCirculation":
        browser.find_element_by_id(links[main_function]).click()
        circulation()
    # else if the catalog link is specified
    elif linkToClick == "TopLevelCatalog":
        browser.find_element_by_id(links[main_function]).click()
        catalog()


main_menu()







