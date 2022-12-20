"""
    @author: Suraj Kumar Giri
    @date: 20 December 2022
    @description:
        * Module to handle database operations related to registration number of students.
        * Like fetching students details using the registration number.
    @classes:
        * FetchDetails:
            - Class to fetch all details related a student based on registration number.
"""
import sqlite3 as sqlite

__author__ = 'Suraj Kumar Giri'
__email__ = 'surajgirioffl@gmail.com'


class FetchDetails:
    """
        @description:
            - Class to fetch all details related a student based on registration number.

        @methods:
            * getDetails():
                - To fetch result of students using various methods (using registrationNo).
    """

    def __init__(self, databaseName: str = 'bca') -> None:
        """
            @description:
                - Constructor to initialize the class.

            @args:
                * databaseName(str,optional):
                    - Name of the database to connect.

            @returns:
                * None
        """
        try:
            self.conn = sqlite.connect(f'database/{databaseName}.db')
            self.cursor = self.conn.cursor()
            self.connectionStatus = True
        except Exception as e:
            print(e)
            print('Connection failed. Error code 101')
            # To check if connection is established or not.
            self.connectionStatus = False

    def __del__(self) -> None:
        """
            @description:
                - Destructor to destroy the instance.
        """
        if self.connectionStatus:
            self.conn.close()

    def __connectToDatabase(databaseName: str) -> sqlite.Connection | None:
        """
                Description:
                    - To connect to any databases.

                Args:
                    * databaseName (str):
                        - Name of the database to connect.

                Returns:
                    * sqlite.Connection:
                        - Connection object of the database.
                    * None:
                        - In case of any failure.
        """
        try:
            return sqlite.connect(f'database/{databaseName}.db')
        except Exception as e:
            print(e)
            print('Connection failed. Error Code 102.')
            return None

    def getDetails(self, registrationNo: str) -> dict | None:
        """
                Description:
                    - To fetch result of students using registrationNo.

                Args:
                    * registrationNo (str):
                        - RegistrationNo of student.

                Returns:
                    * dict:
                        - If data found on given constraints.
                        - Dictionary containing all desired values with respective keys. 
                    * None:
                        - In case of any failure.
                        - If data not found in database.
                        - In case of invalid credentials
            """
        # if connection is not established then return None.
        if not self.connectionStatus:
            return None
        # if connection is established then fetch the data.

        session = self.cursor.execute(
            'SELECT session FROM Students WHERE registrationNo=?', (registrationNo,)).fetchone()[0]
        if session is None:
            return None
        conn = FetchDetails.__connectToDatabase(session)
        cursor = conn.cursor()
        details = cursor.execute(
            'SELECT name,classRoll,examRoll FROM Students WHERE registrationNo=?', (registrationNo,)).fetchone()
        print(details)
        conn.close()
        detailsDictionary = {
            'name': details[0], 'classRoll': details[1], 'examRoll': details[2]}
        return detailsDictionary


if __name__ == '__main__':
    print(FetchDetails().getDetails('20BCVGCS010'))
