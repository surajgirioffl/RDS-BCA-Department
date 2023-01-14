"""
    Module to handle all insert/update operation on database/table related to user IP.
"""

from os import environ
import mysql.connector as mysql


class IP:
    """
        * Class to store and update user's ip address and related information to the database.
    """

    def __init__(self, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSERNAME'), port: int = int(environ.get('DBPORT')), password: str = environ.get('DBPASSWORD'), database: str = "rdsbca$visitors", timeZoneForDatabase="Asia/Kolkata") -> None:
        """
            * This class is used to store user's ip address and other information in database.
            * Constructor of this class will create a table named 'userIp' if it doesn't exist.
            * And also create connection to the database and cursor.
        """

        # creating connection
        self.database = database
        try:
            self.conn = mysql.connect(
                host=f'{host}', user=f'{user}', password=f'{password}', port=port)
            self.cursor = self.conn.cursor(buffered=True)
            self.cursor.execute(f'USE {self.database}')

            # setting timezone for database
            try:
                self.cursor.execute(f"SET time_zone = '{timeZoneForDatabase}'")
            except Exception as e:
                print("Unable to set time_zone. Error code 1201")

            self.connectionStatus = True  # if connection is established then it will be true
            self.tables = {
                'visitors': 'visitors',
                'ip': 'ip_info',
                'visitors_info': 'visitors_info'
            }
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

    def __isIpExist(self, ip: str) -> bool | int:
        """
            * This method will check if the ip address is already present in the database.

            @Param:
                * ip: str -> Desired IP address.

            @returns:
                * int  -> Id of the ip address if ip address is present in the database
                * bool -> False if ip address is not present in the database.
        """

        self.cursor.execute(
            f"""-- sql
                SELECT Id FROM {self.tables['visitors']} 
                WHERE ip=%s
            """, (ip,))

        # if no data is fetched then ip is not present in the database.
        data = self.cursor.fetchall()
        if data == []:
            return False
        return data[0][0]

    def insertInfo(self, ip: str, city: str, pin: str, state: str, country: str, isp: str, timeZone: str, platform: str = "", screen: str = "", path: str = "", referrer: str = "", username: str = "") -> None:
        """
            Description:
                * This method will perform and update all information about the visitors in the database.
                * This method will insert the ip address and other information in the database.

            Args:
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
                * username: str -> Username of the client if logged in.
                * referrer: str -> Referrer of the client.

            Returns:
                * None
        """

        isIpExist = self.__isIpExist(ip=ip)

        if isIpExist:  # if exists then update the info.
            # ip is same. So, ip_info remain same. So, we are not updating ip_info.
            # but we are updating visitors_info and visitors table.
            # Same ip can have different platform, screen, path, referrer, username in different visit.
            # means user may open site in different platform, screen, path in different session.

            # id of the ip address in database.
            # return value of __isIpExist method (it is id of the ip address in database.)
            id = isIpExist

            # for visitors table (Update)
            self.cursor.execute(f"""-- sql
                                    UPDATE {self.tables['visitors']} 
                                    SET
                                        Username='{username}', LastVisited=(SELECT NOW()), VisitCount=VisitCount+1
                                    WHERE Ip='{ip}';
                                """)

            # for visitors_info table (Insert)
            # we will insert only if any of field is different from existing for that id(ip).
            # So, we will check the fields before inserting the data.
            # It will help to remove 100% duplicate rows.
            self.cursor.execute(f"""-- sql
                                    IF NOT EXISTS 
                                        (SELECT * FROM {self.tables['visitors_info']}
                                            WHERE Id={id} AND Platform='{platform}' AND Screen='{screen}' AND Path='{path}' AND Referrer='{referrer}'
                                        )
                                    THEN
                                        INSERT INTO {self.tables['visitors_info']}
                                            (Id, Platform, Screen, Path, Referrer)
                                        VALUES ({id}, '{platform}', '{screen}', '{path}','{referrer}')
                                    END IF
                                """)

        else:  # if ip does not exist then insert the info in the database.
            # for visitors table (Insert)
            self.cursor.execute(f"""-- sql
                                    INSERT INTO {self.tables['visitors']}
                                        (Ip, Username, LastVisited, VisitCount)
                                    VALUES('{ip}', '{username}', (SELECT NOW()), 1)
                                """)

            # for ip_info table (Insert)
            self.cursor.execute(f"""-- sql
                                INSERT INTO {self.tables['ip']}
                                    (Pin, City, State, Country, Isp, TimeZone)
                                VALUES('{pin}', '{city}', '{state}', '{country}', '{isp}', '{timeZone}')
                                """)

            # for visitors_info table (Insert)
            self.cursor.execute(f"""-- sql
                                INSERT INTO {self.tables['visitors_info']}
                                    (Id, Platform, Screen, Path, Referrer)
                                VALUES((SELECT Id FROM {self.tables['visitors']} WHERE Ip='{ip}'), '{platform}', '{screen}', '{path}', '{referrer}')
                                """)


if __name__ == "__main__":
    IP().insertInfo(ip='11.23.29.33', city='Mumbai', pin='400001',
                    state='Maharashtra', country='India', isp='Jio', timeZone='Asia/Kolkata', platform='Windows', screen='1920x1080', path="/home", referrer="https://google.com/", username="surajgirioffl")
