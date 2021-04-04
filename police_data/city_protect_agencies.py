import requests
import json

url = "https://ce-portal-service.commandcentral.com/api/v1.0/public/agencies"
print("Fetching agencies from {}".format(url))

payload="{\"limit\":15000,\"offset\":0,\"geoJson\":{\"type\":\"MultiPolygon\",\"coordinates\":[[[[-180,90],[0,90],[0,-90],[-180,-90],[-180,90]]],[[[0,90],[180,90],[180,-90],[0,-90],[0,90]]]]},\"projection\":false,\"propertyMap\":{}}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

json_resp = json.loads(response.text)

# 1092 agencies
print("Total Fetched: " + str(len(json_resp['result']['list'])))

bulk_y = 0
bulk_n = 0

for agency in json_resp["result"]["list"]:
    if agency['bulkDownload']: bulk_y += 1
    else: bulk_n += 1

# 355 yes, 722 no
print("Agencies with Bulk Download: {} Yes and {} No".format(bulk_y, bulk_n))
