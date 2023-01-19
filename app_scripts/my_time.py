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


if __name__ == '__main__':
    print(readableDateTime())
