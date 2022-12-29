import requests as request
from credentials import username, apiToken, host
header = {'Authorization': f'Token {apiToken}'}  # Authorization header

# See list of available API endpoints: https://help.pythonanywhere.com/pages/API
# some of GET endpoints with no arguments are listed below:
apiEndPoints = {
    'alwaysOn': f'/api/v0/user/{username}/always_on/',
    'consoles': f'/api/v0/user/{username}/consoles/',
    'cpu': f'/api/v0/user/{username}/cpu/'
}


response = request.get(
    url=f"{host+apiEndPoints['cpu']}", headers=header)
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
