"""
    @file: my_random.py
    @author: Suraj Kumar Giri
    @init-date: 25th Jan 2023
    @last-modified: 25th Jan 2023

    @description:
        * Module to generate random numbers of desired digits.
        * Also check if number already exists in the database or not.
"""
import random
import mysql.connector as mysql
from os import environ
from typing import Type
from string import digits


def isExists(cursor: mysql.connect().cursor, number: int, tableName: str, columnName: str) -> bool | None:
    """
    Description:
        - Function to check if number already exists in the database or not.

    Args:
        * cursor (mysql.connect().cursor):
            - Cursor object returned by mysql.connect() after establishing connection with the database.
        * number (int):
            - Number to be checked.
        * tableName (str):
            - Table name of the database to check the existence of the number
        * columnName (str):
            - Column name of the table in which number is expected to be exist.

    Returns:
        * bool | None:
            - Returns None if any error occurred while executing the query.
            - Returns True if number is already exist else False.

    """
    try:
        cursor.execute(f"""-- sql
                            SELECT {columnName} FROM {tableName}
                            WHERE {columnName} = {number}
                        """)
        data = cursor.fetchone()
        if data is None:  # if number is not found
            return False
        return True  # if number already exists

    except Exception as e:
        print("Something went wrong while executing the query... Error code 1300")
        print("Exception:", e)
        return None


