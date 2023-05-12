"""
    @file: files_db.py
    @author: Suraj Kumar Giri
    @init-date: 29th April 2023
    @last-modified: 12th May 2023
    @error-series: 2100

    @description:
        * Module to fetch desired data from the database rdsbca$files.
        * Module to read/insert/update desired data from/to the database rdsbca$files.
        * Simply, module to handle all database related operations on the database rdsbca$files.
    
    @classes:
        * Files
            - Class to handle all database related operations on the database rdsbca$files.
    
    @functions:
        ...
"""

from os import environ
from typing import Any
import mysql.connector as mysql


class Files:
    """
        Description:
            - Class to handle all database related operations on the database rdsbca$files.
            - This class is responsible for fetching/reading/inserting/updating data from/to the database rdsbca$files.

        Attributes(class variables):
            * 

        Methods(static methods):)        
            *

        Attributes(objects):
            * 

        Methods(objects):
            * fetchFileMetadata()
                - Method to fetch file metadata from the database.
            * updateFileStats()
                - Method to insert/update file stats in the database.
    """

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
        """
            Description:
                - Method to fetch file metadata from the database.

            Args:
                * fileId (int | str):
                    - FileId of the file whose metadata is to be fetched.

            Returns:
                * dict: 
                    - Returns a dictionary containing the metadata of the file in form of key-value pairs.
                * None:
                    - Returns None if the file Id is not found in the database or metadata for specified file Id is not found in the database.
                            - Or if the connection with the database is not yet established.
                            - Or any other error occurs while executing the query.
        """
        attributes: list[str] = [
            'files.FileId', 'Title', 'Access', 'ServeVia',
            'FilePath', 'ViewLink', 'DownloadLink', 'DownloadName', 'Extension',
            'Size', 'DownloadCount'
        ]
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
                                        JOIN
                                            files_tracking ON files.FileId = files_tracking.FileId
                                    ) AS `File Metadata`
                                    WHERE FileId = {fileId}                            
                                """)
        except Exception as e:
            print("Unable to fetch file metadata. Error code 2102")
            print("Exception: ", e)
            return None

        desiredTuple: tuple | None = self.cursor.fetchone()
        # print(self.cursor.statement) # to display the executed query (statement)
        if desiredTuple:
            attributes[0] = 'FileId'
            attributesValueDict: dict = {
                key: value for key,
                value in zip(attributes, desiredTuple)
            }
            return attributesValueDict
        return None

    def __isTupleExists(self, tableName: str, keyAttribute: str, value: str | int | float | Any) -> bool:
        """
            Description:
                - Method to check if a tuple exists in the database or not.
                - It checks if a tuple exists in the database with the specified keyAttribute having the specified value.

            Args:
                * tableName (str): 
                    - Name of the table in which the tuple is to be searched.
                * keyAttribute (str): 
                    - Name of the attribute which is to be checked for the specified value.
                * value (str | int | float | Any): 
                    - Value of the specified keyAttribute which is to be checked.

            Returns:
                * bool:
                    - Returns True if the tuple exists in the database else False.

            Warning:
                - This method doesn't check if the connection with the database is established or not.
                - So, caller of this method is responsible for checking the connection with the database.
        """
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT * FROM {tableName}
                                    WHERE {keyAttribute} = {value}
                                """)
        except Exception as e:
            print("Unable to check if tuple exists. Error code 2103")
            print("Exception: ", e)
            return False
        else:
            return self.cursor.fetchone() is not None

    def updateFileStats(self, fileId: int | str) -> bool:
        """
            Description:
                - Method to set/update file stats in the database.
                - It handle both the cases:
                    - If the file stats already exists in the database then it updates the stats.
                    - If the file stats doesn't exists in the database then it creates a new entry for the file stats.
                - Currently, the table 'files_tracking' is used to store the file stats.

            Args:
                * fileId (int | str):
                    - FileId of the file whose stats is to be updated/inserted.
            Returns:
                * bool: 
                    - Returns True if the file stats is updated/inserted successfully else False.
                    - Returns False if any exception or any error occurs. 
        """
        if not self.connectionStatus:
            print("Unable to update file stats because connection with the database is not yet established. Error code 2104")
            return False

        # TODO: update file stats (connection is established)
        try:
            if self.__isTupleExists('files_tracking', 'FileId', fileId):
                self.cursor.execute(f"""-- sql
                                        UPDATE files_tracking
                                        SET 
                                            DownloadCount = DownloadCount + 1, 
                                            LastDownloaded = DEFAULT
                                        WHERE FileId = {fileId}
                                    """)
            else:
                self.cursor.execute(f"""-- sql
                                        INSERT INTO files_tracking(FileId, DownloadCount)
                                        VALUES({fileId}, 1)
                                    """)
        except Exception as e:
            print("Unable to update file stats. Error code 2105")
            print("Exception: ", e)
            return False
        else:
            print(
                f"File stats of the file with id {fileId} inserted/updated successfully.")
            return True


if __name__ == '__main__':
    print(Files().fetchFileMetadata(17648433))
    print(Files()._Files__isTupleExists('files', 'FileId', '17648433'))
    Files().updateFileStats(17648433)
