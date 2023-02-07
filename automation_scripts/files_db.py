"""
    @file: files_db.py
    @author: Suraj Kumar Giri
    @init-date: 24th Jan 2023
    @last-modified: 7th Feb 2023
    @error-series: 1500

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
                f"Unable to establish connection with the database ({database}). Error code 1500")
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
                print("Unable to set time_zone. Error code 1501")

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

    def setTableAttributes(self) -> None:
        # listing all the tables in the database along with their attributes
        # only those tables are listed in which data need to be inserted. So, table like 'files_tracking' etc are not listed.
        self.tables = {
            'files': ["SNo", "FileId", "Title", "Access", "ServeVia"],
            'files_path': ["SNo", "FileId", "FilePath"],
            'drive': ["SNo", "FileId", "ViewLink", "DownloadLink"],
            'file_contents_info': ["SNo", "FileId", "Description", "Keywords"],
            'files_metadata': ["SNo", "FileId", "FileName", "DownloadName", "Extension", "Size"],
            'files_type': ["SNo", "Extension", "FileType"],
            'files_info': ["SNo", "FileId", "Category", "FileFor", "DateCreated", "DateModified", "Tags"],
            'creditors_info': ["Id", "Name", "Email", "Designation", "Username", "AccountId", "Contact"],
            'credits': ["SNo", "FileId", "SubmitterId", "SubmittedOn", "UploaderId", "UploadedOn", "ModifierId", "LastModifiedOn", "ApproverId", "ApprovedOn", "RootSource"],
            'root_sources': ["SNo", "RootSource", "SourceFileLink", "ContactSource"]
        }

        # attributes of type ENUM (means having a predefined values)
        self.enumAttributes = {
            "Access": {
                "options": ["Public", "Private", "Restricted"],
                "default": "Public"
            },
            "ServeVia": {
                "options": ["FileSystem", "Drive"],
                "default": "Drive"
            }
        }

        # attributes having default values except NULL as default value (auto-increment is included)
        # attributes in which DEFAULT need to be set if user doesn't provide any value or no need to provide value
        # mysql date time is like : 2023-01-28 01:00:46 (CURRENT_TIMESTAMP)
        # Except ENUM attributes
        self.passDefault = ["SNo", "Access", "ServeVia", "DateCreated",
                            "DateModified", "SubmittedOn", "UploadedOn", "LastModifiedOn", "ApprovedOn"]

    def files(self) -> int:
        """
            Now taking input from user and inserting into database (Table by Table).
        """
        ...


def main():
    files = Files()
    files.files()


if __name__ == '__main__':
    print("\033[2J\033[H")
    main()