class Random:
    """
        Description:
            - Class to generate random numbers of desired digits.
            - Also provide facility to generate number which is not already exists in the database.

        Methods:
            * generate():
                - Method to generate random number.
    """

    def __init__(self, cursor: Type[mysql.connect().cursor] = ..., tableName: str = ..., columnName: str = ..., digits: int = 8, **kwargs) -> None:
        """
            Description:
                - Class to generate random numbers of desired digits based on specified parameters.
                - Constructor to initialize the class.

            Args:
                * cursor (Type[mysql.connect, optional):
                    - Defaults to ...(ellipsis) which means cursor object is not provided.
                * tableName (str, optional):
                    - Defaults to ...(ellipsis) which means table name is not provided.
                * columnName (str, optional):
                    - Defaults to ...(ellipsis) which means column name is not provided.
                * digits (int, optional):
                    - Number of digits of the random number.
                    - Defaults to 8.
                * kwargs (dict, optional):
                    - key arguments to pass additional parameters.
                    - You can pass key 'method' to specify the method to generate random number.
                    - Pass any other key-value if required. If key is not provided, default value will be used.
                    - methods:
                        - ['mysql', 'pyInt', 'pyStr']
                        - You can pass any of the above three methods to generate random number. Default is 'pyInt'.
                        - And if any error occurs in other method then automatically 'pyInt' will be use to generate random number irrespective which method was passed.

            Returns:
                * None:

            Additional Info:
                * Provide database related parameters only if you want to check if number already exists in the database or not.
                * It also depends on the method you are using to generate random number.
                * If you are using mysql method, then you have to provide database related parameters.
        """
        self.cursor = cursor
        self.tableName = tableName
        self.columnName = columnName
        self.numberOfDigits = digits
        self.kwargs = kwargs

    def __mysqlRandom(self) -> int | None:
        """
            Description:
                - Method to generate random number using mysql RAND() function and other functions of mysql.

            Raises:
                * Exception:
                    - If cursor object is not provided.

            Returns:
                * None: 
                    - Returns None if any error occurred while executing the query or any other error occurred.
                * int
                    - Returns random number if no error occurred.
        """
        try:
            if self.cursor is ...:
                raise Exception("Cursor object is not provided")
        except Exception as e:
            print("Exception:", e)
            return None

        try:
            self.cursor.execute(f"""-- sql
                                    SELECT FLOOR(RAND()* {10**self.numberOfDigits}) as Value
                                """)
            number = self.cursor.fetchone()
            if number is None:
                return None
            return number[0]
        except Exception as e:
            print("Something went wrong while executing the query... Error code 1301")
            return None

    def __pyStrRandom(self) -> int | None:
        """
            Description:
                - Method to generate random number using python's random module.

            Returns:
                * None: 
                    - Returns None if any error occurred while executing the query or any other error occurred.
                * int
                    - Returns random number if no error occurred.
        """
        if self.numberOfDigits < 0:
            return None

        global digits
        # strings are immutable in python. So, we can't use random.shuffle() on it.
        # So, converting the string to list and then shuffling it.
        # digits is a string containing all digits from 0 to 9
        digits = list(digits)
        random.shuffle(digits)  # shuffling the list
        numberList = [random.choice(digits)for _ in range(self.numberOfDigits)]
        return int("".join(numberList))

    def __pyIntRandom(self) -> int | None:
        """
            Description:
                - Method to generate random number using python's random and string modules.

            Returns:
                * None: 
                    - Returns None if any error occurred while executing the query or any other error occurred.
                * int
                    - Returns random number if no error occurred.
        """
        if self.numberOfDigits > 0:
            return random.randint(10**(self.numberOfDigits-1), 10**self.numberOfDigits-1)
        return None

    def generate(self, checkInDatabase: bool = True) -> int:
        """
            Description:
                - Method to generate random number.
                - Prime method to handle all the methods to generate random number.

            Args:
                * checkInDatabase (bool, optional): 
                    - If specified true, then it will check if number already exists in the database or not.
                        - So, if number already exists, then it will generate another random number to return UNIQUE number.
                    - if specified false, then it will not check if number already exists in the database or not and returns whatever number it generates in the first attempt. 
                    - Defaults to True.

            Raises:
                * Exception:
                    - If Database is not connected or configured properly, so that it can check if number already exists in the database or not.

            Returns:
                * int:
                    - Returns random number.
        """
        if self.kwargs.get('method') not in ['mysql', 'pyInt', 'pyStr']:
            category = 'pyInt'  # default method to generate random number
        else:
            category = self.kwargs.get('method')

        # now storing the desired method in a variable 'method' for further use without using if-else every time.
        if category == 'mysql':
            method = self.__mysqlRandom
        elif category == 'pyStr':
            method = self.__pyStrRandom
        else:
            method = self.__pyIntRandom

        if checkInDatabase:
            while True:
                number = method()
                if number is None:
                    # default method to generate random number if any error occurred
                    number = self.__pyIntRandom()
                isNumberExists = isExists(
                    self.cursor, number, self.tableName, self.columnName)
                if isNumberExists is None:
                    raise Exception(
                        "Database is not connected or configured properly. Error code 1303")
                elif isNumberExists:
                    continue  # if number already exists then generate another number because we don't want duplicate numbers
                else:
                    return number
        else:
            number = method()
            if number is None:
                # default method to generate random number if any error occurred
                number = self.__pyIntRandom()
            return number


if __name__ == "__main__":
    # testing the functionality of the class Random
    conn = mysql.connect(host=environ.get('DBHOST'), user=environ.get('DBUSERNAME'), port=int(environ.get(
        'DBPORT')) if environ.get('DBPORT') is not None else 3306, password=environ.get('DBPASSWORD'), database="temp",)
    cursor = conn.cursor()

    print("Without checking the database and without specifying the method to generate random number", end=": ")
    print(Random().generate(False))

    print("With checking the database and without specifying the method to generate random number", end=": ")
    print(Random(cursor=cursor, tableName='users', columnName='userId').generate())

    print("With checking the database and using method mysql", end=": ")
    print(Random(cursor, 'users', 'userId', method='mysql').generate())

    print("With checking the database and using method pyInt", end=": ")
    print(Random(cursor, 'users', 'userId', method='pyInt').generate())

    print("With checking the database and using method pyStr", end=": ")
    print(Random(cursor, 'users', 'userId', method='myStr').generate())

    
    conn.close()
