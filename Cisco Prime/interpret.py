import pandas as pd             # data analysis
import json                     # JSON manipulation

######################################
# Pandas - Interpret the data
######################################

# the data is all nested in clientsDTO, we need to parse it out into a dict we can read from
json_data = json.load(open('devices.json'))
deviceInfo = []
for element in json_data:
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
export.rename(columns={0: "username", 1: "count"})
export.to_csv('results.csv')
