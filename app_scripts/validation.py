"""
    @file: validation.py
    @author: Suraj Kumar Giri
    @init-date: 1st Feb 2023
    @last-modified: 1st Feb 2023

    @description:
        * Module to validate the data/input sent from client to server as per application configuration and requirements.
        * Warning:
            - Any functions/methods in this module only check the validity of the data/string as per criteria defined in specification of the application.
            - It is the server side validation which is same as client side validation using JavaScript (Need for security purpose because data may be manipulated using proxy servers / man in middle)
            - It doesn't check that the data is logically correct or incorrect.
            - Example:
                - If roll number is passed for validation then it only checks that it is integer or not.
                    - It is not responsible for checking that the roll number is in a particular range like less than 50 etc.
                - If session is passed then it only checks that it must consist of a single hyphen(-) and digits.
                    - It is not responsible for checking that the session must be 2020-23 or 2021-24 etc..
            - Logical check must be performed in the destination script like db_scripts or others responsible for processing data send from client.
        * Usage:
            - May be used as first server side validation check for data received from the client.
            - From client form data is received as string. So, all functions of this module accept that data in string format only.
            - Whatever data received from the client, pass it to the desired function of this module to check validation directly without any modification or processing.
"""


class __Tools:
    """
        Description:
            - Class to provide some tools which can be used while validating data in their respective functions.
            - All methods are static. So, one can access them directly using class name.
            - This is just a wrapper class to wrap methods used as tools while validating data.
    """


def isEmpty(value: str) -> bool:
    """
        Description:
            - Function to check if value is empty or null.

        Args:
            * value (str):
                - Value to be checked.

        Returns:
            * bool: 
                - Returns True if value is empty else False.
    """
    if value in [None, ""]:
        return True
    return False


def isValidSession(session: str, duration: int = 3) -> bool:
    """
        Description:
            - Function to check if the session is valid
            - As per the specification of the application:
                - valid sessions are like: 2015-18, 2020-23, 2019-22 and so on.

        Args:
            * session (str):
                - session to check.
            * duration (int):
                - Duration of the session in years.
                - Default to 3 years.

        Returns:
            * bool:
                - True if the session is valid else False.
    """
    ##### Conditions for session as per application's specification #####
    # session contains one hyphen(-) and rest characters must be digits.
    # year in session must be after 2000 means 2001, 2020, 2010 and so on... (means must be starts with '2')
    # difference between starting year (before hyphen(-)) and ending year (after hyphen(-)) must be 3 or as specified (in years).
    # length of session must be 7.

    # in case of None or empty string passed as session.
    if isEmpty(session):
        return False

    # validating number of characters in session
    if len(session) == 7:
        # checking session must contains 1 hyphen and rest characters must be digits and session must be startswith '2'
        # checking difference between 2 digits before hyphen and 2 digits after hyphen (used string slicing for this purpose)
        # From this commit, session after 2097-xx will also be validated and returned as true.
        if session.count('-') == 1 and session.replace('-', '').isdigit() and session.startswith('2') and str(eval(session[:4] + '+' + str(duration)))[2:] == session[-2:]:
            return True  # if all conditions are satisfied
        return False
    else:
        return False


def isValidSemester(semester: str, maxSemester: int = 6) -> bool:
    """
        Description:
            - Function to check if the semester is valid
            - As per the specification of the application:
                - valid sessions are like: 1, 2, 3 and so on till 6.

        Args:
            * semester (str):
                - Semester
                - Semester in string format because from normal form only string format is send from client and received by the server.
            * maxSemester (int, optional):
                - Maximum number of semesters.
                - Defaults to 6.

        Returns:
            * bool:
                - Returns True if semester is valid else False.
    """
    # in case of None or empty string passed as session.
    if isEmpty(semester):
        return False

    if semester in [str(sem) for sem in range(1, maxSemester+1)]:
        return True  # if all conditions are satisfied
    return False


def isValidIdName(idName: str, validIdList: list | tuple | dict = ['registrationNo', 'examRoll', 'classRoll']) -> bool:
    """
        Description:
            - Function to check if id name is valid or not as the specified criteria of the web application.

        Args:
            * idName (str):
                - ID name to be checked.
            * validIdList (list | tuple | dict, optional):
                - List of valid id names.
                - List may be in list or tuple or dictionary. But in case of dictionary only keys will be used.
                - Defaults to ['registrationNo', 'examRoll', 'classRoll'].

        Returns:
            * Bool:
                - Returns True if id name is valid else False.
    """
    # checking for empty name
    if isEmpty(idName):
        return False

    if idName in validIdList:
        return True  # if id name found in valid id list.
    return False


if __name__ == "__main__":
    print("Module Testing... (Press CTRL+C to exit)")
    try:
        while True:
            data = input("Enter data : ")
            if data == "":
                data = None
            print(isValidIdName(data))
    except KeyboardInterrupt:
        exit(0)
