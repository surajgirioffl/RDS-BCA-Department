"""
    @file: previous_year_questions_db.py
    @author: Suraj Kumar Giri
    @init-date: 24th April 2023
    @last-modified: 24th April 2023
    @error-series: 1900
    
    @description:
        * Module to insert data into the database rdsbca$previous_year_questions.
        
    @classes:
        * PreviousYearQuestionsDB
            - Class to INSERT/UPDATE data into the database rdsbca$previous_year_questions.
    
    @functions:
        *     
"""

import mysql.connector as mysql
from os import environ


class PreviousYearQuestionsDB:
    """
        @description:
            - Class to insert data into the database rdsbca$previous_year_questions.
            - Handle all INSERT/UPDATE operations on the database.

        @methods:
            * 
    """

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

    def __isYearExists(self, source: str, year: str):
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT * FROM {source} 
                                    WHERE 
                                    Year = {year}
                                """
                                )
        except Exception as e:
            print("Unable read data from the table {source}. Error code: 1902")
            print("Exception: ", e)
            return False
        else:
            if self.cursor.fetchone():
                return True
            return False

    def __insertData(self, source: str, semester: str, year: str, fileId: str) -> bool:
        try:
            self.cursor.execute(f"""-- sql 
                                    INSERT INTO {source} (Year, Sem{semester})
                                    VALUES (
                                            {year}, {fileId}
                                    )
                                """
                                )
        except Exception as e:
            print("Unable update data in the table {source}. Error code: 1903")
            print("Exception: ", e)
            return False
        else:
            self.conn.commit()
            print("Data inserted successfully.....")
            return True

    def __updateData(self, source: str, semester: str, year: str, fileId: str) -> bool:
        try:
            self.cursor.execute(
                f"""-- sql
                        UPDATE {source}
                        SET 
                        Sem{semester} = {fileId}
                        WHERE
                        Year = {year}
                    """
            )
        except Exception as e:
            print("Unable update data in the table {source}. Error code: 1904")
            print("Exception: ", e)
            return False
        else:
            self.conn.commit()
            print("Data updated successfully.....")
            return True

    def inputAndInsertInDatabase(self):
        index: int = 1
        while True:
            print(
                f"\n=======================FOR INDEX {index}=======================")
            # For `source`
            while True:
                print(
                    """Select Source: 
                        1. BRABU
                        2. LN Mishra
                        3. Vaishali
                        """
                )
                choice = input("Write your choice: ")
                if choice in ["1", "2", "3"]:
                    if choice == "1":
                        source = "brabu"
                        break
                    elif choice == "2":
                        source = "ln_mishra"
                        break
                    else:
                        source = "vaishali"
                        break
                else:
                    print("Invalid choice.")
                    print("Please select again....")
                    continue

            # for `semester`
            while True:
                semester = input("Write semester: ")
                if semester not in [str(number) for number in range(1, 7)]:
                    print("Invalid semester.")
                    print("Please write again...")
                    continue
                break

            # for `year`
            while True:
                year = input("Write year: ")
                if not year.isdigit():
                    print("Invalid semester.")
                    print("Please write again...")
                    continue
                break

            # for `fileId`
            while True:
                fileId = input("Write file ID: ")
                if not year.isdigit():
                    print("Invalid file ID.")
                    print("Please write again...")
                    continue
                break

            print(
                f"""\n------VERIFICATION-------
                    => Source: {source}
                    => Semester: {semester}
                    => Year: {year}
                    => File ID: {fileId}
                        """
            )
            choice = input(
                "Press enter to INSERT/UPDATE else any key to rewrite the data: "
            )
            if choice == "":
                if self.__isYearExists(source, year):
                    print(
                        "Warning: Year already exists. Updating data... (You may overwrite the data and it will be lost.)")
                    choice = input(
                        "Press enter to continue updating else any key to rewrite the data: ")
                    if choice == "":
                        self.__updateData(source, semester, year, fileId)
                    else:
                        continue
                else:
                    self.__insertData(source, semester, year, fileId)

                try:
                    input("Press any key to continue or press Ctrl+C to exit...")
                except KeyboardInterrupt:
                    print("Exiting...")
                    return
                else:
                    index += 1
                    continue  # not need to write this line
            else:
                continue


def main():
    PreviousYearQuestionsDB().inputAndInsertInDatabase()


if __name__ == "__main__":
    main()
