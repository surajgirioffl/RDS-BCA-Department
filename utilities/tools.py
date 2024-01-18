"""
    @author: Suraj Kumar Giri
    @init-date: 18th Jan 2024
    @last-modified: 18th Jan 2024
    @error-series: 2200
    @description:
        * Module to handle database operations related with the database bca.
"""

import json
from datetime import datetime
import pytz


def saveDictAsJSON(dictData: dict, fileNameOrPathWithExtension: str, mode="w", indent=2) -> bool:
    """
    Description:
        - Function to save a dictionary as JSON.

    Parameters:
        * dictData (dict):
            - The dictionary to be saved as JSON.
        * fileNameOrPathWithExtension (str):
            - The name or path of the file where the JSON will be saved (with 'json' extension)
        * mode (str, optional):
            - The file mode to open the file in.
            - Defaults to "w".
        * indent (int, optional):
            - The number of spaces to use for indentation in the JSON.
            - Defaults to 2.

    Returns:
        * bool:
            - True if the dictionary was successfully saved as JSON, False otherwise.
    """
    try:
        jsonData = json.dumps(dictData, indent=indent)
        with open(fileNameOrPathWithExtension, mode) as jsonFile:
            jsonFile.write(jsonData)
    except Exception as e:
        print("Unable to save dictionary as JSON. Error Code: 2201")
        print("Exception:", e)
        return False
    else:
        return True


def loadJSONFile(filePath: str = "settings.json", createFileIfNotExists: bool = False) -> dict | list:
    """
    Description:
        - Function to load JSON file specified in the parameter.
        - The function reads the JSON data and returns it as a dictionary or list (as per JSON).

    Args:
        * filePath (str, optional):
            - Path to the desired JSON file.
            - Defaults to "settings.json".
        * createFileIfNotExists (bool, optional):
            - Whether to create the file if it does not exist.
            - Defaults to False.

    Returns:
        * dict:
            - Return a dictionary or list containing JSON data on success else an empty dictionary.
                - Dictionary if JSON will like {...}
                - List if JSON will like [...]
                - Empty dictionary if JSON file is not found or any error or exception occurs.
    """
    try:
        with open(filePath, "r") as jsonFile:
            jsonData: dict = json.load(jsonFile)
    except FileNotFoundError as e:
        print(f"Unable to open the file {filePath}. Error Code: 2306")
        print("Exception:", e)
        # Creating the file if not exists
        if createFileIfNotExists:
            with open(filePath, "w") as file:
                file.write(str({}))
        return {}
    except Exception as e:
        print(f"Unable to open the file {filePath}. Error Code: 2202")
        print("Exception:", e)
        return {}
    else:
        print(f"{filePath} file loaded successfully...")
        return jsonData


def getCurrentDateTime(timezone: str = 'Asia/Kolkata', formatString: str = "%Y-%m-%d %H:%M:%S"):
    timezone = pytz.timezone(timezone)
    return datetime.now(timezone).strftime(formatString)

if __name__=='__main__':
    print(getCurrentDateTime("America/New_York"))
