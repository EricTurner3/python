from datetime import datetime   # for time tracking
import requests                 # for making API calls
import json                     # decode the JSON response
import urllib3                  # disable warnings
import pandas as pd             # data analysis

# shut up the insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


######################################
# Cisco Prime Collect Devices
######################################

# capture the start of the script
startTime = datetime.now()

# when paginating, update the script each time to the new value to grab the next page
# so page 2 will start at 1000, page 3 will be 2000 .etc
device_count = 0
maxResults = 1000 # maximum amount of results currently is 1000 per page by the server settings

#placeholder for devices with usernames
devices = []


def retrieveDevices(startingNumber, maxNumber):
    # These items are confidential so I put them in key files so they are loaded in externally. 
    # Helps when i push this code to GitHub, I can keep our information out of the internet
    server = str(open('prime_server.key').readline())
    apikey = str(open('prime_credentials.key').readline())

    # .json provides JSON format 
    url = server + "/webacs/api/v2/data/Clients.json"
    # .full provides the full details of the clients (mac address, comnnected username, device type.etc)
    querystring = {".full":"true",".firstResult":startingNumber,".maxResults":maxNumber}

    headers = {
        'Authorization': apikey,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    

    # grab the response manually first
    response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
    # response.json() returns the json

    # grab all devices that have connected via a username and add it to the devices list
    for i in response.json()['queryResponse']['entity']:
        if 'userName' in i["clientsDTO"]:
            devices.append(i)
    # print("Devices Pulled this round: " + str(len(response.json()['queryResponse']['entity'])))
    # print("Devices with Usernames: " + str(len(devices)))
    # return total count (will only be used once in first query)
    return [len(response.json()['queryResponse']['entity']), response.json()['queryResponse']['@count']]

# start with 0
print('Retrieving Devices from Cisco Prime...')
device_count, total = retrieveDevices(0, maxResults)
print(str(device_count) + '/' + str(total))
while device_count < total:
    # we will not use the total again, so changed it to unused (we only need the first int)
    device_count = retrieveDevices(device_count, maxResults)[0] + device_count
    print(str(device_count) + '/' + str(total))

print("Total Devices on Network: " + str(total))
print(str(len(devices)) + " devices connected with a username")
# dump results to file
print('Exported to file: ./devices.json')
with open('devices.json', 'w') as results_file:
    json.dump(devices, results_file)

######################################
# Pandas - Interpret the data
######################################
print('Analyzing data...')
# the data is all nested in clientsDTO, we need to parse it out into a dict we can read from
#json_data = json.load(open('devices.json'))
deviceInfo = []
for element in devices:
    deviceInfo.append(element['clientsDTO'])
# now convert back to JSON
new_json = json.dumps(deviceInfo)
# insert into a dataframe
df = pd.read_json(new_json)

#print(df.head())
group_by_username = df.groupby('userName')['userName'].count()
#print(group_by_username.sort_values(ascending=False))
# export to csv
export = pd.DataFrame(group_by_username.sort_values(ascending=False))
export.to_csv('results.csv')
print('Exported ./results.csv file of devices connected, sorted by username')

# print the elapsed time
print('Script Elapsed Time: ')
print(datetime.now() - startTime)