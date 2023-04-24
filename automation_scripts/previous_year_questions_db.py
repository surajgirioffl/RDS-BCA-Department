"""
    @file: previous_year_questions_db.py
    @author: Suraj Kumar Giri
    @init-date: 24th April 2023
    @last-modified: 24th April 2023
    @error-series: 1900
    
    @description:
        * Module to insert data into the database rdsbca$previous_year_questions.
"""

import mysql.connector as mysql
from os import environ


class PreviousYearQuestionsDB:
    def __init__(self, host: str = environ.get("DBHOST"), user: str = environ.get("DBUSERNAME"), port: int = int(environ.get("DBPORT"))if environ.get("DBPORT") is not None else 3306, password: str = environ.get("DBPASSWORD"), database: str = "previous_year_questions", timeZoneForDatabase="Asia/Kolkata") -> None:
        """
            Description:
                - Constructor to initialize the object and establish connection with the database.

            Args:
                * host (str, optional):
                    - Host of the database.
                    - Defaults to host from the environment variable.
                * user (str, optional): _description_.
                    - Username to use for authentication for establishing connection with the database.
                    - Defaults to username from the environment variable.
                * port (int, optional):
                    - Port to connect to the database.
                    - Defaults to port from the environment variable.
                    - 3306 if unspecified in the environment variable.
                * password (str, optional):
                    - Password to use while connecting to the database.
                    - Defaults to password from the environment variable.
                * database (str, optional):
                    - Name of the database.
                    - Defaults to "rdsbca".
                * timeZoneForDatabase (str, optional):
                    - Timezone to be used within the database.
                    - Defaults to "Asia/Kolkata".

        Returns:
            * None
        """
        try:
            # establishing connection and creating cursor object
            self.conn = mysql.connect(
                host=f"{host}", user=f"{user}", password=f"{password}", port=port
            )
            self.cursor = self.conn.cursor(buffered=True)

            # using database as per the parameter
            self.cursor.execute(f"USE rdsbca${database}")
        except Exception as e:
            print(
                f"Unable to establish connection with the database ({database}). Error code 1900"
            )
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
                print("Unable to set time_zone. Error code 1901")

    def __del__(self) -> None:
        """
            Description:
                - Destructor to delete the object after committing the changes and closing the database.
            Returns:
                * None
        """
        if self.connectionStatus:
            self.conn.commit()
            self.conn.close()
