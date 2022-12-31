
"""
    @file: filesApi.py
    @author: Suraj Kumar Giri
    @init-date: 31st Dec 2022
    @last-modified: 31st Dec 2022

    @description:
        * Module deals with all files operations related with files API endpoint of PythonAnyWhere.
"""


def menu() -> int:
    """
        Description:
            - To display menu for files operations and take user input.

        Returns:
            * int:
                - 1: If user wants to write content and upload in a file.
                - 2: If user wants to upload an existing file from local directory.
    """
    print("""
          Basics:
                01. Write content and upload in a file (Press anything except 2).
          Advanced:
                02. Upload an existing file from local directory.
          """)
    choice = input("Write your choice: ")
    if choice == "2":
        return 2
    return 1


def userInputUpload() -> dict:
    """
        Description:
            - To take user input for contents of file to be uploaded along with file name.
            - This will not do any operations related to upload existing file from local directory.
            - It will upload contents written by use on console as asked in a file.

        Returns:
            * dict: 
                - dict = {"filename": fileName, "content": content}
                - dictionary with file name and content to be uploaded in that file.

    """
    fileName = input(
        "Enter the file name with extension that will be created or updated in PythonAnywhere: ")
    content = input("Enter the content that will be written in the file: ")
    return {"fileName": fileName, "content": content}
