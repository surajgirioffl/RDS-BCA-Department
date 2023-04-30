"""
    @file: files_db.py
    @author: Suraj Kumar Giri
    @init-date: 29th April 2023
    @last-modified: 30th April 2023
    @error-series: 2100

    @description:
        * Module to fetch desired data from the database rdsbca$files.
        * Module to read/insert/update desired data from/to the database rdsbca$files.
        * Simply, module to handle all database related operations on the database rdsbca$files.
    
    @classes:
        ...
    
    @functions:
        ...
"""

from os import environ
import mysql.connector as mysql


class Files:
    def __init__(self, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSERNAME'), port: int = int(environ.get('DBPORT')) if environ.get('DBPORT') is not None else 3306, password: str = environ.get('DBPASSWORD'), database: str = "rdsbca$files", timeZoneForDatabase="Asia/Kolkata") -> None:
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
                host=f'{host}', user=f'{user}', password=f'{password}', port=port)
            self.cursor = self.conn.cursor(buffered=True)

            # using database as per the parameter
            self.cursor.execute(f'USE {database}')
        except Exception as e:
            print(
                f"Unable to establish connection with the database ({database}). Error code 2100")
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
                print("Unable to set time_zone. Error code 2101")

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

    def fetchFileMetadata(self, fileId: int | str) -> dict | None:
        attributes: list = ['files.FileId', 'Title', 'Access', 'ServeVia',
                            'FilePath', 'ViewLink', 'DownloadLink', 'DownloadName', 'Extension']
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT * FROM
                                    (
                                        SELECT {str(attributes).strip('[]').replace("'", "")} FROM files
                                        JOIN
                                            files_path ON files.FileId = files_path.FileId
                                        JOIN
                                            drive ON files.FileId = drive.FileId
                                        JOIN
                                            files_metadata ON files.FileId = files_metadata.FileId
                                    ) AS `File Metadata`
                                    WHERE FileId = {fileId}                            
                                """)
        except Exception as e:
            print("Unable to fetch file metadata. Error code 2102")
            print("Exception: ", e)
            return None

        desiredTuple: tuple | None = self.cursor.fetchone()
        if desiredTuple:
            attributes[0] = 'FileId'
            attributesValueDict: dict = {
                key: value for key,
                value in zip(attributes, desiredTuple)
            }
            return attributesValueDict
        return None


if __name__ == '__main__':
    print(Files().fetchFileMetadata(17648433))
