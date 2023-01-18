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


if __name__ == '__main__':
    DynamicContents()
