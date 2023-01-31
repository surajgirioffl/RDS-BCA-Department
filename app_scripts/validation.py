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
"""


def isValidSession(session: str) -> bool:
    """
        Description:
            - Function to check if the session is valid
            - As per the specification of the application:
                - valid session is like: 2015-18, 2020-23, 2019-22 and so on.

        Args:
            * session (str):
                - session to check.

        Returns:
            * bool:
                - True if the session is valid else False.
    """
    ##### Conditions for session as per application's specification #####
    # session contains one hyphen(-) and rest characters must be digits.
    # year in session must be after 2000 means 2001, 2020, 2010 and so on... (means must be starts with '2')
    # difference between starting year (before hyphen(-)) and ending year (after hyphen(-)) must be 3.
    # length of session must be 7.

    # in case of None or empty string passed as session.
    if session in [None, ""]:
        return False

    # validating number of characters in session
    if len(session) == 7:
        # checking session must contains 1 hyphen and rest characters must be digits and session must be startswith '2'
        # checking difference between 2 digits before hyphen and 2 digits after hyphen
        if session.count('-') == 1 and session.replace('-', '').isdigit() and session.startswith('2') and eval('{starts}-{ends}'.format(starts=session[:4], ends=session[:2]+session[5:])) == -3:
            return True  # if all conditions are satisfied
        return False
    else:
        return False


if __name__ == "__main__":
    data = input("Enter data: ")
    if data == "":
        data = None
    print(isValidSession(data))
