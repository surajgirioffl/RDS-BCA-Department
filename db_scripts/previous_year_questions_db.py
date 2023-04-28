"""
    @file: previous_year_questions_db.py
    @author: Suraj Kumar Giri
    @init-date: 09th Nov 2022
    @last-modified: 29th April 2023
    @error-series: 2000

    @description:
        * Module to fetch data from the rdsbca$previous_year_questions database.
"""

from os import environ
import mysql.connector as mysql


class PreviousYearQuestions:
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
                    - Defaults to "previous_year_questions".
                * timeZoneForDatabase (str, optional):
                    - Timezone to be used within the database.
                    - Defaults to "Asia/Kolkata".

            Returns:
                * None
        """
        try:
            # establishing connection and creating cursor object
            self.conn = mysql.connect(
                host=f"{host}", user=f"{user}", password=f"{password}", port=port)
            self.cursor = self.conn.cursor(buffered=True)

            # using database as per the parameter
            self.cursor.execute(f"USE rdsbca${database}")
        except Exception as e:
            print(
                f"Unable to establish connection with the database ({database}). Error code 2000")
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
                print("Unable to set time_zone. Error code 2001")

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

    def getLinks(self, source: str, semester: int | str) -> list[tuple[str, int, int], tuple[str, int, int], ] | list | None:
        """
            Description:
                - Method to fetch the file ID (used to create links) of previous year questions from the database (previous_year_questions).

            Args:
                * source (str): 
                    - Source of the previous year questions.
                    - Source may be one from these three - [brabu, vaishali, lnMishra]
                    - To select all sources use - all
                * semester (int | str):
                    - Semester for which the previous year questions are to be fetched.

            Returns:
                * list[tuple[str, int, int], tuple[str, int, int], ]
                    - Return list of tuples (rows) containing data for the previous year questions.
                    - Each tuple in the list contains (Source, Year, FileId)
                    - E.g:
                        - [ ('LN Mishra, Muzaffarpur', 2022, 35405203), ('LN Mishra, Muzaffarpur', 2021, 53553236)]

                * list (empty)
                    - Returns empty list if no data (previous year questions) is available for the given semester.

                * None
                    - Returns None if given source is not valid or any other error occurred.
        """
        if source == "all":
            data = self.cursor.execute(f"""-- sql
                                            SELECT * FROM
                                            (
                                                    SELECT "BRABU" AS Source, Year, Sem{semester} FROM brabu WHERE Sem{semester} IS NOT NULL 
                                                    UNION
                                                    SELECT "Vaishali Institute, Muzaffarpur", Year, Sem{semester} AS Source FROM vaishali WHERE Sem{semester} IS NOT NULL 
                                                    UNION
                                                    SELECT "LN Mishra, Muzaffarpur", Year, Sem{semester} as Source FROM ln_mishra WHERE Sem{semester} IS NOT NULL
                                            ) AS `Previous Year Questions`
                                            ORDER BY Year DESC
                                        """)
            return self.cursor.fetchall()

        elif source == "brabu":
            self.cursor.execute(f"""-- sql
                                    SELECT "BRABU" AS Source, Year, Sem{semester}
                                    FROM brabu WHERE Sem{semester} IS NOT NULL 
                                    ORDER BY Year DESC
                                """)
            return self.cursor.fetchall()

        elif source == "vaishali":
            self.cursor.execute(f"""-- sql
                                    SELECT "Vaishali Institute, Muzaffarpur" AS Source, Year, Sem{semester} 
                                    FROM vaishali WHERE Sem{semester} IS NOT NULL 
                                    ORDER BY Year DESC
                                """)
            return self.cursor.fetchall()

        elif source == "lnMishra":
            self.cursor.execute(f"""-- sql
                                    SELECT "LN Mishra, Muzaffarpur" as Source, Year, Sem{semester}
                                    FROM ln_mishra WHERE Sem{semester} IS NOT NULL
                                    ORDER BY Year DESC
                                """)
            return self.cursor.fetchall()

        else:
            return None


if __name__ == '__main__':
    obj = PreviousYearQuestions()
    data = obj.getLinks('all', 4)
    for row in data:
        print(row)
