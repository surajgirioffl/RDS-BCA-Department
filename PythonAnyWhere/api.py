"""
    @file: api.py
    @author: Suraj Kumar Giri
    @init-date: 29th Dec 2022
    @last-modified: 29th Dec 2022
    
    @description:
        * Module to handle database related operations related to PythonAnyWhere API.
        
    @functions:
        * getEndpoints()
            - To fetch Api Endpoints based on different parameters from the database.
"""

import sqlite3 as sqlite

# See list of available API endpoints: https://help.pythonanywhere.com/pages/API
# some of endpoints with no/less arguments and more useful are listed in database.


class __API:
    def __init__(self, databaseName: str = 'PythonAnyWhere/api.db', tableName='ApiList'):
        """
            Description:
                - Constructor to create object of __API class.
                - It will establish connection with the database and create cursor object.

            Args:
                * databaseName (str, optional): 
                    - Name of the database file.
                    - Defaults to 'PythonAnyWhere/api.db'.
                * tableName (str, optional):
                    - Name of the table.
                    - Defaults to 'ApiList'.
        """
        self.databaseName = databaseName
        self.tableName = tableName
        try:
            self.conn = sqlite.connect(self.databaseName)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Error in established connection with the database:", e)
            self.isConnected = False
        else:
            # print("Connection established with the database.")
            self.isConnected = True

    def __del__(self):
        """
            Description:
                - Destructor.
                - It will close the connection with the database.
        """
        self.conn.close()

    def getEndpointById(self, apiId: int) -> tuple[str, str] | None:
        """
            Description:
                - To fetch the API endpoint and request type based on the endpoint id.

            Args:
               * apiId (int):
                    - API Id of the endpoint to be fetched. e.g. 2, 9, 12, 89 etc

            Returns:
                * tuple[str, str]:
                    - Tuple (endpoint, requestType) containing endpoint and request type.
                * None:
                    - If no endpoint found on given id or in case of any error.

        """
        if not self.isConnected:
            return None
        row = self.cursor.execute(f"""
                            SELECT Endpoint, RequestType from {self.tableName} WHERE id = {apiId}
                            """).fetchone()
        if row:  # means row is not None means contains a value (tuple)
            apiDict = {'endpoint': row[0], 'requestType': row[1]}
            return apiDict
        return None

    def getEndpointByKey(self, apiKey: str) -> tuple[str, str] | None:
        """
            Description:
                - To fetch the API endpoint and request type based on the endpoint key name.

            Args:
               * apiKey (str):
                    - API key of the endpoint to be fetched. e.g, 'cpuUsage', 'listConsole', 'listWebApp' etc

            Returns:
                * tuple[str, str]:
                    - Tuple (endpoint, requestType) containing endpoint and request type.
                * None:
                    - If no endpoint found on given API key or in case of any error.

        """
        if not self.isConnected:
            return None
        row = self.cursor.execute(f"""
                            SELECT Endpoint, RequestType from {self.tableName} WHERE key = '{apiKey}'
                            """).fetchone()
        if row:  # means row is not None means contains a value (tuple)
            apiDict = {'endpoint': row[0], 'requestType': row[1]}
            return apiDict
        return None

    def getEndpointParameters(self, apiId: int | None = None, apiKey: str | None = None, tableName: str = 'Parameters') -> list | None:
        """
            Description:    
                - To fetch the parameters of the API endpoint based on the endpoint id or key name.
                - Use only for those endpoints which require parameters. And most endpoints which is of GET type doesn't require any parameters. So, use it only for those endpoints which are of POST, PUT, PATCH etc type.

            Args:
                * apiId (int | None, optional): 
                    - API Id of the endpoint to be fetched. e.g. 2, 9, 12, 89 etc
                    - Defaults to None.
                * apiKey (str | None, optional):
                    - API key of the endpoint to be fetched. e.g, 'cpuUsage', 'listConsole', 'listWebApp' etc
                    - Defaults to None.
                * tableName (str, optional):
                    - Table Name in which the parameters of the endpoints are stored.
                    - Defaults to 'Parameters'.
                - If both apiId and apiKey are None, then it will return None.

            Returns:
                * list
                    - List of parameters of the endpoint.
                * None
                    - If no parameters are found for the given endpoint id/key or in case of any error.
                    - If no arguments passed.
                    - If unable to establish connection with the database.
                    - Any other error.
        """
        # if no argument is passed
        if apiId is None and apiKey is None:
            print("Error: Both apiId and apiKey are None.")
            print("Please pass at least one argument.")
            return None

        # if database is not connected
        if not self.isConnected:
            return None

        if apiId is None:
            apiId = self.cursor.execute(
                f"SELECT id FROM {self.tableName} WHERE key = '{apiKey}'").fetchone()
            if apiId is None:  # if no apiId found for given apiKey
                return None
            apiId = apiId[0]

        row = self.cursor.execute(f"""
                                  SELECT Params from {tableName} WHERE id={apiId}
                                  """).fetchone()
        if row is None:  # if no parameters are found
            return None
        parameters = row[0].split(',')

        # after splitting the parameters, some of list items may contain spaces. Let's trim them.
        for i in range(len(parameters)):
            parameters[i] = parameters[i].strip()
        return parameters


def getEndpoint(apiId: int | None = None, apiKey: str | None = None) -> tuple[str, str, list | None] | None:
    """
        Description:
            - To fetch Api Endpoints based on different parameters from the database.
        Args:
            * apiId (int | None, optional): 
                - Api Id of the endpoint to be fetched. e.g. 2, 9, 12, 89 etc
                - Defaults to None.
            * apiKey (str | None, optional): 
                - API key of the endpoint to be fetched. e.g, 'cpuUsage', 'listConsole', 'listWebApp' etc
                - Defaults to None.
            * Both are specified optional but one of them are compulsory otherwise it will return None.

        Returns:
            * tuple[str, str, list | None]:
                - tuple containing endpoint, requestType and parameters.
                    - endpoint in string.
                    - request type in string.
                    - parameter in list or None in case of no parameters found.
            * None
                - if no endpoint is found or in case of any error or no argument is passed.
    """
    if apiId is None and apiKey is None:
        print("Error: Both apiId and apiKey are None.")
        print("Please pass at least one argument.")
        return None
    api = __API()
    if apiId is not None:
        apiDict = api.getEndpointById(apiId)
    elif apiKey is not None:
        apiDict = api.getEndpointByKey(apiKey)

    if apiDict is not None:
        if apiDict['requestType'] == 'GET':
            # because GET request required no parameters.
            return apiDict['endpoint'], apiDict['requestType'], None
        return apiDict['endpoint'], apiDict['requestType'], api.getEndpointParameters(apiId, apiKey)

    return None


if __name__ == '__main__':
    api = __API()
    print(api.getEndpointById(2))
    print(api.getEndpointByKey('cpuUsage'))
