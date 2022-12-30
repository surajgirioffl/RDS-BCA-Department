"""
    @file: credentials.py
    @author: Suraj Kumar Giri
    @init-date: 29th Dec 2022
    @last-modified: 29th Dec 2022
    
    @description:
        * Module to store and handle credentials related to account and APIs of PythonAnyWhere.
        
    @global-variables:
        * host
            - Host name of PythonAnyWhere.
"""

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
        'rdsbca': '08c8fd81396723df0627ce2a5cd3550d5ddc9a08',
        'surajgiridev': '68a120e0213c5b6b09f20c9a3e81dba7984f621b'
    }
    return tokenDictionary[username]
