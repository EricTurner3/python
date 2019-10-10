import requests
import json
import pandas as pd

# Creston -    3703fb29-4581-47d0-9859-25a7c69da004
# Stonybrook - e938efa1-acf2-4638-aa48-65a41aa8889a

df = pd.DataFrame(columns=['School', 'Season', 'Sport', 'Link'])

schools = ['3703fb29-4581-47d0-9859-25a7c69da004', 'e938efa1-acf2-4638-aa48-65a41aa8889a']
for x in schools:
    base_url = 'https://api.eventlink.com/?a=GetAllByOrganizationID&id=' + x + '&m=Team'
    data = requests.get(base_url).json()
    
    for x in data['Data']:
        event_url = 'https://widget.eventlink.com/sport-schedule?c=%5B%22'+x['GameCalendarID'] +'%22%5D&o='+x['OrganizationID']+'&z=America%2FNew_York&d=false'
        # print(event_url +  ' - ' + x['Organization']['Title'] + ' - '  + x['Gender'] + ' ' + x['Title']+ '[' + x['Season'] + ']')
        df = df.append({'School': x['Organization']['Title'], 'Season': x['Season'], 'Sport': x['Gender'] + ' ' + x['Title'], 'Link': event_url }, ignore_index=True)
    
df.to_csv('links.csv', index=False)
    