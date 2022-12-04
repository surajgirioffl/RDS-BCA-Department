"""
    Module to handle all insert/update operation on database/table related to user IP.
"""

import mysql.connector as mysql


class IP:
    """
        * Class to store and update user's ip address and related information to the database.
    """

    def __createTable(self):
        self.cursor.execute(f"""
               CREATE TABLE IF NOT EXISTS {self.tableName}(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                ip CHAR(30) NOT NULL UNIQUE,
                city CHAR(30) NOT NULL,
                pin CHAR(10) NOT NULL,
                state CHAR(30) NOT NULL,
                country CHAR(30) NOT NULL,
                isp CHAR(30) NOT NULL,
                timeZone CHAR(40) NOT NULL,
                lastVisited DATETIME NOT NULL,
                visitCount INT NOT NULL DEFAULT 0
                );
               """)

    def __init__(self, host: str = "localhost", user: str = "root", port: int = 3306, password: str = "sadashiv@123", database: str = "rdsCollegeIpInfo", tableName: str = '', timeZoneForDatabase="Asia/Kolkata") -> None:
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
            self.__createTable()
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

    def insertInfo(self, ip: str, city: str, pin: str, state: str, country: str, isp: str, timeZone: str):
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

            @returns:
                * None
        """

        if self.__isIpExist(ip):  # if exists then update the info.
            self.cursor.execute(f"""
                                    UPDATE {self.tableName} SET
                                    isp='{isp}',lastVisited=(SELECT NOW()), visitCount=visitCount+1
                                    WHERE ip='{ip}';
                                """)
            # city='{city}', pin='{pin}', state='{state}', country='{country}', isp='{isp}', timeZone='{timeZone}', lastVisited=NOW(), visitCount=visitCount+1 #removing the things which is fixed (but change due to ip details given by api varies)
        else:  # if not exist then insert the info in the database.
            self.cursor.execute(f"""
                                    INSERT INTO {self.tableName}(ip, city, pin, state, country, isp, timeZone, lastVisited, visitCount)
                                    VALUES('{ip}', '{city}', '{pin}', '{state}', '{country}', '{isp}', '{timeZone}', (SELECT NOW()), 1)
                                """)


if __name__ == "__main__":
    IP().insertInfo(ip='11.23.29.33', city='Mumbai', pin='400001',
                    state='Maharashtra', country='India', isp='Jio', timeZone='Asia/Kolkata')
