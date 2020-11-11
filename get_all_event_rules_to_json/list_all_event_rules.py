import requests
import json

event_rules = []
# Update to match your API key
authorization_token = 'Eimm5UqyKbB3416Npa15'
pagerduty_session = requests.Session()
pagerduty_session.headers.update({
    'Authorization': 'Token token=' + authorization_token,
    'Accept': 'application/vnd.pagerduty+json;version=2'
})

response = pagerduty_session.get('https://api.pagerduty.com/event_rules')

outfile = open('event_rules.json', "w")
outfile.write(json.dumps(response.json(), indent=4, sort_keys=True))
outfile.close()
