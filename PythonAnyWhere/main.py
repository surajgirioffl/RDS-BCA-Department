
"""
    @file: main.py
    @author: Suraj Kumar Giri
    @init-date: 29th Dec 2022
    @last-modified: 31st Dec 2022

    @description:
        * Module deals with all required APIs of PythonAnyWhere.
"""

from os import system
from sys import platform
import requests as request
from credentials import getApiToken, host
import menu
import api
import tools
from time import sleep


class API:
    """
        @description:
            Class deals with all required APIs of PythonAnyWhere.

        @methods:
            * displayMenu()
                - Display menu and get user's choice and username
            * setCredentials()
                - Set credentials like API endpoint, request type, token, headers etc.
            * setFormatVariables()
                - To set variable (query parameters) in API endpoint URL.
            * displayEndpointDetails()
                - Display all details related to the API endpoint for verification.
            * makeRequest()
                - To make request to the API endpoint.
            * showResponseStatus()
                - To show the response status of the request.
            * printResponseHeader()
                - To print the response header of the request.
            * printResponseContent()
                - To print the response content of the request.
    """

    def __del__(self) -> None:
        ...

    def displayMenu(self) -> None:
        """
            Description:
                - Display menu and get user's choice and username

            Returns:
                * None
        """
        self.choice, self.username = menu.displayMenu()

    def setCredentials(self) -> None:
        """
            Description:
                - To set credentials like API endpoint, request type, token, headers etc.
                - Also get parameters data from user if required in the API endpoint.
                - Perform some basic checks on the data entered by user.

            Returns:
                * None
        """
        # Get API endpoint and request type and other required credentials
        self.apiEndpoint, self.requestType, parameters = api.getEndpoint(
            apiId=self.choice)

        # Get parameters data from user if required by the API endpoint (Normally in POST, PUT, PATCH request data is required)
        self.data = parameters  # if parameters is None then self.data will be None
        if parameters is not None:
            self.data = {}
            print('\nParameters are required for this API endpoint.')
            for key in parameters:
                while True:
                    self.data[key] = input(f"Enter {key}: ")
                    # if user press enter without entering any value
                    if (self.data[key]) == "":
                        print("Empty value not allowed. Please write again..")
                        continue
                    # in case of sending input to console. We need to add newline character at the end of the input. (Only for API Id 5)
                    elif list(self.data.keys())[0] == 'input':
                        self.data[key] = self.data[key]+'\n'
                        break
                    break

        # API token
        apiToken = getApiToken(self.username)
        # Authorization header
        self.header = {'Authorization': f'Token {apiToken}'}

    def setFormatVariables(self) -> bool:
        """
            Description:
                - To set variables (query parameters) in API endpoint URL.

            Returns:
                - True:
                    - if everything is fine and variables are replaced in endpoint URL.
                - False:
                    - If user want to go back to main menu.
        """
        # fetching variables from endpoint
        variableInEndpoint = tools.getVariablesFromFormat(self.apiEndpoint)
        print("\nVariables in API endpoint: ", variableInEndpoint)

        # replacing variables in endpoint with desired credentials
        if len(variableInEndpoint) == 1:  # means only username is required
            self.apiEndpoint = self.apiEndpoint.format(username=self.username)
            return True
        else:  # means more than one variables are to be replaced in the endpoint url
            variablesValue = {}
            for variable in variableInEndpoint:
                if variable == 'username':
                    variablesValue[variable] = self.username
                else:
                    while True:
                        value = input(
                            f"\nEnter {variable} (Press # for menu): ")
                        if value == '#':
                            return False
                        elif value == "":  # if user press enter without entering any value
                            print("Empty value not allowed. Please write again..")
                            continue
                        else:
                            variablesValue[variable] = value
                            break

        # replacing variables in endpoint with desired credentials in case of more than one variable in format string
        self.apiEndpoint = self.apiEndpoint.format(**variablesValue)
        return True

    def displayEndpointDetails(self) -> None:
        """ 
            Description:
                - Displaying API endpoint and request type and other details to user for verification

            Returns:
                - None
        """
        print(f"""\n
              Username: {self.username}
              Endpoint: {self.apiEndpoint}
              Request: {self.requestType}
              """)
        if self.data is not None:
            print("              Parameters: ", self.data)

    def makeRequest(self) -> bool:
        """
            Description:
                - To make request to the API endpoint.

            Returns:
                * True:
                    - if request was successful
                * False:
                    - if request failed or any error due to which request was unsuccessful.
        """
        #----------------- Making request -----------------#
        # source: https://requests.readthedocs.io/en/latest/api/
        try:
            self.response = request.request(method=self.requestType,
                                            url=f"{host+self.apiEndpoint}", headers=self.header, data=self.data)  # we will not use request.get() because request type can be POST, PUT, DELETE etc.
        except Exception as e:
            print("\nError in request:", e)
            return False
        else:
            print("\nRequest successful")
            return True

    def showResponseStatus(self) -> bool:
        """
            Description:
                - To show the response status of the request.

            Returns:
                * True:
                    - if response status code is 200, 201, 202, 204
                * False:
                    - if response status is other than above mentioned status codes.
        """
        print("\n----------------------------- Response Status--------------------------------")
        print("Status Code:", self.response.status_code)

        if self.response.status_code not in [200, 201, 202, 204]:
            print("\nError:", self.response.status_code, self.response.reason)
            print("Response:", self.response.text)
            print(
                "----------------------------------- End--------------------------------------")
            return False
        return True

    def printResponseHeader(self):
        """
            Description:
                - To print the response headers.

            Returns:
                * None
        """
        print("\n----------------------------- Response Header--------------------------------")
        print("Response Header Type:", type(self.response.headers), end="\n\n")
        for key, value in self.response.headers.items():
            print(key, ":", value)
        print()

    def printResponseContent(self):
        """
            Description:
                - To print the response content of any type to user.

            Returns:
                * None
        """
        print("\n----------------------------- Response Content--------------------------------")

        # if response is json then print it in readable format else print as it is
        if self.response.headers['Content-Type'] == 'application/json':
            print("Response type:", type(self.response.json()))
            # print(response.json())

            if isinstance(self.response.json(), list):
                for json in self.response.json():
                    if isinstance(json, dict):
                        for key, value in json.items():
                            print(key, ":", value)
                    else:
                        print(json)
                    print()
            elif isinstance(self.response.json(), dict):
                for key, value in self.response.json().items():
                    print(key, ":", value)
            else:
                print(self.response.json())

        else:
            print("\nResponse type:", type(self.response.content))
            print(self.response.content)
        print("----------------------------------- End----------------------------------------")

    def close(self) -> None:
        """
            Description:
                To close the response object.

            Returns:
                * None
        """
        self.response.close()  # closing response
        print("\n")


