import requests
from requests_ntlm import HttpNtlmAuth

requests.packages.urllib3.disable_warnings()

#Set up necessary headers comma separated
xrf = 'iX83QmNlvu87yyAB'
headers = {'X-Qlik-xrfkey': xrf,
"Content-Type": "application/json",
"User-Agent":"Windows"}

#Set up user credentials
user_auth = HttpNtlmAuth('SEA\\qdev','Bic.122020')

#add xrfkey to URL
url = 'https://qliksense.seatrasformatori.it/qrs/app/full?xrfkey={}'.format(xrf)

#Call the endpoint to get the list of Qlik Sense apps
resp = requests.get(url,headers = headers,verify=False,auth=user_auth)

if resp.status_code != 200:
    # Returns an error if something went wrong.
    raise ApiError('GET /qrs/app/full {}'.format(resp.status_code))
for app in resp.json():
    print('{1} {0}'.format(app['id'], app['name']))

