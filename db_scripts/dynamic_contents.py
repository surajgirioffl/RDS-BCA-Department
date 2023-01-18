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
    def __init__(self, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSERNAME'), port: int = int(environ.get('DBPORT')) if environ.get('DBPORT') is not None else 3306, password: str = environ.get('DBPASSWORD'), database: str = "rdsbca$dynamic_contents", timeZoneForDatabase="Asia/Kolkata") -> None:
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

    def __del__(self):
        if self.connectionStatus:
            self.conn.commit()
            self.conn.close()


if __name__ == '__main__':
    DynamicContents()
