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
            *
    """

    def __init__(self, cursor: Type[mysql.connect().cursor] = ..., tableName: str = ..., columnName: str = ..., digits: int = 8, **kwargs) -> int | None:
        self.cursor = cursor
        self.tableName = tableName
        self.columnName = columnName
        self.numberOfDigits = digits
        self.kwargs = kwargs

    def __mysqlRandom(self) -> int | None:
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


if __name__ == "__main__":
    conn = mysql.connect(host=environ.get('DBHOST'), user=environ.get('DBUSERNAME'), port=int(environ.get(
        'DBPORT')) if environ.get('DBPORT') is not None else 3306, password=environ.get('DBPASSWORD'), database="temp",)
    cursor = conn.cursor()
    if isExists(cursor, 1235, 'users', 'userId') is None:
        print("Something went wrong while executing the query... Error code 1300")
    elif isExists(cursor, 1235, 'users', 'userId'):
        print("Number already exists")
    else:
        print("Number does not exists")
