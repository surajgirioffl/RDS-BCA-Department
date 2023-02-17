"""
    @author: Suraj Kumar Giri
    @init-date: 17th Oct 2022
    @last-modified: 17th Feb 2023
    @error-series: 1600
    @description:
        * Module to handle database operations related with the database bca.
    @classes:
"""

__author__ = 'Suraj Kumar Giri'
__email__ = 'surajgirioffl@gmail.com'

from os import environ
import mysql.connector as mysql


class Bca:
    """
        Description:
            - Class to handle database operations for student's to fetch data from the database 'bca'.

        Methods:
    """

    def __init__(self, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSERNAME'), port: int = int(environ.get('DBPORT')) if environ.get('DBPORT') is not None else 3306, password: str = environ.get('DBPASSWORD'), databaseName: str = "rdsbca$bca") -> None:
        """
            Description:
                - To initialize the database connection with provided credentials.

            Args:
                * host (str, optional):
                    - Hostname of the database server.
                    - Defaults to the hostname set in the environment variable DBHOST.
                * user (str, optional):
                    - Username of the database server.
                    - Defaults to the username set in the environment variable DBUSERNAME.
                * port (int, optional):
                    - Port number of the database server.
                    - Defaults to the port number set in the environment variable DBPORT or 3306.
                * password (str, optional):
                    - Password of the database server.
                    - Defaults to the password set in the environment variable DBPASSWORD.
                * databaseName (str, optional):
                    - Name of the database.
                    - Defaults to 'rdsbca$bca'.
        """

        # trying to establish connection with the database.
        try:
            self.conn = mysql.connect(
                host=host, user=user, port=port, password=password)
            self.cursor = self.conn.cursor(buffered=True)

            self.cursor.execute(f"""-- sql
                                        USE `{databaseName}`
                                    """)
            self.connectionStatus = True  # flag to check if connection is established or not
            print(f"Connection established with the database {databaseName}.")
        except Exception as e:
            print(
                f"Unable to connect with the database {databaseName}. Error code 1600")
            print("Exception:", e)
            self.connectionStatus = False  # if connection not established

    def __del__(self):
        """
            Description:
                - To close the database connection when destructor called.
        """
        if self.connectionStatus:
            # no need to commit the connection because only read-only functionalities are given in this script.
            self.conn.close()


if __name__ == "__main__":
    print(Bca())
