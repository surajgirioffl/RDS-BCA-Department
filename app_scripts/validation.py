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
