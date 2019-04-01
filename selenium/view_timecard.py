# Practice with using selenium to intereact with websites
from selenium import webdriver
import time

url = ""
browser = webdriver.Safari()

# 001.py - Load my timeclock at work and then view my timecard
# Load the timeclock
browser.get(url)

# Find the employee ID box
element = browser.find_element_by_id("LogOnEmployeeId")
# fill it with my employee ID
element.send_keys("")

#Find the login button and click it
login_btn = browser.find_element_by_xpath("//input[@value='Log On To Dashboard']")
login_btn.click()

#wait after clicking for the new page to load
browser.implicitly_wait(3)
#Find the view button in the navbar
view_btn = browser.find_element_by_id("View")
# click the view button
view_btn.click()
#find the Hours in the new nav bar
view_hrs_btn = browser.find_element_by_id("ViewHours")
# click it
view_hrs_btn.click()