
"""
    @file: main.py
    @author: Suraj Kumar Giri
    @init-date: 29th Dec 2022
    @last-modified: 30th Dec 2022

    @description:
        * Module deals with all required APIs of PythonAnyWhere.
"""

import requests as request
from credentials import getApiToken, host
import menu
import api
import tools
from time import sleep

while True:
    # Display menu and get user's choice and username
    choice, username = menu.displayMenu()

    # Get API endpoint and request type and other required credentials
    apiEndpoint, requestType = api.getEndpoint(apiId=choice)
    apiToken = getApiToken(username)  # API token
    header = {'Authorization': f'Token {apiToken}'}  # Authorization header

    # fetching variables from endpoint
    variableInEndpoint = tools.getVariablesFromFormat(apiEndpoint)
    print("Variable in API endpoint: ", variableInEndpoint)

    # replacing variables in endpoint with desired credentials
    isMoreThanOneVariable = False
    continueToMenu = False
    if len(variableInEndpoint) == 1:  # means only username is required
        apiEndpoint = apiEndpoint.format(username=username)
        break
    else:
        variablesValue = {}
        for variable in variableInEndpoint:
            if variable == 'username':
                variablesValue[variable] = username
            else:
                isMoreThanOneVariable = True
                value = input(f"\nEnter {variable} (Press # for menu): ")
                if value == '#':
                    continueToMenu = True
                    break
                else:
                    variablesValue[variable] = value
    if continueToMenu:
        continue
    break

# replacing variables in endpoint with desired credentials in case of more than one variable in format string
if isMoreThanOneVariable:
    apiEndpoint = apiEndpoint.format(**variablesValue)

# Displaying API endpoint and request type and other details to user for verification
print(f"""\n
      Username: {username}
      Endpoint: {apiEndpoint}
      Request: {requestType}
      """)

# Sleep for 5 seconds before making request for user to cancel request  or verify the credentials before making request
print('Time after which request will made in seconds = 5\033[?25l', end="")
for i in range(5):
    sleep(1)
    print(f'\b{5-i-1}', end="")

#----------------- Making request -----------------#
# source: https://requests.readthedocs.io/en/latest/api/
try:
    response = request.request(method=requestType,
                               url=f"{host+apiEndpoint}", headers=header)  # we will not use request.get() because request type can be POST, PUT, DELETE etc.
except Exception as e:
    print("\nError in request:", e)
    exit(-1)
else:
    print("\nRequest successful")

print("\nStatus Code:", response.status_code)

if response.status_code not in [200, 201, 202, 204]:
    print("\nError:", response.status_code, response.reason)
    print("Response:", response.text)
    exit(-1)

print("\n----------------------------- Response Header--------------------------------")
print("Response Header Type:", type(response.headers), end="\n\n")
for key, value in response.headers.items():
    print(key, ":", value)
print()

print("\n----------------------------- Response Content--------------------------------")

# if response is json then print it in readable format else print as it is
if response.headers['Content-Type'] == 'application/json':
    print("\nResponse type:", type(response.json()))
    # print(response.json())

    if isinstance(response.json(), list):
        for json in response.json():
            if isinstance(json, dict):
                for key, value in json.items():
                    print(key, ":", value)
            else:
                print(json)
            print()
    elif isinstance(response.json(), dict):
        for key, value in response.json().items():
            print(key, ":", value)
    else:
        print(response.json())

else:
    print("\nResponse type:", type(response.content))
    print(response.content)

response.close()  # closing response
print("\n")
