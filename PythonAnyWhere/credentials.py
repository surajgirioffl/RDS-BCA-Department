"""
    @file: credentials.py
    @author: Suraj Kumar Giri
    @init-date: 29th Dec 2022
    @last-modified: 9th Jan 2023
    
    @description:
        * Module to store and handle credentials related to account and APIs of PythonAnyWhere.
        
    @global-variables:
        * host
            - Host name of PythonAnyWhere.
"""
from os import environ

__author__ = 'Suraj Kumar Giri'
__email__ = 'surajgirioffl@gmail.com'


host = 'https://www.pythonanywhere.com'  # host name of PythonAnyWhere


def getApiToken(username: str = 'rdsbca') -> str:
    """
        Description:
            * Function to get API token for the given username.

        Args:
            * username: str (default: 'rdsbca')
                - Username of the account.

        Returns:
            * str:
                - API token for the given username.
    """
    tokenDictionary = {
        'rdsbca': environ.get('PAW-RDSBCA-TOKEN'),
        'surajgiridev': environ.get('PAW-RDSBCA-TOKEN')
    }
    return tokenDictionary[username]
