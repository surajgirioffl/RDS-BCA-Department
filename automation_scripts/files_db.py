"""
    @file: files_db.py
    @author: Suraj Kumar Giri
    @init-date: 24th Jan 2023
    @last-modified: 25th Jan 2023
    
    @description:
        * Module to insert data into the database rdsbca$files.
"""
from os import environ
import mysql.connector as mysql


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

            # listing all the tables in the database
            self.tables = {
                'files': 'files',
                'files_path': 'files_path',
                'drive': 'drive',
                'file_contents_info': 'file_contents_info',
                'files_metadata': 'files_metadata',
                'files_type': 'files_type',
                'files_info': 'files_info',
                'files_tracking': 'files_tracking',
                'creditors_info': 'creditors_info',
                'credits': 'credits',
                'root_sources': 'root_sources'
            }

    def __del__(self):
        ...


if __name__ == '__main__':
    Files()
