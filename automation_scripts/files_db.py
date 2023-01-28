"""
    @file: files_db.py
    @author: Suraj Kumar Giri
    @init-date: 24th Jan 2023
    @last-modified: 28th Jan 2023

    @description:
        * Module to insert data into the database rdsbca$files.
"""
from os import environ
import mysql.connector as mysql
import my_random as myRandom


class Files:
    def __init__(self, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSERNAME'), port: int = int(environ.get('DBPORT')) if environ.get('DBPORT') is not None else 3306, password: str = environ.get('DBPASSWORD'), database: str = "rdsbca$files", timeZoneForDatabase="Asia/Kolkata") -> None:
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

    # Now taking input from user and inserting into database (Table by Table).
    def files(self) -> int:
        print("------------------------------Table files------------------------------")
        while True:
            # for attribute 'Title'
            while True:
                title = input(
                    "Write title of file (It will display on the web page): ")
                if title == "":
                    print("Title can't be empty. Please write again...")
                else:
                    title = title.title()  # converting into title case
                    break

            # for attribute 'Access'
            while True:
                print("""
                        Select the access right:
                        1. Public (Default. Press enter)
                        2. Private
                        3. Restricted
                    """)
                choice = input("write your choice: ")
                if choice == "1" or choice == "":
                    access = "Public"
                    break
                elif choice == "2":
                    access = "Private"
                    break
                elif choice == "3":
                    access = "Restricted"
                    break
                else:
                    print("Invalid choice... Please select again")

            # for attribute 'ServeVia'
            while True:
                print("""
                        Select the way to serve the file to client:
                        1. Drive (Default. Press enter)
                        2. FileSystem
                    """)
                choice = input("write your choice: ")
                if choice == "1" or choice == "":
                    serveVia = "Drive"
                    break
                elif choice == "2":
                    serveVia = "FileSystem"
                    break
                else:
                    print("Invalid choice... Please select again")

            # verification of input data
            print("================VERIFICATION=================")
            print(f"""
                    For table 'files':
                    1. Title: {title}
                    2. Access: {access}
                    3. ServeVia: {serveVia}
                    Press enter or yes to continue else press any key to re-enter the information.
                """)
            choice = input("write your choice: ")
            if choice in ["", "yes", "Yes", "YES"]:
                break

        fileId = myRandom.Random(self.cursor, 'files', 'FileId').generate()

        # Inserting data in table
        self.cursor.execute(f"""-- sql
                                INSERT INTO {self.tables.get('files')}
                                VALUES (
                                        DEFAULT, {fileId}, '{title}', '{access}', '{serveVia}'
                                    );
                            """)


def main():
    files = Files()
    files.files()


if __name__ == '__main__':
    print("\033[2J\033[H")
    main()
