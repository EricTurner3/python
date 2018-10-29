import requests
import os
import random
import string
import json
from urllib2 import urlopen

# Derived from https://github.com/engineer-man/youtube/blob/master/033/scam.py

chars = string.ascii_letters + string.digits + '!@#$%^&*()'

punctuation = ['.', '_', '']

mailproviders = ['@yahoo.com', '@gmail.com', '@aol.com', '@outlook.com', '@hotmail.com']


random.seed = (os.urandom(1024))

# Replace the spam URL, username field ID and password field ID to spam
url = 'URL_HERE'

ip_info = json.load(urlopen('http://www.geoplugin.net/json.gp'))
ip = ip_info['geoplugin_request']
countrycode = ip_info['geoplugin_countryCode']
print(' ')
print("Phishing URL: " + url)
print("My IP: " + ip + ' [' + countrycode + ']')

names = json.loads(open('names.json').read())
surnames = json.loads(open('surnames.json').read())
numbers = json.loads(open('numbers.json').read())
print(' ')
print('Loaded lists: ')
print('First names: ' + str(len(names)))
print('Surnames: ' + str(len(surnames)))
print('Numbers: ' + str(len(numbers)))
print(' ')

count = len(names) + 1
counter = 1
for name in names:

    # username will be lastname + random punctuation + first name + random numbers @ random mail provider
    # so smith.john1964@gmail.com or smith_john64@aol.com or smithjohn3@outlook.com are all possible to diversify
    username = random.choice(surnames).lower() + random.choice(punctuation) + name.lower() + str(random.choice(numbers)) + random.choice(mailproviders)
    password = ''.join(random.choice(chars) for i in range(8))

    print '[' + str(counter) + '/' + str(count) + '] sending username %s and password %s' % (username, password)
    counter += 1
    requests.post(url, allow_redirects=False, data={
        'username': username,
        'password': password
    })

