"""
    Module to handle all insert/update operation on database/table related to user IP.
"""

from os import environ
import mysql.connector as mysql


class IP:
    """
        * Class to store and update user's ip address and related information to the database.
    """

    def __init__(self, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSER'), port: int = int(environ.get('DBPORT')), password: str = environ.get('DBPASSWORD'), database: str = "visitors", timeZoneForDatabase="Asia/Kolkata") -> None:
        """
            * This class is used to store user's ip address and other information in database.
            * Constructor of this class will create a table named 'userIp' if it doesn't exist.
            * And also create connection to the database and cursor.
        """

        # creating connection
        self.database = database
        try:
            self.conn = mysql.connect(host=f'{host}', user=f'{user}',
                                      password=f'{password}', port=port)
            self.cursor = self.conn.cursor(buffered=True)
            self.cursor.execute(f'USE {self.database}')
            self.cursor.execute(
                f"SET time_zone = '{timeZoneForDatabase}'")
            self.connectionStatus = True  # if connection is established then it will be true
            if tableName == '':
                self.tableName = 'userIp'
            else:
                self.tableName = tableName
            print('Connection with database established.')
        except Exception as e:
            # if connection is not established then set connectionStatus to False.
            self.connectionStatus = False
            print('Connection with database not established. Error code 1200')
            print("Exception: ", e)

    def __del__(self):
        if self.connectionStatus:
            self.conn.commit()
            self.conn.close()

    def __isIpExist(self, ip: str) -> bool:
        """
            * This method will check if the ip address is already present in the database.

            @Param:
                * ip: str -> Desired IP address.

            @returns:
                * bool -> True if ip address is present in the database, else False.
        """

        self.cursor.execute(
            f'SELECT * FROM {self.tableName} WHERE ip=%s', (ip,))

        # if no data is fetched then ip is not present in the database.
        if self.cursor.fetchall() == []:
            return False
        return True

    def insertInfo(self, ip: str, city: str, pin: str, state: str, country: str, isp: str, timeZone: str, platform: str = "", screen: str = "", path: str = "") -> None:
        """
            * This method will insert the ip address and other information in the database.

            @Param:
                * ip: str -> Desired IP address.
                * city: str -> City name.
                * pin: str -> Pin code.
                * state: str -> State name.
                * country: str -> Country name.
                * isp: str -> Internet Service Provider.
                * timeZone: str -> Time zone.
                * platform: str -> Platform name of client like Windows, Linux, Mac, etc.
                * screen: str -> Screen resolution of client.
                * path: str-> Path from which the request is made.

            @returns:
                * None
        """

        if self.__isIpExist(ip):  # if exists then update the info.
            self.cursor.execute(f"""
                                    UPDATE {self.tableName} SET
                                    isp='{isp}',lastVisited=(SELECT NOW()), visitCount=visitCount+1, platform='{platform}', screen='{screen}', path='{path}'
                                    WHERE ip='{ip}';
                                """)
            # city='{city}', pin='{pin}', state='{state}', country='{country}', isp='{isp}', timeZone='{timeZone}', lastVisited=NOW(), visitCount=visitCount+1 #removing the things which is fixed (but change due to ip details given by api varies)
        else:  # if not exist then insert the info in the database.
            self.cursor.execute(f"""
                                    INSERT INTO {self.tableName}(ip, city, pin, state, country, isp, timeZone, lastVisited, visitCount, platform, screen, path)
                                    VALUES('{ip}', '{city}', '{pin}', '{state}', '{country}', '{isp}', '{timeZone}', (SELECT NOW()), 1, '{platform}', '{screen}', '{path}')
                                """)


if __name__ == "__main__":
    IP().insertInfo(ip='11.23.29.33', city='Mumbai', pin='400001',
                    state='Maharashtra', country='India', isp='Jio', timeZone='Asia/Kolkata', platform='Windows', screen='1920x1080', path="/home")
