"""
    @file: my_random.py
    @author: Suraj Kumar Giri
    @init-date: 25th Jan 2023
    @last-modified: 15th April 2023

    @description:
        * Module to generate random numbers of desired digits.
        * Also check if number already exists in the database or not.
    
    @classes:
        * Random:
            - Class to handle all operations related to generating random numbers, checking the existence of number in the database etc.
    @methods:
        * isExists():
            - Function to check if number already exists in the database or not. 
"""
import random
import mysql.connector as mysql
from os import environ
from typing import Type
from string import digits
from time import time
from math import ceil, floor


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
                        - ['mysql', 'pyInt', 'pyStr', 'epoch']
                        - You can pass any of the above four methods to generate random number. Default is 'pyInt'.
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
            return int(number[0])
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

    def __epochTimeRandom(self) -> int | None:
        """
            Description:
                - Method to generate random number using Unix epoch time.
                - It uses Python's time module to get current time in seconds which is epoch time.
                - Epoch time is the number of seconds that have elapsed since 00:00:00 Coordinated Universal Time (UTC), Thursday, 1 January 1970.

            Returns:
                * int
                    - Returns random number if no error occurred.
                * None:
                    - Returns None if any error occurred.
        """
        def __reduceDigits(number: int, requiredDigits: int) -> int:
            """
                Description:
                    - Function to reduce number of digits of give number.

                Args:
                    * number (int):
                        - Number whose digits are to be reduced.
                    * requiredDigits (int):
                        - Number of digits required.
                        - Number of digits in the output number.

                Returns:
                    * int: 
                        - Returns number with reduced digits.

                Caution:
                    - Required digits must be less than or equal to the number of digits in the given number.
                    - In this function, I have not handled the scenario in which given number will have less digits than the required number of digits.
                    - This is because according to code in the parent method of this function, there is no possibility of underflow of digits than required of digits.
                    - There will always same or more digits than required digits in the number generated in if or else block of parent method.
                    - In case of same number of digits, the difference will 0 and n^(0) will be 1. So, it will not affect the output.
            """
            return number//(10**(len(str(number)) - requiredDigits))

        if self.numberOfDigits <= 0:  # if invalid number of digits specified.
            return None
        # getting current epoch time in seconds
        epochSeconds: int = ceil(time())
        # Current value of epoch seconds is 1681569899.5771146 (10 digits excluding digits after decimal point)
        # So, in future digits in epoch seconds will be equal or greater than 10.
        # We use a functionality of random multiplier to increase the intensity of randomness.
        # We have to generate a random number in such a way that it will not follow any sequence.
        if self.numberOfDigits > len(str(epochSeconds)):
            digitDiff = self.numberOfDigits - len(str(epochSeconds))
            # least number of required digits will (epochSeconds x 10^diff)
            # So, we will generate a random number between 10^diff and 10^(diff+1)-1 (this is range of multiplier).
            # It will also increase the intensity of randomness.
            # least multiplier will be 10^diff and maximum will be 10^(diff+1)-1
            # Actually least multiplier ensures that number of digits in random number will be equal to number of digits specified.
            # But maximum multiplier ensures that number of digits in random number will be greater than or equal to number of digits specified.
            # So, in case of max multiplier, it's not sure that number of digits in random number will be same as required number of digits. It may same or more than required number of digits.
            # So, for solve this issue, we will use method reduceDigits() to reduce the number of digits to required number of digits.
            number: int = epochSeconds * \
                random.randint(10**digitDiff, 10**(digitDiff+1)-1)
            # here number of digits in the number may be same or more than required number of digits.
            # So, we use reduceDigits() method to reduce the number of digits to required number of digits.
            return __reduceDigits(number, self.numberOfDigits)
        else:
            # in else suite
            # if number of digits is less than or equal to length of epoch seconds, then we don't need to use random multiplier for increase number of digits.
            # Currently, length of epoch seconds is 10. So, we else suite execute when condition self.numberOfDigits <= 10 satisfies.
            # Here, I am using multiplier for increase the intensity of randomness.
            # here 2,5 in randint() are just selected randomly. There is no logic behind it except providing wide range to receive random number from randint().
            number: int = epochSeconds * random.randint(10**2, 10**5)
            return __reduceDigits(number, self.numberOfDigits)
        # keep in mind, in both suite (if-else), the obtained random will have same or more number of digits than required number of digits.
        # There is no possibility of underflow in number of digits.
        # That's why I have not used any logic to handle underflow in number of digits in the function __reduceDigits().

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
        if self.kwargs.get('method') not in ['mysql', 'pyInt', 'pyStr', 'epoch']:
            category = 'pyInt'  # default method to generate random number
        else:
            category = self.kwargs.get('method')

        # now storing the desired method in a variable 'method' for further use without using if-else every time.
        if category == 'mysql':
            method = self.__mysqlRandom
        elif category == 'pyStr':
            method = self.__pyStrRandom
        elif category == 'epoch':
            method = self.__epochTimeRandom
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

    @staticmethod
    def generateOtp(numberOfDigits: int = 6) -> int:
        """
            Description:
                * Generate OTP based on true random source provided by the OS.
                * May be used to generate random number other than OTP.
            Args:
                * numberOfDigits (int, optional): 
                    - Specify the number of digits to generate for the OTP.
                    - Defaults to 6 digits.

            Returns:
                * int:
                    - Returns generated OTP.

            More:
                * Unlike random.randint(), which generates random numbers based on a pseudo-random algorithm, random.SystemRandom() generates random numbers based on a true random source provided by the operating system. 
                * This makes it more secure and less predictable than random.randint().
                * That's why for OTP generation, random.SystemRandom() has been used.
        """
        sysRandom: random.SystemRandom = random.SystemRandom()
        return sysRandom.randint(10**(numberOfDigits-1), 10**(numberOfDigits)-1)


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
    print(Random(cursor, 'users', 'userId', method='pyStr').generate())

    print("\nWithout checking the database and using method epoch", end=": ")
    print("in main: ", Random(method='epoch').generate(False))
    conn.close()
