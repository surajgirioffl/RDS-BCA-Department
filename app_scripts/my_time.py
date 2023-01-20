"""
    @author: Suraj Kumar Giri
    @init-date: 19th Jan 2023
    @last-modified: 20th Jan 2023

    @description:
        * Module to handle all the time related operations involving in the web app.
    
    @functions:
        *
"""
import datetime


def readableDateTime(dateTime: datetime.datetime = datetime.datetime.now()) -> str:
    """
        Description:
            - Function to convert datetime object to readable format.
            - Readable format is like 19 Jan 2023 12:30:00 PM

        Args:
            * dateTime (datetime.datetime, optional):
                - Datetime object to be converted to readable format.
                - Default to current datetime.

        Returns:
            * str:
                - Readable datetime string.
                - Format is like 19 Jan 2023 12:30:00 PM
    """
    return dateTime.strftime("%d %b %Y %I:%M:%S %p")


def readableStringDateTime(dateTime: str) -> str:
    """
        Description:
            - Function to convert string format of datetime to readable format.
            - Readable format is like 19 Jan 2023 12:30:00 PM

        Args:
            * dateTime (str):
                - Datetime string to be converted in to readable format.
                - Accepted format is "2023-01-09 13:55:30"

        Returns:
            * str:
                - Readable datetime string.
                - Format is like 19 Jan 2023 12:30:00 PM
    """
    # Below is the format of MySQL datetime string (But by fetching DATETIME data using mysql.connector, it will convert it into python datetime.datetime object similarly as done by this function.)
    # 2023-01-09 13:55:30

    # fetching each element from the datetime string
    dateTimeDict = {
        'year': int(dateTime[:4]),
        'month': int(dateTime[5:7]),
        'day': int(dateTime[8:10]),
        'hour': int(dateTime[11:13]),
        'minute': int(dateTime[14:16]),
        'second': int(dateTime[17:])
    }
    return readableDateTime(datetime.datetime(**dateTimeDict))


if __name__ == '__main__':
    print(readableDateTime())
    print(readableStringDateTime('2023-01-09 13:55:30'))
