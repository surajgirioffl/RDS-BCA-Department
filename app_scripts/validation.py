"""
    @file: validation.py
    @author: Suraj Kumar Giri
    @init-date: 1st Feb 2023
    @last-modified: 30th April 2023
    @error-series: 1800

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

        >>> All functions of this module accept only string as argument which need to be validated irrespective of the type of data it is.
                - Like if you want to validate a roll number then pass it as string.
                - Simply pass the data as it is received from the client. Don't convert it to any other type.
                - And by default data from client is received as string.
"""

import re


class __Tools:
    """
        Description:
            - Class to provide some tools which can be used while validating data in their respective functions.
            - All methods are static. So, one can access them directly using class name.
            - This is just a wrapper class to wrap methods used as tools while validating data.
    """


def isEmpty(value: str | list | tuple | dict | None, ellipsisAsEmpty: bool = True) -> bool:
    """
        Description:
            - Function to check if value is empty or not.
            - If value is Ellipsis then by default it will taken as empty. And True will be returned.
            - By the way, Python treats Ellipsis as non-empty value.
            - You can specify that Ellipsis should be taken as empty or not via variable "ellipsisAsEmpty" whose default value is True.

        Args:
            * value (str | list | tuple | dict | None | ...):
                - Value to be checked.
            * ellipsisAsEmpty (bool, optional):
                - Specify that ellipsis should be taken as empty or not.
                - Default to True. Means Ellipsis will be taken as empty.
                - By the way, Python treats Ellipsis as non-empty value.
                - So, if you want to treat Ellipsis as non-empty value then set this variable to False.

        Returns:
            * bool:
                - Returns True if value is empty else False.
    """
    if value == ... and ellipsisAsEmpty:
        return True  # in case of Ellipsis
    elif value:
        return False  # if no empty value
    return True  # in case of empty value


