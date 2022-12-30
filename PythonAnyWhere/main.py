
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

choice, username = menu.displayMenu()
apiEndpoint, requestType = api.getEndpoint(apiId=choice)
apiToken = getApiToken(username)  # API token
header = {'Authorization': f'Token {apiToken}'}  # Authorization header

variableInEndpoint = tools.getVariablesFromFormat(apiEndpoint)
print(variableInEndpoint)

apiEndpoint = apiEndpoint.format(username=username)

print('Time after which request will made in seconds = 9\033[?25l', end="")
for i in range(9):
    sleep(1)
    print(f'\b{9-i}', end="")


response = request.get(
    url=f"{host+apiEndpoint}", headers=header)
if response.status_code == 200:
    print(type(response.json()))
    print(response.json())

    if isinstance(response.json(), list):
        for json in response.json():
            for key, value in json.items():
                print(key, ":", value)
            print()
    else:
        for key, value in response.json().items():
            print(key, ":", value)
else:
    print("Error:", response.status_code, response.reason)
    print("Response:", response.text)
