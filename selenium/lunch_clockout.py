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
leave_btn = browser.find_element_by_xpath("//input[@value='Leave On Break']")
leave_btn.click()

#wait after clicking for the new page to load
browser.implicitly_wait(3)

#Find the continue button and click it
cont_btn = browser.find_element_by_xpath("//input[@value='Continue']")
#cont_btn.click()
browser.implicitly_wait(3)
# now open up a timer and start it
browser.get('https://vclock.com/set-timer-for-1-hour/')
start_btn = browser.find_element_by_id("btn-resume")
start_btn.click()

