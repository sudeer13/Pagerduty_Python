#!/usr/bin/python

#   Title       : Get PagerDuty Services Keys
#   Document(s) : Get_PagerDuty_Services_Keys.py
#	Version 	: 1.0
#   Update  	: This is the first version
#	Date    	: 012/08/2019
#   Description : Saves PagerDuty Services Service Names, Service IDs, Escalation Policy IDs, & ServiceNow Webhook IDs
#                 as an Microsoft Excel file so data can be manually added to ServiceNow once the PagerDuty app is installed.
#   Author      : Sudeer Vadali

# Modules Used
import os
import json
import requests
import sys
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

# Help Message
message = """
Example usage:
    ./Get_PagerDuty_Services_Keys.py -k <PagerDuty v2 API Key>
    ./Get_PagerDuty_Services_Keys.py -key <PagerDuty v2 API Key>   
"""
# Passing arguments. Either help (-h) or the PagerDuty v2 API Key (-k)
if len(sys.argv) == 1:
    print(message)
    sys.exit(2)
elif sys.argv[1] not in ('-h', '--help', '-k', '--key'):
    print(message)
    sys.exit(2)

elif sys.argv[1] in ('-h', '--help'):
    print(message)
    sys.exit(2)

elif sys.argv[1] in ('-k', '--key') and len(sys.argv) == 3:
    api_key = sys.argv[2]
else:
    print(message)
    sys.exit(2)

# Override default limit and offset. See: https://v2.developer.pagerduty.com/docs/pagination
limit = 100
offset = 0

# PagerDuty REST API details
api_endpoint   = 'https://api.pagerduty.com/'
api_services   = 'services'
api_extensions = 'extensions'
api_variables  = '?limit=' + str(limit) + '&offset=' + str(offset)
api_headers    = {'Authorization': 'Token token=' + api_key, 'Accept': 'application/vnd.pagerduty+json;version=2'}

def get_request(_endpoint,_fucntion,_variable,_headers):

    response = requests.get(_endpoint + _fucntion + _variable, headers=_headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        print('[!] PagerDuty REST API Connection Failure')
        sys.exit(2)

# Create dictionary where keys gets stored
keys_dict =	{
  "Service Name": {},
  "Service ID": {},
  "Escalation Policy ID": {},
  "ServiceNow Webhook ID": {}
}

# Get extensions details(json)
pg_extensions = get_request(api_endpoint,api_extensions,api_variables,api_headers)

# Get ServiceNow extension webhook key
if pg_extensions is not None:

    for item in pg_extensions['extensions']:

        # Make sure extension is ServiceNow
        if 'snow_user' in item['config']:
            sn_webhook_key = item['id'].encode("utf-8")

else:
    print('[!] No Extensions Found')
    sys.exit(2)

# Get Services details (json)
pg_services = get_request(api_endpoint,api_services,api_variables,api_headers)

# Add Services details to dictionary
if pg_services is not None:

    i = 0
    for item in pg_services['services']:
        keys_dict["Service Name"][i] = item['name'].encode("utf-8")
        keys_dict["Service ID"][i] = item['id'].encode("utf-8")
        keys_dict["Escalation Policy ID"][i] = item['escalation_policy']['id'].encode("utf-8")
        keys_dict["ServiceNow Webhook ID"][i] = sn_webhook_key
        i = i+1

else:
    print('[!] No Services Found')
    sys.exit(2)

# Convert key dictionary into pretty Excel file
wb = Workbook()
ws = wb.active
ws.title = "PagerDuty Services & Keys"

ws.append(list(keys_dict.keys()))

for i in range(0, len(keys_dict["Service Name"])):
    row = [keys_dict["Service Name"][i], keys_dict["Service ID"][i], keys_dict["Escalation Policy ID"][i], keys_dict["ServiceNow Webhook ID"][i]]
    ws.append(row)

cell_range = 'A1:D' + str(len(keys_dict["Service Name"]) + 1)

tab = Table(displayName="Table1", ref=cell_range)

style = TableStyleInfo(name="TableStyleMedium16", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)

tab.tableStyleInfo = style
ws.add_table(tab)

ws.column_dimensions['A'].width = 50
ws.column_dimensions['B'].width = 20
ws.column_dimensions['C'].width = 20
ws.column_dimensions['D'].width = 20

wb.save('PagerDuty_Services_Keys.xlsx')
