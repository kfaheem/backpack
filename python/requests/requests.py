# The following are dummy examples of post & get requests with headers & body

import requests
import json

# Get Bearer token for your App ===============================================
headers1 = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "no-cache"
}

body1 = {
    "client_id": "",
    "client_secret": "",
    "grant_type": "client_credentials"
}

response1 = requests.post(url="", headers=headers1, data=body1, verify=False)

# ===============================================

# Get Authorization using bearer tokens ===============================================

headers2 = {
    "Authorization": "Bearer" + "Bearer token from response1",
    "Content-Type": "application/json;v={}",
    "Accept": "application/json;v={}"
}

body2 = {
    "accessType": "Custom",
    "": ""
}

response2 = requests.post(url="", headers=headers2, data=body2, verify=False)

response3 = requests.get(url="", headers=headers1, verify=False)

# HTTPBasicAuth ===============================================

from requests.auth import HTTPBasicAuth

username = ""
password = ""
response4 = requests.get(url="", headers="", data="", auth=HTTPBasicAuth(username, password))