def isValidSession(session: str, duration: int = 3) -> bool:
    """
        Description:
            - Function to check if the session is valid
            - As per the specification of the application:
                - valid sessions are like: 2015-18, 2020-23, 2019-22 and so on.

        Args:
            * session (str):
                - session to check.
                - Strictly in string format.
            * duration (int):
                - Duration of the session in years.
                - Default to 3 years.

        Returns:
            * bool:
                - True if the session is valid else False.
    """
    ##### Conditions for valid session as per application's specification #####
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
                - Semester to be checked.
                - Strictly in string format.
                - Semester in string format because from normal form only string format is send from client and received by the server.
            * maxSemester (int, optional):
                - Maximum number of semesters.
                - Defaults to 6.

        Returns:
            * bool:
                - Returns True if semester is valid else False.
    """
    ##### Conditions for valid semester as per application's specification #####
    # semester must be integer and in range of 1 to 6.

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


def isValidSource(source: str, validSourceList: list | tuple | dict = ["all", "brabu", "vaishali", "lnMishra"]) -> bool:
    """
        Description:
            - Function to check if source name is valid or not as the specified criteria of the web application.
            - Can be used in route like previous year question.

        Args:
            * source (str):
                - Source name to be checked.
            * validSourceList (list | tuple | dict, optional):
                - List of valid source names.
                - List may be in list or tuple or dictionary. But in case of dictionary only keys will be used.
                - Defaults to ["all", "brabu", "vaishali", "lnMishra"].

        Returns:
            * Bool:
                - Returns True if source name is valid else False.
    """
    return isValidIdName(source, validSourceList)


def isValidRegistrationNo(registrationNo: str) -> bool:
    """
        Description:
            - Function to check if registration number is valid or not as the specified criteria of the web application.

        Args:
            * registrationNo (str):
                - Registration number to be checked.
                - Strictly in string format.

        Returns:
            * bool:
                - Returns True if registration number is valid else False.

    """
    ##### Conditions for valid registration number as per application's specification #####
    # registration number must be alphanumeric

    # if registration number is empty
    if isEmpty(registrationNo):
        return False
    return registrationNo.isalnum()


def isValidClassRollNo(classRollNo: str, isDefinedRange: bool = True, start: int = 1, end: int = 60,  include: list = [], exclude: list = []) -> bool:
    """
        Description:
            - Function to check if class roll number is valid or not as the specified criteria of the web application.

        Args:
            * classRollNo (str):
                - Class Roll number to be checked.
                - Strictly in string format.
            * isDefinedRange (bool, optional):
                - If the range is predefined or not.
                - If this is true then only roll numbers in the range(start to end) will be considered.
                - Defaults to True.
            * start (int, optional):
                - Starting number of the range to be considered while validating roll number.
                - This will included while validating.
                - Not considered if isDefinedRange is False.
                - Defaults to 1.
            * end (int, optional):
                - End number of the range to be considered while validating roll number.
                - This will included while validating.
                - Not considered if isDefinedRange is False.
                - Defaults to 60.
            * include (list, optional):
                - List of roll numbers others than the range to be considered while validating roll number.
                - Roll number contains in this list be considered as valid while validating even if it is not in the range.
                - May be used for some special cases.
                - Defaults to [] (empty list).
                - Must be empty or list of integers (or string of integers but recommended to be integer)
            * exclude (list, optional):
                - List of roll numbers to be excluded while validating roll number.
                - Roll number contains in this list be not considered as valid while validating even if it is in the range.
                - May be used for some special cases.
                - Defaults to [].
                - Must be empty or list of integers (only integers. No string of integers are allowed.)

            Returns:
                * bool:
                    - Returns True if class roll number is valid else False.

            Special:
                * If both include and exclude will be passed and both contains common(same) roll number then finally common roll number will be included.
                * Means include has more priority than exclude.
    """
    ##### Conditions for valid class roll number as per application's specification #####
    # class roll number must be a positive integer and in range of 1 to 60 (inclusive) (May be different in some special cases)

    # checking for empty class roll number
    if isEmpty(classRollNo):
        return False

    # checking if roll number is integer or not
    if classRollNo.isnumeric():
        # checking if roll number is positive or not
        if int(classRollNo) < 1:
            return False  # if roll number is negative

        # 'include' list need to be added. So, converting all elements to string because rollNo is string.
        include = [str(roll) for roll in include]

        # if range is predefined then only roll numbers in the range(start to end) will be considered.
        if isDefinedRange:
            if classRollNo in [str(roll) for roll in range(start, end+1) if roll not in exclude]+include:
                # if range is defined and roll number is within the range.
                return True
        # if range is not predefined then all roll numbers will be considered except listed in exclude list (no need to use 'include' list here)
        else:
            exclude = [str(roll) for roll in exclude]
            if classRollNo not in exclude:
                return True
    return False  # invalid roll number (no condition satisfied)


def isValidExamRollNo(examRollNo: str, isDefinedRange: bool = False, start: int = ..., end: int = ...,  include: list = [], exclude: list = []) -> bool:
    """
        Description:
            - Function to check if exam roll number is valid or not as per the specified criteria of the web application.

        Args:
            * rollNo (str):
                - Exam Roll number to be checked.
                - Strictly in string format.
            * isDefinedRange (bool, optional):
                - If the range is predefined or not.
                - If this is true then only roll numbers in the range(start to end) will be considered.
                - Defaults to False.
            * start (int, optional):
                - Starting number of the range to be considered while validating roll number.
                - This will included while validating.
                - Not considered if isDefinedRange is False.
                - Defaults to ...
            * end (int, optional):
                - End number of the range to be considered while validating roll number.
                - This will included while validating.
                - Not considered if isDefinedRange is False.
                - Defaults to ...
            * include (list, optional):
                - List of roll numbers others than the range to be considered while validating roll number.
                - Roll number contains in this list be considered as valid while validating even if it is not in the range.
                - May be used for some special cases.
                - Defaults to [] (empty list).
                - Must be empty or list of integers (or string of integers but recommended to be integer)
            * exclude (list, optional):
                - List of roll numbers to be excluded while validating roll number.
                - Roll number contains in this list be not considered as valid while validating even if it is in the range.
                - May be used for some special cases.
                - Defaults to [].
                - Must be empty or list of integers (only integers. No string of integers are allowed.)

            Returns:
                * bool:
                    - Returns True if exam roll number is valid else False.

            Special:
                * If both include and exclude will be passed and both contains common(same) roll number then finally common roll number will be included.
                * Means include has more priority than exclude.
    """
    ##### Conditions for valid exam roll number as per application's specification #####
    # Exam roll number must be a positive integer [may be in a specified range (inclusive) (May be different in some special cases)]

    return isValidClassRollNo(examRollNo, isDefinedRange, start, end, include, exclude)


def isValidIdValue(idName: str, idValue: str) -> bool:
    """
        Description:
            - Function to check if id value is valid or not for the given id name as per the specified criteria of the web application.
            - Id name may be 'registrationNo', 'classRoll', 'examRoll' etc.
            - This function is helpful in such condition when both are supplied by the client/user and need to be checked.
            - This function is helpful if user has given to select id name from a list of options and then need to enter id value.
            - Or can used as per the requirement.

        Args:
            * idName (str):
                - Name of the id to be checked.
            * idValue (str):
                - Value of the provided id name to be checked.
                - Strictly in string format irrespective of any condition.

        Returns:
            * bool:
                - Returns True if id value is valid else False.
                - Return False if id name is not found.
    """
    if idName == 'registrationNo':
        return isValidRegistrationNo(idValue)
    elif idName == 'classRoll':
        return isValidClassRollNo(idValue)
    elif idName == 'examRoll':
        return isValidExamRollNo(idValue)
    else:
        print(f"ID Name '{idName}' not found.")
        return False


def isValidEmail(email: str, allowDefaultDisposableEmailDomains: bool = False, includeMails: list = ..., excludeMails: list = ..., prohibitedDomains: list = ..., allowedDomains: list = ...) -> bool:
    """
        Description:
            - 

        Args:
            * email (str):
                - Email address to be checked. 
            * allowDefaultDisposableEmailDomains (bool, optional):
                - Specify that default list of disposable domains should be allowed or not.
                - If True then disposable domain list will be ignored.
                - If False (default) then disposable domain list will be considered and if email matched with any of the domain then it will be considered as invalid.  
                - Defaults to False.
            * includeMails (list, optional):
                - List of emails to be included while validating email.
                - List of any emails that should be included at any cost.
                - It will be considered with top priority. 
                - It will be considered even if email matched with any of the disposable domain or exclude list emails.
                - Defaults to ....
            * excludeMails (list, optional): 
                - List of emails to be excluded while validating email.
                - List of any emails that should be excluded at any cost.
                - It will be considered after include list.
                - Defaults to ....
            * prohibitedDomains (list, optional): 
                - List of domains to be prohibited while validating email.
                - You can pass any domain name that you want to prohibit. 
                - Domains of this list will be considered as invalid.
                - Given to extend the default list of disposable domains.
                - Defaults to ....
            * allowedDomains (list, optional): 
                - List of domains to be allowed while validating email.
                - Given to override the default list of disposable domains.
                - Defaults to ....

        Returns:
            * bool: 
                - Returns True if the email is valid else False.

        More:
            - prohibitedDomains has more priority than allowedDomains.
            - Means if email matched with any of the domain of prohibitedDomains then it will be considered as invalid even if it matched with any of the domain of allowedDomains.
    """
    # some disposable email domains (default)
    defaultDisposalEmailDomains: list = [
        "10minutemail.com",
        "temp-mail.org",
        "guerrillamail.com",
        "mailinator.com",
        "sharklasers.com",
        "throwawaymail.com",
        "getairmail.com",
        "fakeinbox.com",
        "yopmail.com",
        "burnermail.io"
    ]

    # if email is empty
    if isEmpty(email):
        return False
    # if email is in include list
    if not isEmpty(includeMails):
        if email in includeMails:
            return True
    # if email is in exclude list
    if not isEmpty(excludeMails):
        if email in excludeMails:
            print("Email is in exclude list.")
            return False
    # if email-domain is in prohibited domains list
    if not isEmpty(prohibitedDomains):
        for domain in prohibitedDomains:
            if(email.endswith(domain)):
                print("Email with prohibited domains are not allowed.")
                return False
    # if email-domain is in allowed domains list
    if not isEmpty(allowedDomains):
        for domain in allowedDomains:
            try:
                defaultDisposalEmailDomains.remove(domain)
            except Exception as e:
                print(
                    "Something went wrong while removing allowed domains from default disposable domains list. Error Code: 1800")
                print("Exception: ", e)
    # If default disposable email domains are allow or not
    if not allowDefaultDisposableEmailDomains:
        for domain in defaultDisposalEmailDomains:
            if(email.endswith(domain)):
                print(
                    "Disposable Email Domains are not allowed (Found from default disposable list).")
                return False
    emailRegex: re.Pattern = re.compile("^[a-zA-Z0-9+.-_]+@[a-zA-Z0-9.-]+$")
    if(emailRegex.match(email)):
        return True
    return False


def isValidFileId(fileId: str, length: int = 8, include: list[str | int] = [], exclude: list[str | int] = []) -> bool:
    """
        Description:
            - Function to check if file id is valid or not.

        Args:
            * fileId (str): 
                - File id to be checked.
            * length (int, optional): 
                - Length of the valid file id.
                - Defaults to 8.
            * include (list, optional): 
                - List of file ids to be included while validating file id irrespective of any other condition.
                - File Id in this list will be considered even if it's not follow any criteria like length, must be numeric etc.
                - May be used for some special file ids.
                - Must be empty or list of integers or strings.
                - Defaults to [] (empty list).
            * exclude (list, optional): 
                - List of file ids to be excluded while validating file id irrespective of any other condition (except included in the include list).
                - File Id in this list will not be considered even if it's follow all the criteria like length, must be numeric etc.
                - May be used for some special file ids.
                - Must be empty or list of integers or strings.
                - Defaults to [] (empty list).

        Returns:
            * bool: 
                - Returns True if file id is valid else False.

        Special:
            - If file id is in include list then it will be considered with top priority irrespective of any other condition like length, must be number etc.
            - If same file id is passed in both include and exclude list then it will be considered as valid because include list has top priority (Means it will not be considered as an item of exclude list).
            - Simply, file ids of include list have top priority and file ids of exclude list have 2nd top priority.

    """
    ##### Conditions for valid file id as per application's specification #####
    # File id must be an integer having length of 8 digits.

    # if fileId is empty
    if isEmpty(fileId):
        return False

    # if fileId is in include list. It will be considered with top priority irrespective of any other condition like length, must be number etc.
    if fileId in [str(id) for id in include]:
        return True

    # if fileId is in exclude list. It will be considered with 2nd top priority irrespective of any other condition like length, must be number etc.
    # Means we have given include list with top priority and exclude list with 2nd top priority.
    # So, if a same fileId is in both include and exclude list then it will be considered as valid because include list has top priority (Means it will not be considered as an item of exclude list).
    if fileId in [str(id) for id in exclude]:
        return False

    # Now, We will check fileId using default criteria specified by the application.
    # checking if fileId is numeric or not
    if fileId.isnumeric():
        # checking if fileId is of specified length or not
        if len(fileId) == length:
            return True
    return False  # if any of the above condition is not satisfied then return False


if __name__ == "__main__":
    print("Module Testing... (Press CTRL+C to exit)")
    try:
        while True:
            data = input("Enter data : ")
            if data == "":
                data = None
            print(isValidFileId(data, include=[121, 'giri']))
    except KeyboardInterrupt:
        exit(0)