class Terminal:
    """
        @description:
            - class to perform different operation related to terminal of system.
            - Can be use in both windows and linux.

        @methods (can be used with class name -> @staticmethod)):
            * pause()
                - To pause the terminal until user press any key.
            * sleepTimer()
                - To sleep the terminal for specified seconds along with displaying countdown timer.
    """

    def pause() -> None:
        """
            Description:
                - To pause the terminal until user press any key.

            Returns:
                - None
        """
        if platform == 'win32':
            system('pause')
        else:
            system('read -n1 -r -p "Press any key to continue..."')

    @staticmethod
    def sleepTimer(self, timeout: int = 5) -> None:
        """
            Description:
                - To sleep the terminal for specified seconds along with displaying countdown timer.

            Returns:
                - None
        """
        # Sleep for specified seconds before making request for user to cancel request or verify the credentials before making request
        print(
            f'Time after which request will made in seconds = {timeout}\033[?25l', end="")
        for i in range(timeout):
            sleep(1)
            print(f'\b{timeout-i-1}', end="")
        print("\033[?25h")


def main() -> None:
    """
        Description:
            - Main menu to handle all API related operations in systematic manner 
            - Operations like setting credentials, setting format variables, making request, showing response status, printing response header and content using API class.
    """
    api = API()
    while True:
        api.displayMenu()
        api.setCredentials()
        if api.setFormatVariables():
            api.displayEndpointDetails()
            Terminal.sleepTimer(5)
            if api.makeRequest():
                if api.showResponseStatus():
                    api.printResponseHeader()
                    api.printResponseContent()
                    Terminal.pause()
                    api.close()
                    continue
                else:
                    print(
                        "\nResponse is not satisfactory. Something went wrong either client side or server side.")
                    print("Press any key to main menu")
                    Terminal.pause()
                    api.close()
                    continue
            else:
                print("\nSomething went wrong while making request.")
                print("Press any key to main menu")
                Terminal.pause()
                continue
        else:
            print('\nUser want to go to Main Menu or Something went wrong in variable replacement in format string..')
            print("Press any key to main menu")
            Terminal.pause()
            continue


if __name__ == '__main__':
    main()
