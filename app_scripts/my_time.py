"""
    @author: Suraj Kumar Giri
    @init-date: 19th Jan 2023
    @last-modified: 19th Jan 2023

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


def readableMySqlDateTime(dateTime: str) -> str:
    """
        Description:
            - Function to convert MySQL datetime string to readable format.
            - Readable format is like 19 Jan 2023 12:30:00 PM

        Args:
            * dateTime (str):
                - MySQL datetime string to be converted in to readable format.

        Returns:
            * str:
                - Readable datetime string.
                - Format is like 19 Jan 2023 12:30:00 PM
    """
    # Below is the format of MySQL datetime string
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
    print(readableMySqlDateTime('2023-01-09 13:55:30'))
