"""
    @file: dynamic_contents.py
    @author: Suraj Kumar Giri
    @init-date: 18th Jan 2023
    @last-modified: 18th Jan 2023

    @description:
        * Module to handle database related operations related to serving dynamic contents on the website.
"""

from os import environ
import mysql.connector as mysql


class DynamicContents:
    """
        Description:
            * Class to handle database related operations related to serving dynamic contents on the website.
    """

    def __init__(self, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSERNAME'), port: int = int(environ.get('DBPORT')) if environ.get('DBPORT') is not None else 3306, password: str = environ.get('DBPASSWORD'), database: str = "rdsbca$dynamic_contents", timeZoneForDatabase="Asia/Kolkata") -> None:
        """
            Description:
                - Class to handle database related operations related to serving dynamic contents on the website
                - Constructor of the class DynamicContents
            Args:
                * host (str, optional): 
                    - Host of the database.
                    - Defaults to hostname set in the environment for the database.
                * user (str, optional):
                    - Username of the database.
                    - Defaults to username set in the environment for the database.
                * port (int, optional): 
                    - Port of the database.
                    - Defaults to port set in the environment for the database.
                * password (str, optional): 
                    - Password of the database.
                    - Defaults to password set in the environment for the database.
                * database (str, optional): 
                    - Name of the database.
                    - Defaults to rdsbca$dynamic_contents
                * timeZoneForDatabase (str, optional):
                    - TimeZone for the current session of the database (May not work in Windows).
                    - Defaults to "Asia/Kolkata".

            Returns:
                * None
        """
        try:
            # establishing connection and creating cursor object
            self.conn = mysql.connect(
                host=f'{host}', user=f'{user}', password=f'{password}', port=port)
            self.cursor = self.conn.cursor(buffered=True)

            # using database as per the parameter
            self.cursor.execute(f'USE {database}')
        except Exception as e:
            print(
                f"Unable to establish connection with the database ({database}). Error code 1300")
            print("Exception: ", e)
            # if connection is not established then set connectionStatus to False.
            self.connectionStatus = False
        else:
            # if connection is established then set connectionStatus to True.
            self.connectionStatus = True
            print(f"Connection with database established ({database}).")

            # setting the timezone for database
            try:
                self.cursor.execute(f"SET time_zone = '{timeZoneForDatabase}'")
            except Exception as e:
                print("Unable to set time_zone. Error code 1301")

            # listing all the tables in the database
            self.tables = {
                'notice': 'notice',
                'credits': 'credits',
                'sources': 'sources'
            }

    def __del__(self) -> None:
        """
            Description:
                * Destructor
                * Commit and close the session.
            Returns:
                * None
        """
        if self.connectionStatus:
            self.conn.commit()
            self.conn.close()

    def notice(self, index: int = 0) -> tuple | None:
        """
            Description:
                - Method to fetch latest or desired notice from the database.

            Args:
                * index (int, optional): 
                    - SNo (index) of the notice.
                    - Defaults to 0 (Latest notice).
                    - For last 2nd notice index will 1

            Returns:
                * tuple:
                    - Notice data (desired row of the database)
                * None:
                    - If no data is found for given index.
                    - Any other error occurred.
        """
        # notice are arranged in descending order. Means latest notice has maximum index (SNO.).
        # We will sort the table in descending order to get the latest notice on top.
        # To get last 2nd, 3rd etc notice we use "Desired Sno = Latest S.no - Index" during fetching from the database.
        # For top (latest) notice index is 0.
        # For last 2nd notice index is 1 and so on ....
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT * FROM {self.tables.get('notice')}
                                    ORDER BY SNo DESC
                                    LIMIT 1;
                                """)
        except Exception as e:
            print("Unable to fetch notice from database. Error Code 1302")
            print("Exception: ", e)
            return None
        latestNotice = self.cursor.fetchone()

        # if no notice found
        if latestNotice is None:
            return None
        elif index == 0:  # means user needs only latest notice
            return latestNotice

        # If user wants to see previous notice
        # In schema SNo is the first attribute.
        latestNoticeSNo = latestNotice[0]
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT * FROM {self.tables.get('notice')}
                                    ORDER BY SNo DESC
                                    WHERE SNo = {latestNoticeSNo-index}
                                """)
        except Exception as e:
            print("Unable fetch desired notice from the database. Error Code 1303")
            print("Exception: ", e)
            return None

        desiredNotice = self.cursor.fetchone()
        return desiredNotice  # it will return None if no rows found else returns the desired row

    def __credits_sources(self, tableName: str, orderBy: str = "Name", order: str = "ASC") -> list[tuple, tuple, ] | None:
        """
            Description:
                - Method to fetch data from credits and sources table from the database.
                - This method is private and should not be used directly.
                - This method is used by credits() and sources() methods.
                - Due to similar functionality of both the tables, this method is used to fetch data from both the tables.

            Args:
                * tableName (str):
                    - Name of the table from which data is to be fetched.
                    - Must be one of the following: "credits", "sources"
                * orderBy (str, optional):
                    - Order by which the tuples will be shorted and returned.
                    - Defaults to "Name".
                    - If any other value is passed then it will be set to "Name".
                * order (str, optional): 
                    - Order of the sorting. [ASC, DESC]
                    - Defaults to "ASC".
                    - If any other value is passed then it will be set to "ASC".

            Returns:
                * list[tuple, tuple, ] 
                    - List of tuples containing the credits table data.
                    - See schema for more details about the data.
                * None:
                    - If no data is found.
                    - Any other error occurred.
        """
        if tableName == 'credits':
            if orderBy not in ["Name", "SNo", "Designation"]:
                orderBy = "Name"
        elif tableName == 'sources':
            if orderBy not in ["Name", "SNo"]:
                orderBy = "Name"
        else:
            return None  # if tableName is not credits or sources

        if order not in ["ASC", "DESC"]:
            order = "ASC"
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT * FROM {tableName}
                                    ORDER BY {orderBy} {order}
                                """)
        except Exception as e:
            print("Unable to fetch credits from database. Error Code 1304")
            print("Exception: ", e)
            return None

        credits = self.cursor.fetchall()  # fetching all the rows

        if credits == []:  # if no rows found
            return None
        return credits

    def credits(self, orderBy: str = "Name", order: str = "ASC") -> list[tuple, tuple, ] | None:
        """
            Description:
                - Method to fetch data from credits table of the database.

            Args:
                * orderBy (str, optional):
                    - Order by which the tuples will be shorted and returned.
                    - Defaults to "Name".
                    - If any other value is passed then it will be set to "Name".
                * order (str, optional): 
                    - Order of the sorting. [ASC, DESC]
                    - Defaults to "ASC".
                    - If any other value is passed then it will be set to "ASC".

            Returns:
                * list[tuple, tuple, ] 
                    - List of tuples containing the credits table data.
                    - See schema for more details about the data.
                * None:
                    - If no data is found.
                    - Any other error occurred.
        """
        return self.__credits_sources(self.tables.get('credits'), orderBy, order)


if __name__ == '__main__':
    print(DynamicContents().credits())
