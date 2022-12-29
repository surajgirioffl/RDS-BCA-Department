import sqlite3 as sqlite

# See list of available API endpoints: https://help.pythonanywhere.com/pages/API
# some of endpoints with no/less arguments and more useful are listed in database.


class __API:
    def __init__(self, databaseName: str = 'PythonAnyWhere/api.db', tableName='ApiList'):
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
        self.conn.close()

    def getEndpointById(self, apiId: int) -> tuple[str, str] | None:
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
        if not self.isConnected:
            return None
        row = self.cursor.execute(f"""
                            SELECT Endpoint, RequestType from {self.tableName} WHERE key = '{apiKey}'
                            """).fetchone()
        if row:  # means row is not None means contains a value (tuple)
            apiDict = {'endpoint': row[0], 'requestType': row[1]}
            return apiDict
        return None


def getEndpoint(apiId: int | None = None, apiKey: str | None = None) -> tuple[str, str] | None:
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
        return apiDict['endpoint'], apiDict['requestType']
    return None


if __name__ == '__main__':
    api = __API()
    print(api.getEndpointById(2))
    print(api.getEndpointByKey('cpuUsage'))
