import json
file = open("c:/Users/Eric/Documents/Python_testing/Police Data/agencies.json")
state = 'IN'
all_agencies = json.load(file)
state_agencies = []
state_agency_text = []

for agency in all_agencies["result"]["list"]:
    if agency["state_agencies"] == state:
        state_agencies.append(agency)
        state_agency_text.append('['+ agency["name"] + '](https://cityprotect.com/agency/' + str(agency['agencyPathName']) + ')' + ' - ' + agency['city'] + ', ' + agency['state_agencies'] + ' ' + agency['zip'])
        #print(agency["name"])

#print alphabetical agency names
state_agency_text.sort()
print('\n'.join(state_agency_text))

out_file = open("c:/Users/Eric/Documents/Python_testing/Police Data/in_agencies.json", "w")
json.dump(state_agencies, out_file, indent = 6)
out_file.close()
