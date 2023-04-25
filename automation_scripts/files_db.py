"""
    @file: files_db.py
    @author: Suraj Kumar Giri
    @init-date: 24th Jan 2023
    @last-modified: 25th April 2023
    @error-series: 1500

    @description:
        * Module to insert data into the database rdsbca$files.
"""
from os import environ
import os
import sys
import mysql.connector as mysql
import my_random as myRandom
import drive_direct_download_link as driveLink
sys.path.append(os.getcwd())
from app_scripts.my_time import epochToMySql


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
        """
            Description:
                - Method to set the attributes of the tables of the database.

            Returns:
                * None
        """
        # listing all the tables in the database along with their attributes
        # only those tables are listed in which data need to be inserted. So, table like 'files_tracking' etc are not listed.
        # files database has total of 11 tables.
        # some tables like 'files_type', 'creditors_info', 'root_sources' are not added because of file independency because multiple files may use same contents of these tables. (Data should be inserted manually or by any separate script.)
        # some tables like 'files_tracking' are not added because of user dependencies.
        self.tables = {
            'files': ["SNo", "FileId", "Title", "Access", "ServeVia"],
            'files_path': ["SNo", "FileId", "FilePath"],
            'drive': ["SNo", "FileId", "ViewLink", "DownloadLink"],
            'file_contents_info': ["SNo", "FileId", "Description", "Keywords"],
            'files_metadata': ["SNo", "FileId", "FileName", "DownloadName", "Extension", "Size"],
            'files_info': ["SNo", "FileId", "Category", "FileFor", "DateCreated", "DateModified", "Tags"],
            'credits': ["SNo", "FileId", "SubmitterId", "SubmittedOn", "UploaderId", "UploadedOn", "ModifierId", "LastModifiedOn", "ApproverId", "ApprovedOn", "RootSourceFileLink", "RootSourceId"]
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
        # self.passDefault = ["SNo", "Access", "ServeVia", "DateCreated", "DateModified", "SubmittedOn", "UploadedOn", "LastModifiedOn", "ApprovedOn"]
        self.passDefault = ["SNo", "Access", "ServeVia"]

        # attributes of INT data type in above listed tables. Means no quotes(double or single) will be allowed while inserting data in the table.
        self.intAttributes = ["SNo", "FileId", "SubmitterId",
                              "UploaderId", "ModifierId", "ApproverId", "RootSourceId"]

        # Special attributes whose value gathered after some processing (using same or another module) instead of user input dependency.
        # Some special attributes whose values will be fetched before user input for a specific file.
        # Some of these attribute's value will be fetched automatically after providing path of the file.
        # User don't need to provide value for these attributes.
        self.attributesWithAvailableValue = ["FileId", "FilePath", "ViewLink",
                                             "DownloadLink", "FileName", "Extension", "Size", "DateCreated", "DateModified"]

    def __getSqlQuery(self, tableName: str, dataList: list) -> str:
        """
            Description:
                - Method to generate MySQL query for inserting data into the table.
                - Generate query as per schema of the table.

            Args:
                * tableName (str):
                    - Table name in which data need to be inserted.
                * dataList (list):
                    - List of data to be inserted into the table.
                    - Data to be inserted into the table should be in the same order as the attributes of the table.
                    - DEFAULT, ENUM etc should be maintained in dataList.
                    - DEFAULT should be written as 'DEFAULT' (single quotes included).

            Returns:
                * str:
                    - MySQL query for inserting data into the table.

            Drawbacks:
                - INT type attributes are also written as string in the returned query.
                - But this will not cause any problem because MySQL will automatically convert the string to int.
                    - Example: "123" will be converted to 123.
                    - MySQL auto perform implicit type conversion. Thanks to MySQL.
        """
        sql: str = f"""
                        INSERT INTO {tableName} ({(', '.join(self.tables[tableName]))})
                        VALUES
                        ({(str([data for data in dataList])).strip('[]')})
                    """
        sql = sql.replace("'DEFAULT'", "DEFAULT")
        return sql

    def __insertData(self, tableName: str, query: str) -> bool:
        """"""
        """
            Description:
                - Method to insert data in desired table of files database.

            Args:
                * tableName (str):
                    - Table name in which data will be inserted.
                * query (str):
                    - MySQL query for INSERT into desired table.

            Returns:
                * bool:
                    - Returns True if data inserted successfully else False.
        """
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(
                f"Unable to insert data into table {tableName}. Error code 1502")
            print("Exception: ", e)
            return False
        else:
            self.conn.commit()  # commit the changes to desired table of the database
            print("Data inserted successfully....")
            return True

    def __setSessionScopedAttributes(self) -> None:
        """
            Description:
                - Method to get and set session scoped attributes and respective values after taking from the user.
                - Session scoped attributes are those attributes which are same for all the files of the current session.
                - Means user don't need to provide these attributes for each file.

            More Info:
                - It will create a instance variable named 'sessionScopedAttributes` which is a dictionary of session scoped attributes and respective values if user want to provide session scoped attributes.
                - If user refuse to provide session scoped attributes then also it will create a instance variable named 'sessionScopedAttributes` which will be an empty dictionary.

            Returns:
                * None:
                    - Returns None.
        """
        print("\n======================SESSION SCOPED ATTRIBUTES======================")
        print("Session scoped attributes are those attributes which are same for all the files of the current session.")
        print("By providing this you don't need to provide these attributes for each file.")
        print("Warning: If you provide session scoped attributes then you can't provide these attributes for any file.")
        print("If you have any doubt regarding any attribute then don't add it here. Just provide it for each file manually.\n")
        choice = input(
            "Do you want to provide session scoped attributes (Press enter for yes else any key for no): ")

        self.sessionScopedAttributes: dict = {}

        if choice != "":
            return

        print("""KEEP IN MIND:
                    1. Attributes name must be same as in the schema.
                    2. Attributes name must be in PascalCase.
                    3. Must provide value for each attribute.
                    4. Warning: You will not able to provide these attributes for any file manually. It will be automatically provided by the program.
                    5. Now write attributes name and value as per schema.
                    6. Press Ctrl+C to stop providing attributes and save the data in session scoped attributes dictionary.\n
            """)

        while True:
            try:
                index = 1
                while True:
                    print(
                        f"======================ATTRIBUTE NUMBER {index:02}======================")
                    attribute = input("Write attribute name as per schema: ")
                    value = input(
                        f"Write value for the attribute {attribute}: ")
                    if attribute == "" or value == "":
                        print(
                            "      Attribute name or value can't be empty. Try again...")
                        continue
                    else:
                        self.sessionScopedAttributes[attribute] = value
                        index += 1
            except KeyboardInterrupt:
                print(
                    "===========================VERIFICATION===========================")
                for key, value in self.sessionScopedAttributes.items():
                    print(f"{key}: {value}")
                choice = input(
                    "Press enter to save attributes-value if everything is fine else press any key to rewrite: ")
                if choice == "":
                    return
                continue

    def inputAndInsertInDatabase(self) -> bool:
        """
            Description:
                - Take input from user as per schema and insert them into the database (Table by Table).

            Returns:
                * bool:
                    - Returns True if everything went fine else False.
        """
        fileIndex: int = 1
        while True:
            print(
                f"\n======================FILE NUMBER {fileIndex:02}======================")
            attributesWithAvailableValueDict: dict = {}
            while True:
                filePath: str = input("Write file path: ")
                if os.path.exists(filePath):
                    # if path is valid then check if it is a file or not
                    if os.path.isfile(filePath):
                        attributesWithAvailableValueDict["FilePath"] = filePath.removeprefix(
                            os.getcwd()+'\\').replace('\\', '/')
                        break
                    else:
                        # if path is not a file then ask user to provide path again
                        print("      Provided path is not a file. Try again...")
                        continue
                else:
                    # if path is not valid then ask user to provide path again
                    print("      Invalid file path. Try again...")
                    continue
            fileMetaData: dict = Files.fetchFileMetadata(filePath)
            for key, value in fileMetaData.items():
                if key == 'Size':
                    # fetchFileMetadata returns file size in bytes. So, we will convert it into MB.
                    value = f'{value/1024**2:.03}'
                elif key in ['DateCreated', 'DateModified']:
                    value = epochToMySql(value)
                elif key == 'Extension':
                    # removing leading dot from extension
                    value = value.replace('.', '')
                attributesWithAvailableValueDict[key] = value

            # Now, we have valid file path. So, we will fetch value of some file attributes.
            while True:
                viewLink: str = input("Write drive view link of the file: ")
                if driveLink.checkLink(viewLink):
                    attributesWithAvailableValueDict['ViewLink'] = viewLink
                    attributesWithAvailableValueDict['DownloadLink'] = driveLink.convertToDownloadLink(
                        viewLink)
                    break
                else:
                    print("      Invalid drive link. Try again...")
                    continue

            # Now, we will generate a random 8 digits FileID for the current file.
            attributesWithAvailableValueDict['FileId'] = myRandom.Random(
                cursor=self.cursor, tableName='files', columnName='FileId').generate()

            for table in self.tables:
                while True:
                    print(f"\n================Table {table}================")
                    dataList = []  # list of data to be inserted into the table
                    for attributeIndex, attribute in enumerate(self.tables[table]):
                        if attribute in self.enumAttributes:
                            while True:
                                print(
                                    f"{attributeIndex+1:02}) Select value for Enum attribute {attribute}")
                                print(
                                    f"      0: Default ({self.enumAttributes[attribute]['default']}) (Press Enter to select)")
                                for index, option in enumerate(self.enumAttributes[attribute]['options']):
                                    print(f"      {index+1}: {option}")
                                choice = input(
                                    f"      Enter your choice for attribute {attribute}: ")
                                if choice in ["0", ""]:
                                    dataList.append("DEFAULT")
                                    break
                                elif choice in [str(x) for x in range(1, len(self.enumAttributes[attribute]['options'])+1)]:
                                    dataList.append(
                                        self.enumAttributes[attribute]['options'][int(choice)-1])
                                    break
                                else:
                                    print("      Invalid choice. Select again...")
                                    continue
                        elif attribute in attributesWithAvailableValueDict:
                            print(
                                f"{attributeIndex+1:02}) {attribute}: {attributesWithAvailableValueDict[attribute]}")
                            dataList.append(
                                attributesWithAvailableValueDict[attribute])
                        elif attribute in self.passDefault:
                            print(f"{attributeIndex+1:02}) {attribute}: DEFAULT")
                            dataList.append("DEFAULT")
                        else:
                            while True:
                                value = input(
                                    f"{attributeIndex+1:02}) Enter value for {attribute} (Write DEFAULT for default value): ")
                                if value == "":
                                    print(
                                        "      Value can't be empty. Write again...")
                                    continue
                                else:
                                    break
                            dataList.append(value)
                    print(
                        f"\n=>=>=>=>=>=>=>=>=>Verify Data For Table {table}<=<=<=<=<=<=<=<=<=")
                    for attributeIndex, attribute in enumerate(self.tables[table]):
                        print(
                            f"{attributeIndex+1:02}) {attribute}: {dataList[attributeIndex]}")
                    choice = input(
                        f"Press enter to finalize and save in database (Any other key to rewrite the data for the table {table}): ")
                    if choice == "":
                        if self.__insertData(table, self.__getSqlQuery(table, dataList)):
                            input(
                                "Press any key to continue for INSERT in the next table....")
                            break
                        else:
                            print("Something went wrong while inserting data..")
                            print(
                                f"Write again the data that is to be inserted in the table {table}.")
                            input("Press any key to continue...")
                            continue
                    else:
                        print(
                            f"Write again the data that is to be inserted in the table {table}.")
                        continue
            print("==> Add current file details to another database if you want to. It will ease if you do it now.")
            print("==> Press any key to continue to INSERT for next file..")
            print("==> Press Ctrl + C to exit...")
            try:
                input("Write your choice: ")
            except KeyboardInterrupt:
                print("Exiting...")
                return True
            else:
                fileIndex += 1
                if sys.platform == 'win32':
                    os.system('cls')
                else:
                    os.system('clear')
                continue

    @staticmethod
    def fetchFileMetadata(filePath: str) -> dict | bool:
        """
            Description:
                - Static method to fetch metadata of a file.
                - Meta data includes: File Name, Extension, Size, Date Created, Date Modified.
                - Keep in mind that Date Created and Date Modified are in Epoch format.
                    - You need to convert it to any specific format as per your requirement (Use time and datetime module).

            Args:
                * filePath (str):
                    - Path of the file whose metadata is to be fetched.

            Returns:
                * dict:
                    - Returns a dictionary containing metadata of the file.
                * bool:
                    - Returns False if any error occurs.
                    - Error may be due to invalid file path, file not found, path doesn't specify a file etc.
        """
        if not os.path.exists(filePath) and not os.path.isfile(filePath):
            # if path is not valid then return False or path is not a file.
            return False
        metaData: dict = {}
        metaData['FileName'] = os.path.basename(filePath)
        # os.path.splitext() returns a tuple of (file_name, extension). So, we will take the second element of the tuple.
        metaData['Extension'] = os.path.splitext(filePath)[1]
        metaData['Size'] = os.path.getsize(filePath)
        metaData['DateCreated'] = os.path.getctime(filePath)
        metaData['DateModified'] = os.path.getmtime(filePath)
        return metaData


def main() -> None:
    """
        Description:
            - Driver function to perform the operation to insert data into the database.

        Returns:
            * None
    """
    files = Files()  # instantiating Files class
    if not files.connectionStatus:  # checking if connection is established or not
        print("Connection not established. Exiting...")
        exit(-1)
    files.setTableAttributes()  # setting the table attributes and related data
    files.inputAndInsertInDatabase()


if __name__ == '__main__':
    print("\033[2J\033[H")
    main()
