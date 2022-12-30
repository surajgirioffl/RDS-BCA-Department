"""
    @file: tools.py
    @author: Suraj Kumar Giri
    @init-date: 29th Dec 2022
    @last-modified: 29th Dec 2022
    
    @description:
        * Module containing program to perform multiple operation while dealing with PythonAnyWhere API in @file main.py.
        
    @functions:
        * getVariablesFromFormat()
            - To extract the list of variables from a format string.
"""


def getVariablesFromFormat(stringFormat) -> list | None:
    """
        Description:
            Returns a list of variables from a string format.

        Args:
            * stringFormat (str):
                    - Format of a string.

        Returns:
            * list:
                - list of variables extracted from the string format.
            * None:
                - if no variables are found in the format string.
    """
    numberOfBraces = stringFormat.count('{')
    variables = []
    for i in range(numberOfBraces):
        variables.append(
            stringFormat[stringFormat.find('{')+1: stringFormat.find('}')])
        stringFormat = stringFormat[stringFormat.find('}')+1:]
    if variables:
        return variables
    return None


if __name__ == '__main__':
    variables = getVariablesFromFormat('Hello {name}, your age is {age}.')
    print(variables)
